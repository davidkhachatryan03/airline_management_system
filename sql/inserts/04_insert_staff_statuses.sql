USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE staff_stasuses;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO staff_stasuses (description) VALUES
("Active"),
("On Leave"),
("Inactive"),
("On Vacation")