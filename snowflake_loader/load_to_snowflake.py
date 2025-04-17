import os
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Snowflake connection parameters
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT_ID")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")

# File paths
raw_transactions_path = '../spark_processing/output/raw_transactions'
segmented_customers_path = '../spark_processing/output/segmented_customers'

# Function to check if a Parquet file is empty
def is_parquet_empty(file_path):
    return os.path.getsize(file_path) == 0

# Function to establish Snowflake connection
def create_snowflake_connection():
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )


def map_columns(df, table_name):
    if table_name == "RAW_TRANSACTIONS":
        rename_map = {
            'CUSTOMER_ID': 'CUSTOMER_ID',
            'AMOUNT': 'AMOUNT',
            'CATEGORY': 'MERCHANT_CATEGORY',
            'TIMESTAMP': 'TIMESTAMP'
        }
    elif table_name == "SEGMENTED_CUSTOMERS":
        rename_map = {
            'CUSTOMER_ID': 'CUSTOMER_ID',
            'TOTAL_SPENT': 'TOTAL_SPENT'
        }
    else:
        raise ValueError(f"Unknown table: {table_name}")

    # Rename columns
    df = df.rename(columns=rename_map)

    # Convert datetime columns to string format explicitly
    for col in df.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns:
        df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Clean NaN values to None (NULL in SQL)
    df = df.replace({pd.NA: None, pd.NaT: None, float('nan'): None, 'NaN': None, 'nan': None})
    df = df.where(pd.notnull(df), None)

    # Keep only the required columns
    df = df[list(rename_map.values())]
    return df

# Function to load parquet file into Snowflake
def load_parquet_and_write_to_snowflake(file_path, table_name):
    if is_parquet_empty(file_path):
        print(f"❌ The file {file_path} is empty, skipping load.")
        return

    df = pd.read_parquet(file_path)

    df = map_columns(df, table_name)

    conn = create_snowflake_connection()
    cs = conn.cursor()

    try:
        for index, row in df.iterrows():
            placeholders = ", ".join(["%s"] * len(row))
            columns = ", ".join(row.index)
            values = tuple(row)

            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cs.execute(insert_query, values)

        print(f"✅ Successfully loaded {len(df)} records into {table_name}")
    except Exception as e:
        print(f"❌ Error inserting into {table_name}: {str(e)}")
    finally:
        cs.close()
        conn.close()

# Main function to load data
def load_data_to_snowflake():
    print(f"🔄 Loading data from {raw_transactions_path} into RAW_TRANSACTIONS...")
    load_parquet_and_write_to_snowflake(raw_transactions_path, "RAW_TRANSACTIONS")
    
    print(f"🔄 Loading data from {segmented_customers_path} into SEGMENTED_CUSTOMERS...")
    load_parquet_and_write_to_snowflake(segmented_customers_path, "SEGMENTED_CUSTOMERS")

# Run the data load
if __name__ == "__main__":
    load_data_to_snowflake()
