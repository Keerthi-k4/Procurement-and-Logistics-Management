from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import datetime


db = SQLAlchemy()

# Model representing the Customer table in your MySQL database
class Customer(db.Model):
    __tablename__ = 'Customer'
    Customer_ID = db.Column(db.Integer, primary_key=True)
    Customer_name = db.Column(db.String(100), nullable=False)
    Phone_no = db.Column(db.String(15), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Address = db.Column(db.String(100))
    Password = db.Column(db.String(255), nullable=False)


    def __init__(self, Customer_name, Phone_no, Email, Address, Password):
        self.Customer_name = Customer_name
        self.Phone_no = Phone_no
        self.Email = Email
        self.Address = Address
        self.Password = Password

# Product Model
class Product(db.Model):
    __tablename__ = 'Product'
    Product_ID = db.Column(db.Integer, primary_key=True)
    Product_name = db.Column(db.String(100), nullable=False)
    Price = db.Column(db.Numeric(10, 2))
    Category = db.Column(db.Enum(
        'Consumer Goods', 'Electronics', 'Automotive', 'Industrial Supplies',
        'Pharmaceuticals', 'Construction Materials', 'Furniture',
        'Packaging', 'Agricultural Products', 'Others'))

# CustomerOrder Model
class CustomerOrder(db.Model):
    __tablename__ = 'Customer_Order'
    Customer_order_ID = db.Column(db.Integer, primary_key=True)
    Order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    Status = db.Column(db.String(50), nullable=False)
    Total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('Customer.Customer_ID'), nullable=False)
    Product_ID = db.Column(db.Integer, db.ForeignKey('Product.Product_ID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)

    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))

# Inventory Model
class Inventory(db.Model):
    __tablename__ = 'Inventory'
    Inventory_ID = db.Column(db.Integer, primary_key=True)
    Stock_level = db.Column(db.Integer, nullable=False)
    Reorder_point = db.Column(db.Integer, nullable=False)
    Product_ID = db.Column(db.Integer, db.ForeignKey('Product.Product_ID'), nullable=False)
    Supplier_ID = db.Column(db.Integer, db.ForeignKey('Supplier.Supplier_ID'), nullable=False)
    Location_ID = db.Column(db.Integer, db.ForeignKey('Location.Location_ID'), nullable=False)

    Product = db.relationship('Product', backref=db.backref('inventory_items', lazy=True))
    Supplier = db.relationship('Supplier', backref=db.backref('inventory_items', lazy=True))
    Location = db.relationship('Location', backref=db.backref('inventory_items', lazy=True))

class Procurement(db.Model):
    __tablename__ = 'Procurement'
    Procurement_ID = db.Column(db.Integer, primary_key=True)
    Order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    Expected_delivery_date = db.Column(db.Date)
    Total_cost = db.Column(db.Numeric(10, 2))
    Supplier_ID = db.Column(db.Integer, db.ForeignKey('Supplier.Supplier_ID'), nullable=False)

    supplier = db.relationship('Supplier', backref=db.backref('procurements', lazy=True))


# Supplier Model
class Supplier(db.Model):
    __tablename__ = 'Supplier'
    Supplier_ID = db.Column(db.Integer, primary_key=True)
    Supplier_name = db.Column(db.String(100), nullable=False)
    Phone_no = db.Column(db.String(15), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)  # Add Password field

    def __init__(self, Supplier_name, Phone_no, Email, Password):
        self.Supplier_name = Supplier_name
        self.Phone_no = Phone_no
        self.Email = Email
        self.Password = Password  # Assign the password


# Location Model
class Location(db.Model):
    __tablename__ = 'Location'
    Location_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Location_name = db.Column(db.String(100), nullable=False)
    Location_address = db.Column(db.String(255), nullable=True)

    def __init__(self, Location_name, Location_address=None):
        self.Location_name = Location_name
        self.Location_address = Location_address


# Shipment_Logistics Model
class ShipmentLogistics(db.Model):
    __tablename__ = 'Shipment_Logistics'
    Shipment_ID = db.Column(db.Integer, primary_key=True)
    Shipment_status = db.Column(db.String(50), nullable=False)
    Shipment_route = db.Column(db.String(255))
    Delivery_date = db.Column(db.Date)
    Warehouse_Location_ID = db.Column(db.Integer, db.ForeignKey('Location.Location_ID'), nullable=False)
    Customer_order_ID = db.Column(db.Integer, db.ForeignKey('Customer_Order.Customer_order_ID'), nullable=False)

    warehouse_location = db.relationship('Location', backref=db.backref('shipments', lazy=True))
    customer_order = db.relationship('CustomerOrder', backref=db.backref('shipment_logistics', lazy=True))
