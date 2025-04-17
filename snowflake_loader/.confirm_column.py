import pandas as pd

df = pd.read_parquet("../spark_processing/output/raw_transactions/part-00000-*.parquet")
print(df.columns.tolist())
