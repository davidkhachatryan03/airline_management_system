USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE sale_stasuses;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO sale_stasuses (description) VALUES
("Paid"),
("Refunded"),
("Booked"),
("Fraud Detected")