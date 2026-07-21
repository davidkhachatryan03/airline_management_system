DROP DATABASE IF EXISTS airline;
CREATE DATABASE airline CHARACTER SET utf8mb4;

USE airline;

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