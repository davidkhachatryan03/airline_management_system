USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE positions;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO positions (description) VALUES
("Captain"),
("First Officer"),
("Cabin Crew"),
("Cabin Manager"),
("Maintenance Technician"),
("Aeronautical Engineer"),
("Ground Agent"),
("Ground Manager"),
("Tester")