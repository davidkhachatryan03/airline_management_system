USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE airplane_stasuses;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO airplane_stasuses (description) VALUES 
("Active"),
("Inactive"),
("Maintenance")