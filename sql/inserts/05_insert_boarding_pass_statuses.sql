USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE boardig_pass_stasuses;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO boardig_pass_stasuses (description) VALUES
("Issued"),
("No Show"),
("Denegated"),
("Boarded")