-- Customers
CREATE TABLE dim_customers (
    customer_unique_id   VARCHAR(40) PRIMARY KEY,
    customer_id          VARCHAR(40),
    customer_zip_code_prefix INT,
    customer_city        VARCHAR(100),
    customer_state       NVARCHAR(10)
);

-- Products
CREATE TABLE dim_products (
    product_id                   VARCHAR(40) PRIMARY KEY,
    product_category_name        NVARCHAR(100),
    product_name_lenght          DECIMAL(10,2),
    product_description_lenght   DECIMAL(10,2),
    product_photos_qty           INT,
    product_weight_g             DECIMAL(10,2),
    product_length_cm            DECIMAL(10,2),
    product_height_cm            DECIMAL(10,2),
    product_width_cm             DECIMAL(10,2)
);

-- Date
CREATE TABLE dim_date (
    DateKey    INT PRIMARY KEY,
    FullDate   DATE,
    Year       INT,
    Month      INT,
    MonthName  NVARCHAR(20),
    Quarter    INT
);

-- Orders
CREATE TABLE dim_orders (
    order_id                      VARCHAR(40) PRIMARY KEY,
    order_status                  NVARCHAR(20),
    order_purchase_timestamp      DATETIME2,
    order_approved_at             DATETIME2,
    order_delivered_carrier_date  DATETIME2,
    order_delivered_customer_date DATETIME2,
    order_estimated_delivery_date DATETIME2,            
);

-- Fact table
CREATE TABLE fact_order_items (
    order_id            VARCHAR(40),
    order_item_id       INT,
    product_id          VARCHAR(40),
    customer_unique_id  VARCHAR(40),
    DateKey             INT,        
    seller_id           VARCHAR(40),
    price               DECIMAL(10,2),
    freight_value       DECIMAL(10,2),
    total_order_value   DECIMAL(10,2),
    delivery_days       INT,
    shipping_limit_date DATETIME2,               
                     
    CONSTRAINT pk_order_items PRIMARY KEY (order_id, order_item_id),
    CONSTRAINT fk_fact_product FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
    CONSTRAINT fk_fact_customer FOREIGN KEY (customer_unique_id) REFERENCES dim_customers(customer_unique_id),
    CONSTRAINT fk_fact_date FOREIGN KEY (DateKey) REFERENCES dim_date(DateKey),
    CONSTRAINT fk_fact_order FOREIGN KEY (order_id) REFERENCES dim_orders(order_id)
   
);













