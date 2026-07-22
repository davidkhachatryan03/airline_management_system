CREATE TABLE routes (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    flight_number CHAR(6) UNIQUE NOT NULL,
    origin CHAR(3) NOT NULL,
    destination CHAR(3) NOT NULL,
    distance_km INT UNSIGNED NOT NULL,
    duration_min SMALLINT UNSIGNED NOT NULL
);

CREATE TABLE passengers (
	id BINARY(16) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    is_blacklisted BOOLEAN NOT NULL,
    is_vip BOOLEAN NOT NULL
); 

CREATE TABLE booking_statuses (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE flight_statuses (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE airplane_statuses (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE positions (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	description VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE staff_statuses (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE boarding_pass_statuses (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE document_types (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE roles (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	description VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE ticket_statuses (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE documents (
	id BINARY(16) PRIMARY KEY,
    document_number VARCHAR(20) NOT NULL,
    valid_from DATE NOT NULL,
    valid_until DATE NOT NULL,
    issue_country CHAR(3) NOT NULL,
    passenger_id BINARY(16) NOT NULL,
    document_type_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (passenger_id) REFERENCES passengers(id),
    FOREIGN KEY (document_type_id) REFERENCES document_types(id),
    UNIQUE (document_number, issue_country)
);

CREATE TABLE airplanes (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tail_number VARCHAR(10) UNIQUE NOT NULL,
    manufacturer VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    capacity SMALLINT UNSIGNED NOT NULL,
    range_km SMALLINT UNSIGNED NOT NULL,
    flight_hour_cost_usd DECIMAL(10,2) NOT NULL,
    current_status_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (current_status_id) REFERENCES airplane_statuses(id)
);

CREATE TABLE scheduled_maintenances (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(100) NOT NULL,
    scheduled_start_datetime DATETIME NOT NULL,
    scheduled_end_datetime DATETIME NOT NULL,
    actual_start_datetime DATETIME NOT NULL,
    actual_end_datetime DATETIME NOT NULL,
    airplane_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (airplane_id) REFERENCES airplanes(id)
);

CREATE TABLE flights (
	id BINARY(16) PRIMARY KEY,
    scheduled_departure_datetime DATETIME NOT NULL,
    scheduled_arrival_datetime DATETIME NOT NULL,
    actual_departure_datetime DATETIME,
    actual_arrival_datetime DATETIME,
    operating_cost_usd DECIMAL(10,2) NOT NULL,
    base_price_usd DECIMAL(10,2) NOT NULL,
    current_status_id INT UNSIGNED NOT NULL,
    route_id INT UNSIGNED NOT NULL,
    airplane_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (current_status_id) REFERENCES flight_statuses(id),
    FOREIGN KEY (route_id) REFERENCES routes(id),
    FOREIGN KEY (airplane_id) REFERENCES airplanes(id),
    UNIQUE (scheduled_departure_datetime, route_id)
);

CREATE TABLE staff (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) UNIQUE NOT NULL,
    current_status_id INT UNSIGNED NOT NULL,
    current_position_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (current_status_id) REFERENCES staff_statuses(id),
    FOREIGN KEY (current_position_id) REFERENCES positions(id)
);

CREATE TABLE maintenance_assignments (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    staff_id INT UNSIGNED NOT NULL,
    maintenance_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES staff(id),
    FOREIGN KEY (maintenance_id) REFERENCES scheduled_maintenances(id)
);

CREATE TABLE crew_assignments (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    role_id INT UNSIGNED NOT NULL,
    flight_id BINARY(16) NOT NULL,
    staff_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (flight_id) REFERENCES flights(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id),
    UNIQUE (flight_id, staff_id),
    UNIQUE (start_time, staff_id)
);

CREATE TABLE bookings (
	id BINARY(16) PRIMARY KEY,
    booking_reference VARCHAR(6) UNIQUE NOT NULL,
    booking_datetime DATETIME NOT NULL,
    paid_amount_usd DECIMAL(10,2) NOT NULL,
    current_status_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (current_status_id) REFERENCES booking_statuses(id)
);

CREATE TABLE tickets (
	id BINARY(16) PRIMARY KEY,
    ticket_number CHAR(13) UNIQUE NOT NULL,
    paid_amount_usd DECIMAL(10,2) NOT NULL,
    current_status_id INT UNSIGNED NOT NULL,
    booking_id BINARY(16) NOT NULL,
    flight_id BINARY(16) NOT NULL,
    passenger_id BINARY(16) NOT NULL,
    FOREIGN KEY (current_status_id) REFERENCES ticket_statuses(id),
    FOREIGN KEY (booking_id) REFERENCES bookings(id),
    FOREIGN KEY (flight_id) REFERENCES flights(id),
    FOREIGN KEY (passenger_id) REFERENCES passengers(id)
);

CREATE TABLE boarding_passes (
	id BINARY(16) PRIMARY KEY,
    issue_datetime DATETIME,
    boarding_datetime DATETIME DEFAULT NULL,
    current_status_id INT UNSIGNED NOT NULL,
    ticket_id BINARY(16) UNIQUE NOT NULL,
    FOREIGN KEY (current_status_id) REFERENCES boarding_pass_statuses(id),
	FOREIGN KEY (ticket_id) REFERENCES tickets(id)
);

CREATE TABLE staff_certifications (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(100) NOT NULL,
    valid_from DATE NOT NULL,
    valid_until DATE NOT NULL,
    staff_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES staff(id),
    UNIQUE (description, staff_id)
);

CREATE TABLE audit_logs (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    action VARCHAR(100) NOT NULL,
    record_id VARCHAR(50),
    column_name VARCHAR(100),
    old_value VARCHAR(100),
    new_value VARCHAR(100),
    changed_at DATETIME NOT NULL,
    changed_by_staff_id INT UNSIGNED
);

INSERT INTO document_types (description) VALUES
("National ID Card"),
("Passport"),
("VISA");

INSERT INTO positions (description) VALUES
("Captain"),
("First Officer"),
("Cabin Crew"),
("Cabin Manager"),
("Maintenance Technician"),
("Aeronautical Engineer"),
("Ground Agent"),
("Ground Manager"),
("Tester");

INSERT INTO airplane_statuses (description) VALUES 
("Active"),
("Inactive"),
("Retired");

INSERT INTO staff_statuses (description) VALUES
("Active"),
("On Leave"),
("Inactive"),
("On Vacation");

INSERT INTO boarding_pass_statuses (description) VALUES
("Issued"),
("No Show"),
("Denegated"),
("Boarded");

INSERT INTO booking_statuses (description) VALUES
("Paid"),
("Refunded"),
("Booked"),
("Fraud Detected");

INSERT INTO flight_statuses (description) VALUES 
("Scheduled"),
("In Flight"),
("Landed"),
("Cancelled");

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
("Aeronautical Engineer");

INSERT INTO routes (flight_number, origin, destination, distance_km, duration_min) VALUES 
    ('AR1240', 'AEP', 'COR', 646, 85),
    ('AR1241', 'COR', 'AEP', 646, 85),
    ('AR1432', 'AEP', 'MDZ', 984, 110),
    ('AR1433', 'MDZ', 'AEP', 984, 110),
    ('AR1870', 'AEP', 'BRC', 1316, 140),
    ('AR1871', 'BRC', 'AEP', 1316, 140),
    ('AR2840', 'AEP', 'USH', 2380, 215),
    ('AR2841', 'USH', 'AEP', 2380, 215),
    ('AR1530', 'AEP', 'IGR', 1050, 105),
    ('AR1531', 'IGR', 'AEP', 1050, 105),
    ('LA2350', 'SCL', 'AEP', 1140, 130),
    ('LA2351', 'AEP', 'SCL', 1140, 130),
    ('LA3122', 'AEP', 'GRU', 1700, 165),
    ('LA3123', 'GRU', 'AEP', 1700, 165),
    ('LA4500', 'LIM', 'AEP', 3150, 245),
    ('LA4501', 'AEP', 'LIM', 3150, 245),
    ('AV9340', 'BOG', 'AEP', 4600, 370),
    ('AV9341', 'AEP', 'BOG', 4600, 370),
    ('AF7652', 'GIG', 'AEP', 1980, 190),
    ('AF7653', 'AEP', 'GIG', 1980, 190),
    ('AA1142', 'MIA', 'AEP', 7100, 540),
    ('AA1143', 'AEP', 'MIA', 7100, 540),
    ('IB3106', 'AEP', 'MAD', 10050, 750),
    ('IB3107', 'MAD', 'AEP', 10050, 750),
    ('LH0120', 'FRA', 'AEP', 11500, 820),
    ('LH0121', 'AEP', 'FRA', 11500, 820),
    ('AM0120', 'MEX', 'AEP', 7400, 580),
    ('AM0121', 'AEP', 'MEX', 7400, 580),
    ('AF0412', 'AEP', 'CDG', 11100, 790),
    ('AF0413', 'CDG', 'AEP', 11100, 790);

INSERT INTO airplanes (tail_number, manufacturer, model, capacity, range_km, flight_hour_cost_usd, current_status_id) VALUES 
('LV-GLF', 'Gulfstream', 'G650ER', 18, 13890, 15500.00, 1),
('N-750GL', 'Bombardier', 'Global 7500', 19, 14260, 16200.00, 1),
('LV-F8X', 'Dassault', 'Falcon 8X', 14, 11945, 14800.50, 1),
('LV-CIT', 'Cessna', 'Citation X+', 12, 6400, 9500.00, 1),
('N-350CH', 'Bombardier', 'Challenger 350', 9, 5900, 8700.00, 1),
('LV-CJ4', 'Cessna', 'Citation CJ4', 10, 4010, 5600.00, 1),
('LV-PHE', 'Embraer', 'Phenom 300E', 10, 3650, 5200.00, 1),
('N-LJ75', 'Learjet', '75 Liberty', 8, 3850, 5100.00, 1),
('LV-PIL', 'Pilatus', 'PC-24', 11, 3704, 4900.00, 1),
('LV-HND', 'Honda Aircraft', 'HondaJet Elite', 5, 2661, 3800.00, 1);

INSERT INTO staff (full_name, current_position_id, current_status_id) VALUES 
('Carlos Gómez', 1, 1),
('Lucía Benitez', 1, 1), 
('Ricardo Darín', 1, 2),
('Valeria Lynch', 1, 1),
('Mariana López', 2, 1),
('Esteban Quito', 2, 1),
('Julián Álvarez', 2, 3),
('Lionel Messi', 2, 1),
('Lali Espósito', 3, 1),
('Tini Stoessel', 7, 1),
('Fito Páez', 7, 2),
('Charly García', 7, 1),
('Marcelo Tinelli', 7, 1),
('Celeste Cid', 7, 1),
('Alejandro Ruiz', 8, 1),
('Mirtha Legrand', 8, 1),
('Roberto Fernández', 4, 2),  
('Gustavo Cerati', 4, 1),     
('Norberto Pappo', 4, 1),
('Sofía Martínez', 5, 1),    
('Diego Maradona', 5, 4),    
('Susana Giménez', 6, 1),
('Guillermo Francella', 6, 1),
('Elon Musk', 6, 1),
('Tester', 9, 1),
('Máximo Penacino', 3, 1);

INSERT INTO staff_certifications (description, valid_from, valid_until, staff_id) VALUES 
('Captain License', '2023-12-31', '2028-12-31', 1),
('Captain License', '2025-06-15', '2027-06-15', 2),
('Captain License', '2024-11-30', '2026-11-30', 3),
('Captain License', '2024-03-01', '2029-03-01', 4),
('First Officer License', '2026-05-20', '2028-05-20', 5),
('First Officer License', '2025-08-10', '2027-08-10', 6),
('First Officer License', '2024-10-15', '2026-10-15', 7),
('First Officer License', '2025-01-01', '2030-01-01', 8),
('Flight Attendant License', '2026-01-01', '2027-12-31', 9),
('Ground Agent License', '2025-03-15', '2027-03-15', 10),
('Ground Agent License', '2024-08-30', '2026-08-30', 11),
('Ground Agent License', '2026-01-01', '2028-01-01', 12),
('Ground Agent License', '2025-05-20', '2027-05-20', 13),
('Ground Agent License', '2024-12-10', '2026-12-10', 14),
('Ground Manager License', '2026-10-31', '2029-10-31', 15),
('Ground Manager License', '2025-02-28', '2028-02-28', 16),
('Cabin Manager License', '2026-06-30', '2028-06-30', 17),
('Cabin Manager License', '2025-04-15', '2027-04-15', 18),
('Cabin Manager License', '2024-09-20', '2026-09-20', 19),
('Maintenance License', '2021-12-31', '2031-12-31', 20),
('Maintenance License', '2024-07-10', '2029-07-10', 21),
('Aeronautical Engineering License', '2025-12-31', '2035-12-31', 22),
('Aeronautical Engineering License', '2020-11-01', '2030-11-01', 23),
('Aeronautical Engineering License', '2025-12-31', '2035-12-31', 24),
('Tester License', '2022-01-01', '2032-01-01', 25);

INSERT INTO ticket_statuses (description) VALUES
("Paid"),
("Refunded"),
("Booked"),
("Fraud Detected");