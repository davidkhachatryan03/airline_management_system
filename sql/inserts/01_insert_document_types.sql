USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE document_types;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO document_types (description) VALUES
("National ID Card"),
("Passport"),
("VISA")