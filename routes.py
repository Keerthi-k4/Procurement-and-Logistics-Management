from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Customer, Product, CustomerOrder, Inventory, Procurement, Location, Supplier
from datetime import datetime, timedelta
from sqlalchemy import text
from extensions import bcrypt  # Import bcrypt from extensions

routes_bp = Blueprint('routes', __name__)

# Routes
@routes_bp.route('/')
def index():
    return render_template('index.html')  # Main landing page


#########################################################################################################################
# inventory
#########################################################################################################################

# Inventory Manager routes
@routes_bp.route('/inventory')
def inventory_dashboard():
    return render_template('inventory/inventory_index.html')


@routes_bp.route('/inventory/check_stock', methods=['GET'])
def check_stock():
    # Call the stored procedure to get low-stock items
    low_stock_items = db.session.execute(text('CALL CheckLowStockItems()')).fetchall()
    if not low_stock_items:
        flash('All items are sufficiently stocked.', 'info')  # Flash message for sufficiently stocked items

    return render_template('inventory/check_stock.html', low_stock_items=low_stock_items)

# Route to create a procurement order for a specific low-stock item
@routes_bp.route('/inventory/create_procurement_order', methods=['POST'])
def create_procurement_order():
    inventory_id = request.form.get('inventory_id')  # Get inventory_id from the form
    order_quantity = int(request.form.get('order_quantity'))  # Get quantity from the form
    expected_delivery_date = request.form.get('expected_delivery_date')  # Get expected delivery date from the form

    # Fetch the inventory item and associated product details
    item = db.session.query(Inventory).filter_by(Inventory_ID=inventory_id).first()

    if item:
        # Get the product price
        product_price = item.Product.Price

        # Calculate the total cost (product price * quantity)
        total_cost = product_price * order_quantity

        # Create the procurement order
        procurement_order = Procurement(
            Supplier_ID=item.Supplier_ID,
            Expected_delivery_date=expected_delivery_date,  # Use the user-provided expected delivery date
            Total_cost=total_cost
        )

        # Add the procurement order to the session
        db.session.add(procurement_order)

        # Update the stock level in the Inventory table
        item.Stock_level += order_quantity

        # Commit both the new procurement order and stock update
        db.session.commit()

        flash(f'Procurement order created successfully for {item.Product.Product_name}. Stock level updated.', 'success')
    else:
        flash('Item not found for procurement order.', 'danger')

    return redirect(url_for('routes.check_stock'))  # Redirect back to the check stock page


# Route to view inventory details for each location
@routes_bp.route('/inventory/view_inventory', methods=['GET'])
def view_inventory():
    # Call the stored procedure to fetch inventory items with location and product details
    result = db.session.execute(text('CALL ViewInventory()'))

    # Convert the result into a list of dictionaries
    inventory_items = result.fetchall()
    location_inventory = {}

    for row in inventory_items:
        location_name = row.Location_name  # Access the location name from the result
        if location_name not in location_inventory:
            location_inventory[location_name] = []

        # Append item details as a dictionary
        location_inventory[location_name].append({
            'Inventory_ID': row.Inventory_ID,
            'Stock_level': row.Stock_level,
            'Reorder_point': row.Reorder_point,
            'Product_name': row.Product_name,
            'Price': row.Price,
        })

    return render_template('inventory/view_inventory.html', location_inventory=location_inventory)

#########################################################################################################################
# customer
#########################################################################################################################


# Routes
@routes_bp.route('/customer')
def customer_dashboard():
    return render_template('customer/customer_index.html')  # Main Customer landing page

