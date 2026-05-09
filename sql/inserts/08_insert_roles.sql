USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE roles;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO roles (description) VALUES
("PIC"),
("SIC"),
("Cabin Crew"),
("Cabin Manager"),
("Check-In Agent"),
("Boarding Agent"),
("Groung Manager"),
("Maintenance Technician"),
("Hangar Technician"),
("Aeronautical Engineer"),
