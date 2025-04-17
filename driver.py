import os
import time
from dotenv import load_dotenv
from snowflake_loader.load_to_snowflake import load_parquet_and_write_to_snowflake

load_dotenv()

# Parquet output directories
RAW_PATH = "spark_processing/output/raw_transactions"
SEG_PATH = "spark_processing/output/segmented_customers"

# Table names (you can hardcode or get from .env)
TABLE_RAW = os.getenv("SNOWFLAKE_TABLE_RAW")
TABLE_SEG = os.getenv("SNOWFLAKE_TABLE_SEG")


def wait_for_parquet(path, timeout=120):
    print(f"⏳ Waiting for data in {path}...")
    for _ in range(timeout):
        if os.path.exists(path) and any(f.endswith(".parquet") for f in os.listdir(path)):
            print(f"✅ Parquet files found in {path}")
            return
        time.sleep(1)
    raise TimeoutError(f"❌ No Parquet files found in {path} after {timeout} seconds.")

def run_pipeline():
    wait_for_parquet(RAW_PATH)
    wait_for_parquet(SEG_PATH)
    load_parquet_and_write_to_snowflake(RAW_PATH, TABLE_RAW)
    load_parquet_and_write_to_snowflake(SEG_PATH, TABLE_SEG)

if __name__ == "__main__":
    run_pipeline()