@routes_bp.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        customer = Customer.query.filter_by(Email=email).first()

        if customer and check_password_hash(customer.Password, password):
            session['customer_id'] = customer.Customer_ID
            session['role'] = 'customer'  # Store the role in the session
            flash('Logged in successfully', 'success')
            return redirect(url_for('routes.products_page'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('customer/customer_login.html')

@routes_bp.route('/customer/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form['Customer_name']
        phone = request.form['Phone_no']
        email = request.form['Email']
        address = request.form['Address']
        password = request.form['Password']

        # Check if the email already exists
        if Customer.query.filter_by(Email=email).first():
            flash('Email already registered', 'error')
        else:
            hashed_password = generate_password_hash(password)

            # Create customer record in the database
            customer = Customer(Customer_name=name, Phone_no=phone, Email=email, Address=address, Password=hashed_password)
            db.session.add(customer)
            db.session.commit()
            flash('Account created successfully', 'success')
            return redirect(url_for('routes.customer_login'))
    return render_template('customer/customer_create_account.html')


@routes_bp.route('/customer/products_page', methods=['GET'])
def products_page():
    # Ensure only customers can access this page
    if session.get('role') != 'customer':
        flash('Access denied', 'error')
        return redirect(url_for('routes.customer_login'))

    # Fetch all products and group them by category
    categories = db.session.execute(text("""
        SELECT DISTINCT Category 
        FROM Product
    """)).fetchall()

    products_by_category = {}
    for category in categories:
        category_name = category[0]
        products = Product.query.filter_by(Category=category_name).all()
        products_by_category[category_name] = products

    return render_template('customer/customer_products_page.html', products_by_category=products_by_category)

@routes_bp.route('/customer/order_page', methods=['POST'])
def order_page():
    if session.get('role') != 'customer':
        flash('Access denied', 'error')
        return redirect(url_for('routes.customer_login'))

    product_id = request.form['Product_ID']
    quantity = int(request.form['Quantity'])  # Ensure quantity is an integer
    customer_id = session.get('customer_id')

    # Retrieve the product and associated inventory
    product = Product.query.get(product_id)
    inventory = Inventory.query.filter_by(Product_ID=product_id).first()

    if inventory and inventory.Stock_level >= quantity:
        # Calculate the total amount
        total_amount = product.Price * quantity



        # Create the order
        order = CustomerOrder(
            Status='Pending',
            Total_amount=total_amount,
            Customer_ID=customer_id,
            Product_ID=product_id,
            Quantity=quantity
        )
        db.session.add(order)
        db.session.commit()

        # Pass order details to the confirmation template
        order_details = {
            'product_name': product.Product_name,
            'quantity': quantity,
            'total_amount': total_amount,
            'order_date': order.Order_date,
            'status': order.Status
        }

        return render_template('customer/order_page.html', order_details=order_details)
    else:
        # Handle insufficient stock
        flash("Insufficient stock for the requested quantity.", "error")
        return redirect(url_for('routes.products_page'))
@routes_bp.route('/customer/orders', methods=['GET'])
def customer_orders():
    if session.get('role') != 'customer':
        flash('Access denied', 'error')
        return redirect(url_for('routes.index'))

    customer_id = session.get('customer_id')

    # SQL query to get all orders for the logged-in customer
    orders_query = db.session.execute(text(""" 
        SELECT co.Customer_order_ID, co.Order_date, co.Status, co.Total_amount, co.Quantity, p.Product_name
        FROM Customer_Order co
        JOIN Product p ON co.Product_ID = p.Product_ID
        WHERE co.Customer_ID = :customer_id
        ORDER BY co.Order_date DESC
    """), {'customer_id': customer_id})

    orders = orders_query.fetchall()

    # Nested SQL query to get aggregated data for product categories
    category_count_query = db.session.execute(text("""
        SELECT p.Category, 
               COUNT(co.Product_ID) AS product_count,
               SUM(co.Total_amount) AS total_spent,
               COUNT(DISTINCT co.Customer_order_ID) AS order_count,
               (
                   SELECT SUM(co2.Total_amount)
                   FROM Customer_Order co2
                   JOIN Product p2 ON co2.Product_ID = p2.Product_ID
                   WHERE co2.Customer_ID = :customer_id AND p2.Category = p.Category
               ) AS category_total_spent
        FROM Customer_Order co
        JOIN Product p ON co.Product_ID = p.Product_ID
        WHERE co.Customer_ID = :customer_id
        GROUP BY p.Category
    """), {'customer_id': customer_id})

    category_counts = category_count_query.fetchall()

    return render_template('customer/customer_orders.html', orders=orders, category_counts=category_counts)

#########################################################################################################################
# supplier
#########################################################################################################################
# Supplier routes
@routes_bp.route('/supplier')
def supplier_dashboard():
    return render_template('supplier/supplier_index.html')

# Route to create a supplier account
@routes_bp.route('/supplier/create_account', methods=['GET', 'POST'])
def create_supplier_account():
    if request.method == 'POST':
        name = request.form['Supplier_name']
        phone = request.form['Phone_no']
        email = request.form['Email']
        password = request.form['Password']

        if Supplier.query.filter_by(Email=email).first():
            flash('Email already registered', 'error')
        else:
            hashed_password = generate_password_hash(password)
            supplier = Supplier(Supplier_name=name, Phone_no=phone, Email=email, Password=hashed_password)
            db.session.add(supplier)
            db.session.commit()
            flash('Supplier account created successfully', 'success')
            return redirect(url_for('routes.supplier_login'))
    return render_template('supplier/supplier_create_account.html')

# Route to log in as supplier
@routes_bp.route('/supplier/login', methods=['GET', 'POST'])
def supplier_login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        supplier = Supplier.query.filter_by(Email=email).first()

        if supplier and check_password_hash(supplier.Password, password):
            session['supplier_id'] = supplier.Supplier_ID
            flash('Login successful', 'success')
            return redirect(url_for('routes.view_supplier_information'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('supplier/supplier_login.html')


# Route to view supplier information
@routes_bp.route('/supplier/view_supplier_information', methods=['GET'])
def view_supplier_information():
    supplier_id = session.get('supplier_id')  # Retrieve supplier_id from session

    if not supplier_id:
        flash('Please log in to view supplier information', 'warning')
        return redirect(url_for('routes.supplier_login'))

    supplier = Supplier.query.get(supplier_id)
    return render_template('supplier/view_supplier_information.html', supplier=supplier)

@routes_bp.route('/supplier/add_product', methods=['GET', 'POST'])
def add_product():
    supplier_id = session.get('supplier_id')  # Retrieve supplier_id from session

    if not supplier_id:
        flash('Please log in to add a product', 'warning')
        return redirect(url_for('routes.supplier_login'))

    if request.method == 'POST':
        # Get form data for Product
        product_name = request.form['product_name']
        price = request.form['price']
        category = request.form['category']

        # Create a new Product entry
        new_product = Product(
            Product_name=product_name,
            Price=price,
            Category=category
        )
        db.session.add(new_product)
        db.session.commit()

        # Get Inventory-specific details, including location
        quantity = request.form['quantity']
        location_id = request.form['location_id']  # Location is part of Inventory
        reorder_point = request.form['reorder_point']

        # Create a new Inventory entry linking Product to Location
        inventory_item = Inventory(
            Stock_level=quantity,
            Supplier_ID=supplier_id,
            Product_ID=new_product.Product_ID,
            Location_ID=location_id,
            Reorder_point=reorder_point
        )
        db.session.add(inventory_item)
        db.session.commit()

        flash('Product added to inventory successfully!', 'success')
        return redirect(url_for('routes.add_product'))

    return render_template('supplier/add_product.html')


# Route to view order fulfillment status
@routes_bp.route('/supplier/order_status', methods=['GET'])
def order_status():
    supplier_id = 1  # Example ID; this should be dynamic
    orders = CustomerOrder.query.filter_by(Supplier_ID=supplier_id).all()
    return render_template('supplier/order_status.html', orders=orders)

@routes_bp.route('/supplier/manage_products', methods=['GET', 'POST'])
def manage_products():
    # Assuming the supplier is logged in and their ID is stored in the session
    supplier_id = session.get('supplier_id')  # Get the supplier ID from the session or some other way

    # Fetch products that belong to the logged-in supplier through Inventory table
    inventory_items = Inventory.query.filter_by(Supplier_ID=supplier_id).all()

    # Get the unique Product_IDs from the filtered Inventory items
    product_ids = [item.Product_ID for item in inventory_items]

    # Fetch products only for the logged-in supplier
    products = Product.query.filter(Product.Product_ID.in_(product_ids)).all()

    if request.method == 'POST':
        product_id = request.form['product_id']
        action = request.form['action']

        if action == 'update':
            # Update product information
            product = Product.query.get(product_id)
            product.Product_name = request.form['product_name']
            product.Price = request.form['price']
            product.Category = request.form['category']
            db.session.commit()
            flash('Product updated successfully!', 'success')

        elif action == 'remove':
            # Remove the product
            product = Product.query.get(product_id)
            db.session.delete(product)
            db.session.commit()
            flash('Product removed successfully!', 'success')

    return render_template('supplier/manage_products.html', products=products)


#########################################################################################################################
# procurement
#########################################################################################################################
# Procurement Officer routes
@routes_bp.route('/procurement')
def procurement_dashboard():
    return render_template('procurement/procurement_index.html')


@routes_bp.route('/procurement/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        supplier_id = request.form['supplier_id']
        total_cost = request.form['total_cost']
        expected_delivery_date = request.form['expected_delivery_date']

        new_procurement = Procurement(Supplier_ID=supplier_id, Total_cost=total_cost,
                                      Expected_delivery_date=expected_delivery_date)
        db.session.add(new_procurement)
        db.session.commit()
        flash('Purchase order created successfully!', 'success')
        return redirect(url_for('routes.create_order'))

    suppliers = Supplier.query.all()
    return render_template('procurement/create_order.html', suppliers=suppliers)

@routes_bp.route('/procurement/view_orders')
def view_orders():
    orders = Procurement.query.all()
    return render_template('procurement/view_orders.html', orders=orders)

@routes_bp.route('/procurement/delete_order/<int:procurement_id>', methods=['POST'])
def delete_order(procurement_id):
    order = Procurement.query.get(procurement_id)
    if order:
        db.session.delete(order)
        db.session.commit()
        flash('Procurement order deleted successfully!', 'success')
    else:
        flash('Order not found.', 'error')
    return redirect(url_for('routes.view_orders'))

#########################################################################################################################
# logistics
#########################################################################################################################

# Logistics Coordinator routes
@routes_bp.route('/logistics')
def logistics_dashboard():
    return render_template('logistics/logistics_index.html')  # Logistics main dashboard
@routes_bp.route('/logistics/shipment_status', methods=['GET'])
def shipment_status():
    # Fetch all shipments and their statuses, including customer location
    shipments = db.session.execute(text(""" 
        SELECT sl.Shipment_ID, sl.Shipment_status, sl.Delivery_date,
               c.Customer_name, p.Product_name, l.Location_name AS Warehouse_Location,
               c.Address AS Customer_Location  -- Use c.Address directly for Customer Location
        FROM Shipment_Logistics sl
        JOIN Customer_Order co ON sl.Customer_order_ID = co.Customer_order_ID
        JOIN Customer c ON co.Customer_ID = c.Customer_ID
        JOIN Product p ON co.Product_ID = p.Product_ID
        JOIN Location l ON sl.Warehouse_Location_ID = l.Location_ID
    """)).fetchall()

    return render_template('logistics/shipment_status.html', shipments=shipments)

@routes_bp.route('/logistics/update_shipment_status', methods=['POST'])
def update_shipment_status():
    shipment_id = request.form.get('shipment_id')
    new_status = request.form.get('new_status')

    # Update the status of the shipment
    db.session.execute(text("UPDATE Shipment_Logistics SET Shipment_status = :new_status WHERE Shipment_ID = :shipment_id"),
                       {'new_status': new_status, 'shipment_id': shipment_id})
    db.session.commit()

    flash('Shipment status updated successfully!', 'success')
    return redirect(url_for('routes.shipment_status'))

@routes_bp.route('/logistics/view_deliveries', methods=['GET'])
def view_deliveries():
    # Display delivery details and their current statuses
    deliveries = db.session.execute(text(""" 
        SELECT sl.Shipment_ID, sl.Shipment_status, sl.Delivery_date, c.Customer_name, l.Location_name
        FROM Shipment_Logistics sl
        JOIN Customer_Order co ON sl.Customer_order_ID = co.Customer_order_ID
        JOIN Customer c ON co.Customer_ID = c.Customer_ID
        JOIN Location l ON sl.Warehouse_Location_ID = l.Location_ID
        WHERE sl.Shipment_status = 'Delivered'
    """)).fetchall()

    return render_template('logistics/view_deliveries.html', deliveries=deliveries)


@routes_bp.route('/logistics/schedule_delivery', methods=['POST'])
def schedule_delivery():
    order_id = request.form.get('order_id')
    warehouse_location_id = request.form.get('warehouse_location_id')
    shipment_date = datetime.now()
    delivery_date = shipment_date + timedelta(days=3)  # Assume delivery within 3 days

    # Insert a new shipment record
    db.session.execute(text("""
        INSERT INTO Shipment_Logistics (Customer_order_ID, Warehouse_Location_ID, Shipment_status, Shipment_date, Delivery_date)
        VALUES (:order_id, :warehouse_location_id, 'Scheduled', :shipment_date, :delivery_date)
    """), {'order_id': order_id, 'warehouse_location_id': warehouse_location_id, 'shipment_date': shipment_date, 'delivery_date': delivery_date})
    db.session.commit()

    flash('Delivery scheduled successfully!', 'success')
    return redirect(url_for('routes.logistics_dashboard'))
