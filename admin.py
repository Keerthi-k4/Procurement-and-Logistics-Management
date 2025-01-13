from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from models import db
from models import Customer, Supplier, Product, Inventory, Location  # Import models

# Blueprint for admin
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin dashboard
@admin_bp.route('/')
def admin_dashboard():
    return render_template('admin/dashboard.html')


### Customer Management ###

@admin_bp.route('/customers')
def list_customers():
    customers = Customer.query.all()
    return render_template('admin/customers.html', customers=customers)


from werkzeug.security import generate_password_hash


@admin_bp.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']

        # Use pbkdf2:sha256 as the hashing method
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Corrected hashing method

        new_customer = Customer(Customer_name=name, Phone_no=phone, Email=email, Address=address, Password=hashed_password)
        db.session.add(new_customer)
        db.session.commit()
        flash("Customer added successfully.", "success")
        return redirect(url_for('admin.list_customers'))

    return render_template('admin/add_customer.html')


@admin_bp.route('/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == 'POST':
        customer.Customer_name = request.form['name']
        customer.Phone_no = request.form['phone']
        customer.Email = request.form['email']
        customer.Address = request.form['address']
        if request.form['password']:
            customer.Password = generate_password_hash(request.form['password'], method='sha256')
        db.session.commit()
        flash("Customer updated successfully.", "success")
        return redirect(url_for('admin.list_customers'))
    return render_template('admin/edit_customer.html', customer=customer)

@admin_bp.route('/customers/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash("Customer deleted successfully.", "success")
    return redirect(url_for('admin.list_customers'))


### Supplier Management ###

@admin_bp.route('/suppliers')
def list_suppliers():
    suppliers = Supplier.query.all()
    return render_template('admin/suppliers.html', suppliers=suppliers)


@admin_bp.route('/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        # Use pbkdf2:sha256 as the hashing method
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Corrected hashing method

        new_supplier = Supplier(Supplier_name=name, Phone_no=phone, Email=email, Password=hashed_password)
        db.session.add(new_supplier)
        db.session.commit()
        flash("Supplier added successfully.", "success")
        return redirect(url_for('admin.list_suppliers'))

    return render_template('admin/add_supplier.html')

@admin_bp.route('/suppliers/edit/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    if request.method == 'POST':
        supplier.Supplier_name = request.form['name']
        supplier.Phone_no = request.form['phone']
        supplier.Email = request.form['email']
        if request.form['password']:
            supplier.Password = generate_password_hash(request.form['password'], method='sha256')
        db.session.commit()
        flash("Supplier updated successfully.", "success")
        return redirect(url_for('admin.list_suppliers'))
    return render_template('admin/edit_supplier.html', supplier=supplier)

@admin_bp.route('/suppliers/delete/<int:supplier_id>', methods=['POST'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    flash("Supplier deleted successfully.", "success")
    return redirect(url_for('admin.list_suppliers'))


### Product Management ###

@admin_bp.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category = request.form['category']

        new_product = Product(Product_name=name, Price=price, Category=category)
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully.", "success")
        return redirect(url_for('admin.list_products'))
    return render_template('admin/add_product.html')

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.Product_name = request.form['name']
        product.Price = request.form['price']
        product.Category = request.form['category']
        db.session.commit()
        flash("Product updated successfully.", "success")
        return redirect(url_for('admin.list_products'))
    return render_template('admin/edit_product.html', product=product)

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully.", "success")
    return redirect(url_for('admin.list_products'))


### Inventory Management ###

@admin_bp.route('/inventory')
def list_inventory():
    inventory_items = Inventory.query.all()
    return render_template('admin/inventory.html', inventory_items=inventory_items)

@admin_bp.route('/inventory/add', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        stock_level = request.form['stock_level']
        reorder_point = request.form['reorder_point']
        product_id = request.form['product_id']
        supplier_id = request.form['supplier_id']
        location_id = request.form['location_id']

        new_inventory = Inventory(Stock_level=stock_level, Reorder_point=reorder_point,
                                  Product_ID=product_id, Supplier_ID=supplier_id, Location_ID=location_id)
        db.session.add(new_inventory)
        db.session.commit()
        flash("Inventory item added successfully.", "success")
        return redirect(url_for('admin.list_inventory'))
    products = Product.query.all()
    suppliers = Supplier.query.all()
    locations = Location.query.all()
    return render_template('admin/add_inventory.html', products=products, suppliers=suppliers, locations=locations)

@admin_bp.route('/inventory/edit/<int:inventory_id>', methods=['GET', 'POST'])
def edit_inventory(inventory_id):
    inventory = Inventory.query.get_or_404(inventory_id)
    if request.method == 'POST':
        inventory.Stock_level = request.form['stock_level']
        inventory.Reorder_point = request.form['reorder_point']
        inventory.Product_ID = request.form['product_id']
        inventory.Supplier_ID = request.form['supplier_id']
        inventory.Location_ID = request.form['location_id']
        db.session.commit()
        flash("Inventory item updated successfully.", "success")
        return redirect(url_for('admin.list_inventory'))
    products = Product.query.all()
    suppliers = Supplier.query.all()
    locations = Location.query.all()
    return render_template('admin/edit_inventory.html', inventory=inventory, products=products, suppliers=suppliers, locations=locations)

@admin_bp.route('/inventory/delete/<int:inventory_id>', methods=['POST'])
def delete_inventory(inventory_id):
    inventory = Inventory.query.get_or_404(inventory_id)
    db.session.delete(inventory)
    db.session.commit()
    flash("Inventory item deleted successfully.", "success")
    return redirect(url_for('admin.list_inventory'))
