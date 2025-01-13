-- Create Customer table
CREATE TABLE Customer (
    Customer_ID INT PRIMARY KEY AUTO_INCREMENT,
    Customer_name VARCHAR(100),
    Phone_no VARCHAR(15),
    Email VARCHAR(100),
    Address VARCHAR(100)
);

-- Create Supplier table
CREATE TABLE Supplier (
    Supplier_ID INT PRIMARY KEY AUTO_INCREMENT,
    Supplier_name VARCHAR(100),
    Phone_no VARCHAR(15),
    Email VARCHAR(100)
);

-- Create Location table
CREATE TABLE Location (
    Location_ID INT PRIMARY KEY AUTO_INCREMENT,
    Location_name VARCHAR(100),
    Location_address VARCHAR(255)
);

-- Create Product table
CREATE TABLE Product (
    Product_ID INT PRIMARY KEY AUTO_INCREMENT,
    Product_name VARCHAR(100),
    Category ENUM('Consumer Goods', 'Electronics', 'Automotive', 'Industrial Supplies', 'Pharmaceuticals', 'Construction Materials', 'Furniture', 'Packaging', 'Agricultural Products', 'Others')
);

-- Create Inventory table with Product_ID
CREATE TABLE Inventory (
    Inventory_ID INT PRIMARY KEY AUTO_INCREMENT,
    Stock_level INT,
    Supplier_ID INT,
    Location_ID INT,
    Product_ID INT,
    Reorder_point INT,
    FOREIGN KEY (Supplier_ID) REFERENCES Supplier(Supplier_ID),
    FOREIGN KEY (Location_ID) REFERENCES Location(Location_ID),
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
);

-- Create Customer_Order table
CREATE TABLE Customer_Order (
    Customer_order_ID INT PRIMARY KEY AUTO_INCREMENT,
    Order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Use TIMESTAMP for date and time
    Status VARCHAR(50),
    Total_amount DECIMAL(10, 2),
    Customer_ID INT,
    Product_ID INT,
    Quantity INT,
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
);


-- Create Shipment_Logistics table
CREATE TABLE Shipment_Logistics (
    Shipment_ID INT PRIMARY KEY AUTO_INCREMENT,
    Shipment_status VARCHAR(50),
    Shipment_route VARCHAR(255),
    Delivery_date DATE,
    Warehouse_Location_ID INT,
    Customer_order_ID INT,
    FOREIGN KEY (Warehouse_Location_ID) REFERENCES Location(Location_ID),
    FOREIGN KEY (Customer_order_ID) REFERENCES Customer_Order(Customer_order_ID)
);

-- Create Procurement table
CREATE TABLE Procurement (
    Procurement_ID INT PRIMARY KEY AUTO_INCREMENT,
    Order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Expected_delivery_date DATE,
    Total_cost DECIMAL(10, 2),
    Supplier_ID INT,
    FOREIGN KEY (Supplier_ID) REFERENCES Supplier(Supplier_ID)
);

ALTER TABLE Customer
ADD COLUMN Password VARCHAR(255);
ALTER TABLE Product ADD COLUMN Price DECIMAL(10, 2);


ALTER TABLE Supplier ADD Password VARCHAR(255) NOT NULL;
