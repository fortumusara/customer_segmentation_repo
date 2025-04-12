# snowflake_loader/load_to_snowflake.py

import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# Snowflake connection config
conn = snowflake.connector.connect(
    user='YOUR_USERNAME',
    password='YOUR_PASSWORD',
    account='YOUR_ACCOUNT_ID',
    warehouse='YOUR_WAREHOUSE',
    database='CUSTOMER_DB',
    schema='PUBLIC'
)

# Example data (you would load this from a Spark output or local file)
data = {
    'customer_id': ['C001', 'C002'],
    'total_spent': [125.5, 87.0],
    'category': ['grocery', 'travel'],
    'timestamp': ['2025-04-11T08:00:00Z', '2025-04-11T08:01:00Z']
}
df = pd.DataFrame(data)

# Ensure destination table exists
conn.cursor().execute("""
CREATE TABLE IF NOT EXISTS CUSTOMER_SPEND (
    customer_id STRING,
    total_spent FLOAT,
    category STRING,
    timestamp TIMESTAMP
)
""")

# Load the DataFrame into Snowflake
success, nchunks, nrows, _ = write_pandas(conn, df, 'CUSTOMER_SPEND')
print(f"✅ Loaded {nrows} rows into Snowflake.")
