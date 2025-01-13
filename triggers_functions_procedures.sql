DELIMITER //

CREATE PROCEDURE CheckLowStockItems()
BEGIN
    SELECT 
        i.Inventory_ID,
        i.Stock_level,
        i.Reorder_point,
        p.Product_name,
        l.Location_name
    FROM 
        Inventory i
    JOIN 
        Product p ON i.Product_ID = p.Product_ID
    JOIN 
        Location l ON i.Location_ID = l.Location_ID
    WHERE 
        i.Stock_level < i.Reorder_point;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE ViewInventory()
BEGIN
    SELECT 
        i.Inventory_ID,
        i.Stock_level,
        i.Reorder_point,
        p.Product_name,
        p.Price,
        l.Location_name
    FROM 
        Inventory i
    JOIN 
        Product p ON i.Product_ID = p.Product_ID
    JOIN 
        Location l ON i.Location_ID = l.Location_ID;
END //

DELIMITER ;


DELIMITER //

CREATE TRIGGER UpdateStockLevelAfterOrder
AFTER INSERT ON Customer_Order
FOR EACH ROW
BEGIN
    UPDATE Inventory
    SET Stock_level = Stock_level - NEW.Quantity
    WHERE Product_ID = NEW.Product_ID;
END//

DELIMITER ;

