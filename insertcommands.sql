

-- Assuming Product_ID is set as AUTO_INCREMENT and PRIMARY KEY
INSERT INTO Product (Product_name, Category, Price) VALUES
('Smartphone X', 'Electronics', 999.90),
('Agricultural Tractor', 'Agricultural Products', 50000.00),
('Office Desk', 'Furniture', 150.00),
('Industrial Drill', 'Industrial Supplies', 1200.00),
('Couch', 'Furniture', 500.00),
('Laptop Pro', 'Electronics', 1500.00),
('Compact Car', 'Automotive', 20000.00),
('Concrete Mix', 'Construction Materials', 100.00),
('Pain Reliever', 'Pharmaceuticals', 20.00),
('Steel Beams', 'Construction Materials', 300.00),
('Vacuum Cleaner', 'Consumer Goods', 250.00),
('Table Saw', 'Industrial Supplies', 850.00),
('Organic Fertilizer', 'Agricultural Products', 30.00),
('Office Chair', 'Furniture', 80.00),
('Refrigerator', 'Consumer Goods', 1200.00),
('Heavy Duty Truck', 'Automotive', 75000.00),
('Packing Tape', 'Packaging', 5.00),
('Tablet Device', 'Electronics', 300.00),
('Air Conditioner', 'Consumer Goods', 800.00),
('Medical Syringe Pack', 'Pharmaceuticals', 15.00),
('Safety Helmet', 'Industrial Supplies', 50.00),
('Wooden Cabinet', 'Furniture', 600.00),
('Rice Seeds', 'Agricultural Products', 10.00),
('Plastic Wrap', 'Packaging', 12.00),
('Bulldozer', 'Construction Materials', 120000.00),
('Sofa Set', 'Furniture', 900.00),
('Electric Drill', 'Industrial Supplies', 100.00),
('Luxury Sedan', 'Automotive', 45000.00),
('Tablet Stand', 'Consumer Goods', 25.00),
('LED Monitor', 'Electronics', 200.00);





INSERT INTO Inventory (Stock_level, Supplier_ID, Location_ID, Product_ID, Reorder_point) VALUES
(37, 1, 1, 1, 10),
(15, 3, 1, 2, 5),
(28, 1, 2, 3, 25),
(30, 2, 3, 4, 10),
(40, 1, 1, 5, 15),
(80, 7, 1, 11, 10),
(80, 7, 2, 12, 10),
(90, 6, 4, 9, 8);

INSERT INTO Inventory (Stock_level, Supplier_ID, Location_ID, Product_ID, Reorder_point) VALUES
(55, 2, 3, 6, 15),   -- Additional product
(120, 4, 5, 7, 20),  -- Additional product
(65, 1, 2, 8, 10),   -- Additional product
(50, 3, 1, 9, 8),    -- Additional product
(75, 5, 4, 10, 12),  -- Additional product
(95, 6, 2, 13, 18),  -- Additional product
(30, 4, 3, 14, 6),   -- Additional product
(60, 2, 5, 15, 25),  -- Additional product
(45, 3, 1, 16, 7),   -- Additional product
(85, 7, 2, 17, 15),  -- Additional product
(40, 5, 4, 18, 9),   -- Additional product
(70, 6, 3, 19, 20),  -- Additional product
(100, 4, 1, 20, 30), -- Additional product
(95, 7, 5, 21, 10),  -- Additional product
(30, 2, 4, 22, 5);   -- Additional product




-- Insert data into Customer_Order table with stock-aware quantities
INSERT INTO Customer_Order (Order_date, Status, Total_amount, Customer_ID, Product_ID, Quantity) VALUES
('2024-10-15 10:08:30', 'Pending', 999.99, 1, 1, 2),         -- Product_ID 1, Stock: 37
('2024-10-15 10:08:30', 'Shipped', 50000.00, 2, 2, 1),       -- Product_ID 2, Stock: 15
('2024-10-15 10:08:30', 'Delivered', 150.00, 3, 3, 1),       -- Product_ID 3, Stock: 28
('2024-10-24 00:00:00', 'Pending', 3999.96, 4, 1, 4),        -- Product_ID 1
('2024-10-28 00:00:00', 'Pending', 300000.00, 5, 2, 6),      -- Product_ID 2
('2024-10-28 00:00:00', 'Pending', 2999.97, 5, 1, 3),        -- Product_ID 1
('2024-10-30 18:09:19', 'Pending', 999.99, 1, 1, 2),         -- Product_ID 1
('2024-10-30 18:09:19', 'Shipped', 50000.00, 2, 2, 1),       -- Product_ID 2
('2024-10-30 18:09:19', 'Delivered', 150.00, 3, 3, 1),       -- Product_ID 3
('2024-10-30 13:41:17', 'Pending', 1999.98, 5, 1, 2),        -- Product_ID 1
('2024-10-31 05:41:05', 'Pending', 2999.97, 6, 1, 3),        -- Product_ID 1
('2024-10-31 05:42:27', 'Pending', 2999.97, 7, 1, 3),        -- Product_ID 1
('2024-10-31 05:42:40', 'Pending', 100000.00, 7, 2, 2),      -- Product_ID 2
('2024-10-31 05:52:32', 'Pending', 999.99, 7, 1, 1),         -- Product_ID 1
('2024-10-31 05:57:46', 'Pending', 7500.00, 7, 3, 5),        -- Product_ID 3, adjusted to not exceed stock
('2024-10-31 05:58:23', 'Pending', 4050.00, 7, 3, 10),       -- Product_ID 3, adjusted to not exceed stock
('2024-11-03 15:53:27', 'Pending', 9999.90, 9, 1, 10),       -- Product_ID 1
('2024-11-05 04:19:38', 'Pending', 50000.00, 9, 2, 1),       -- Product_ID 2
('2024-11-07 03:41:16', 'Pending', 100000.00, 9, 2, 2),      -- Product_ID 2
('2024-11-07 05:44:00', 'Pending', 999.99, 10, 1, 1),        -- Product_ID 1
('2024-11-07 12:54:37', 'Pending', 150.00, 1, 3, 1),         -- Product_ID 3
('2024-11-10 14:31:39', 'Pending', 1999.80, 17, 1, 2),       -- Product_ID 1
('2024-11-10 14:31:49', 'Pending', 100000.00, 17, 2, 2);     -- Product_ID 2



-- Insert missing Product_IDs into the Inventory table
INSERT INTO Inventory (Stock_level, Supplier_ID, Location_ID, Product_ID, Reorder_point) VALUES
(100, 1, 1, 24, 10),  -- Product_ID 24, Stock_level = 100
(150, 3, 2, 25, 5),   -- Product_ID 25, Stock_level = 150
(200, 4, 3, 26, 20),  -- Product_ID 26, Stock_level = 200
(50, 2, 4, 27, 15),   -- Product_ID 27, Stock_level = 50
(300, 6, 5, 28, 30),  -- Product_ID 28, Stock_level = 300
(120, 5, 1, 29, 25),  -- Product_ID 29, Stock_level = 120
(80, 7, 2, 30, 20);   -- Product_ID 30, Stock_level = 80
