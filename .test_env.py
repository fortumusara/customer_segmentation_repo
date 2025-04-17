import os
from dotenv import load_dotenv
from snowflake_loader.execute_sql import execute_sql_script  # Import your module

# Step 4.1: Load environment variables
load_dotenv()

# Step 4.2: Debug print env variables (optional)
print("SNOWFLAKE_ACCOUNT_ID =", os.getenv("SNOWFLAKE_ACCOUNT_ID"))
print("SNOWFLAKE_USER =", os.getenv("SNOWFLAKE_USER"))
print("SNOWFLAKE_PASSWORD =", os.getenv("SNOWFLAKE_PASSWORD"))
print("SNOWFLAKE_DATABASE =", os.getenv("SNOWFLAKE_DATABASE"))
print("SNOWFLAKE_SCHEMA =", os.getenv("SNOWFLAKE_SCHEMA"))
print("SNOWFLAKE_WAREHOUSE =", os.getenv("SNOWFLAKE_WAREHOUSE"))

# Step 4.3: Run SQL to ensure Snowflake tables exist
execute_sql_script("snowflake_loader/create_tables.sql")
