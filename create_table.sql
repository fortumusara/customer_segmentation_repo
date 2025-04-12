-- Staging Table for Raw Transactions
CREATE OR REPLACE TABLE RAW_TRANSACTIONS (
    transaction_id STRING,
    customer_id STRING,
    timestamp TIMESTAMP,
    amount FLOAT,
    merchant_category STRING
);

-- Final Segmented Customers Table
CREATE OR REPLACE TABLE SEGMENTED_CUSTOMERS (
    customer_id STRING,
    total_spent FLOAT,
    avg_transaction FLOAT,
    transaction_count INT,
    segment STRING
);
