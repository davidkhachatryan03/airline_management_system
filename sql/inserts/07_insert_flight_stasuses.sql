USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE flight_stasuses;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO flight_stasuses (description) VALUES 
("Scheduled"),
("In Flight"),
("Landed"),
("Canelled")