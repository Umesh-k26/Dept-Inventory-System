DROP DATABASE IF EXISTS Inventory;
CREATE DATABASE Inventory;
\c inventory;
DROP TABLE IF EXISTS users, order_table, asset, bulk_asset;
CREATE TABLE users (
    user_id VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    gmail VARCHAR(255),
    user_type VARCHAR(255),
    department VARCHAR(255),
    PRIMARY KEY (user_id)
);

CREATE TABLE order_table(
    purchace_order_no VARCHAR(255) UNIQUE,
    order_date DATE,
    indentor VARCHAR(255),
    firm_name TEXT,
    financial_year SMALLINT,
    quantity INT,
    unit_price FLOAT,
    gst_tin INT,
    final_procurement_date DATE,
    invoice_no VARCHAR(255) UNIQUE,
    invoice_date DATE,
    PRIMARY KEY (purchace_order_no, invoice_no),
    FOREIGN KEY (indentor) REFERENCES users (user_id)
);

CREATE TABLE asset(
    asset_name VARCHAR(255),
    model VARCHAR(255),
    serial_no VARCHAR(255),
    department VARCHAR(255),
    asset_location VARCHAR(255),
    asset_holder VARCHAR(255),
    entry_date DATE,
    warranty DATE,
    is_hardware BOOLEAN,
    system_no VARCHAR(255),
    purchace_order_no VARCHAR(255),
    asset_state VARCHAR(255),
    picture BYTEA,
    PRIMARY KEY (serial_no),
    FOREIGN KEY (asset_holder) REFERENCES users (user_id),
    FOREIGN KEY (purchace_order_no) REFERENCES order_table (purchace_order_no)
);

CREATE TABLE bulk_asset(
    asset_name VARCHAR(255),
    model VARCHAR(255),
    department VARCHAR(255),
    asset_location VARCHAR(255),
    entry_date DATE,
    quantity INT,
    purchace_order_no VARCHAR(255),
    picture BYTEA,
    asset_state VARCHAR(255),
    FOREIGN KEY (purchace_order_no) REFERENCES order_table (purchace_order_no)
);