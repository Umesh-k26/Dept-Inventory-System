DROP DATABASE IF EXISTS Inventory;
CREATE DATABASE Inventory;

\c inventory;

DROP TABLE IF EXISTS users, order_table, asset, bulk_asset;
CREATE TABLE users (
    user_id VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    user_type VARCHAR(255),
    department VARCHAR(255),
    user_state VARCHAR(255) DEFAULT 'Active',
    PRIMARY KEY (user_id)
);

CREATE TABLE order_table(
    purchase_order_no VARCHAR(255) NOT NULL UNIQUE,
    order_date DATE,
    indentor VARCHAR(255),
    firm_name TEXT,
    financial_year SMALLINT,
    -- quantity INT,
    gst_tin VARCHAR(255),
    final_procurement_date DATE,
    invoice_no VARCHAR(255) NOT NULL UNIQUE,
    invoice_date DATE,
    PRIMARY KEY (purchase_order_no, invoice_no),
    FOREIGN KEY (indentor) REFERENCES users (user_id)
);

CREATE TABLE asset(
    asset_name VARCHAR(255),
    model VARCHAR(255),
    serial_no VARCHAR(255) NOT NULL UNIQUE,
    department VARCHAR(255),
    asset_location VARCHAR(255),
    asset_holder VARCHAR(255),
    entry_date DATE,
    unit_price FLOAT,
    warranty DATE,
    is_hardware BOOLEAN,
    system_no VARCHAR(255),
    purchase_order_no VARCHAR(255),
    asset_state VARCHAR(255),
    picture BYTEA,
    PRIMARY KEY (serial_no),
    FOREIGN KEY (asset_holder) REFERENCES users (user_id),
    FOREIGN KEY (purchase_order_no) REFERENCES order_table (purchase_order_no)
);

CREATE TABLE bulk_asset(
    asset_name VARCHAR(255),
    model VARCHAR(255),
    department VARCHAR(255),
    asset_location VARCHAR(255),
    entry_date DATE,
    quantity INT,
    purchase_order_no VARCHAR(255),
    asset_state VARCHAR(255),
    picture BYTEA,
    FOREIGN KEY (purchase_order_no) REFERENCES order_table (purchase_order_no)
);