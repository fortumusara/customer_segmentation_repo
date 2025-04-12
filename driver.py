import os
from snowflake_loader.execute_sql import execute_sql_script
from snowflake_loader.load_to_snowflake import load_data_to_snowflake

if __name__ == "__main__":
    print("🚀 Starting Customer Segmentation Pipeline")

    # Step 1 - Load data from local staging to Snowflake RAW table
    load_data_to_snowflake()

    # Step 2 - Create/Ensure tables exist
    execute_sql_script("snowflake_loader/create_tables.sql")

    # Step 3 - Apply segmentation
    execute_sql_script("snowflake_loader/transform_segment.sql")

    print("✅ Pipeline execution complete.")
