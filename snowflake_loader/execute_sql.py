import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

def execute_sql_script(script_path):
    with open(script_path, 'r') as file:
        sql = file.read()

    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT_ID"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

    try:
        cs = conn.cursor()
        for stmt in sql.split(";"):
            if stmt.strip():
                print(f"🧠 Executing:\n{stmt.strip()}")
                cs.execute(stmt)
        print("✅ SQL script executed successfully.")
    finally:
        cs.close()
        conn.close()
