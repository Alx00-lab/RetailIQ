-- Client's Table
CREATE TABLE dim_customers (
	customer_unique_id VARCHAR(40) PRIMARY KEY,
    customer_id VARCHAR(40),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100), 
    customer_state NVARCHAR(10) 
);

-- Product's Table
CREATE TABLE dim_products (
    product_id VARCHAR(40) PRIMARY KEY,
    product_category_name NVARCHAR(100),
    product_name_lenght DECIMAL(10,2),
    product_description_lenght DECIMAL(10,2),
    product_photos_qty INT,
    product_weight_g DECIMAL(10,2),
    product_length_cm DECIMAL(10,2),
    product_height_cm DECIMAL(10,2),
    product_width_cm DECIMAL(10,2)
);


CREATE TABLE dim_orders (
    order_id VARCHAR(40) PRIMARY KEY,
    customer_unique_id VARCHAR(40),
    order_status NVARCHAR(20),
    order_purchase_timestamp DATETIME2,
    order_approved_at DATETIME2,
    order_delivered_carrier_date DATETIME2,
    order_delivered_customer_date DATETIME2,
    order_estimated_delivery_date DATETIME2

    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_unique_id)
        REFERENCES dim_customers(customer_unique_id)
);



-- dim_order_items's Table - now fact table due has all value to be it.
CREATE TABLE dim_order_items (
    order_id VARCHAR(40),
    order_item_id INT,
    product_id VARCHAR(40),
    seller_id VARCHAR(40),
    shipping_limit_date DATETIME2,
    price DECIMAL,
    freight_value DECIMAL

    CONSTRAINT pk_order_items PRIMARY KEY (order_id, order_item_id),
    CONSTRAINT fk_order_items_order FOREIGN KEY (order_id)
        REFERENCES dim_orders(order_id),
    CONSTRAINT fk_order_items_product FOREIGN KEY (product_id)
        REFERENCES dim_products(product_id)
);






