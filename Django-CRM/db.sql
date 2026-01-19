CREATE DATABASE IF NOT EXISTS django_crm
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE django_crm;

GRANT ALL PRIVILEGES ON django_crm.* TO 'root'@'localhost' IDENTIFIED BY 'MySQL@123';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS record (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) DEFAULT NULL,
    address VARCHAR(100) DEFAULT NULL,
    city VARCHAR(50) DEFAULT NULL,
    state VARCHAR(50) DEFAULT NULL,
    zipcode VARCHAR(20) DEFAULT NULL,

    -- Order-related fields
    product_id VARCHAR(50) DEFAULT NULL,
    order_day DATE DEFAULT NULL,
    delivered_date DATE DEFAULT NULL,
    customer_response TEXT DEFAULT NULL,

    status ENUM('Pending', 'Delivered', 'Cancelled') DEFAULT 'Pending',
    rating TINYINT UNSIGNED DEFAULT 0 CHECK (rating BETWEEN 0 AND 5)
);

DELIMITER $$

-- Prevent setting delivered_date if status ≠ 'Delivered'
CREATE TRIGGER trg_validate_delivery_date
BEFORE INSERT ON record
FOR EACH ROW
BEGIN
    IF NEW.status <> 'Delivered' AND NEW.delivered_date IS NOT NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Delivered date can only be set when status is Delivered.';
    END IF;

    IF NEW.status <> 'Delivered' AND NEW.rating > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Rating can only be given after delivery.';
    END IF;

    IF NEW.rating < 0 OR NEW.rating > 5 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Rating must be between 0 and 5.';
    END IF;
END$$

-- Ensure the same rules during UPDATE
CREATE TRIGGER trg_validate_delivery_date_update
BEFORE UPDATE ON record
FOR EACH ROW
BEGIN
    IF NEW.status <> 'Delivered' AND NEW.delivered_date IS NOT NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Delivered date can only be set when status is Delivered.';
    END IF;

    IF NEW.status <> 'Delivered' AND NEW.rating > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Rating can only be given after delivery.';
    END IF;

    IF NEW.rating < 0 OR NEW.rating > 5 THEN
        SET NEW.rating = 0;
    END IF;
END$$

DELIMITER ;

SHOW TABLES;
