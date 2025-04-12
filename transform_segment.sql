-- Transform and Segment Customers
MERGE INTO SEGMENTED_CUSTOMERS AS target
USING (
    SELECT 
        customer_id,
        SUM(amount) AS total_spent,
        AVG(amount) AS avg_transaction,
        COUNT(*) AS transaction_count,
        CASE 
            WHEN SUM(amount) > 1000 THEN 'High-Spender'
            WHEN COUNT(*) > 20 THEN 'Frequent-Spender'
            ELSE 'Low-Spender'
        END AS segment
    FROM RAW_TRANSACTIONS
    GROUP BY customer_id
) AS source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN 
    UPDATE SET 
        total_spent = source.total_spent,
        avg_transaction = source.avg_transaction,
        transaction_count = source.transaction_count,
        segment = source.segment
WHEN NOT MATCHED THEN 
    INSERT (customer_id, total_spent, avg_transaction, transaction_count, segment)
    VALUES (source.customer_id, source.total_spent, source.avg_transaction, source.transaction_count, source.segment);
