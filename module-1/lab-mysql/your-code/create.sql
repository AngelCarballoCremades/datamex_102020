USE lab_mysql;


CREATE TABLE cars(
    VIN VARCHAR(50) PRIMARY KEY,
    manufacturer VARCHAR(50) NOT NULL,
    model VARCHAR(50),
    year YEAR,
    color VARCHAR(50)
);

CREATE TABLE customers(
	customer_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(50),
    address VARCHAR(100),
    city VARCHAR(100),
    state_province VARCHAR(100),
    country VARCHAR(100),
    zip_postal MEDIUMINT
);

CREATE TABLE salespersons(
	staff_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    store VARCHAR(100) NOT NULL
);

CREATE TABLE invoices(
	invoice_id INT PRIMARY KEY,
    invoice_date DATE NOT NULL,
    car VARCHAR(50) NOT NULL,
    customer INT NOT NULL,
    salesperson INT NOT NULL,
    FOREIGN KEY (car) REFERENCES cars(VIN),
    FOREIGN KEY (customer) REFERENCES customers(customer_id),
    FOREIGN KEY (salesperson) REFERENCES salespersons(staff_id)
);