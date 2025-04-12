# spark_processing/stream_processor.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

# Define schema for Kafka JSON payload
schema = StructType() \
    .add("customer_id", StringType()) \
    .add("amount", DoubleType()) \
    .add("category", StringType()) \
    .add("timestamp", StringType())  # Will be cast to TimestampType later

# Create Spark session
spark = SparkSession.builder \
    .appName("KafkaTransactionProcessor") \
    .getOrCreate()

# Read stream from Kafka
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "bank-transactions") \
    .option("startingOffsets", "latest") \
    .load()

# Convert Kafka value to string and parse JSON
df_parsed = df_raw.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("timestamp", col("timestamp").cast(TimestampType()))

# Group and aggregate by 1-minute windows
df_agg = df_parsed.groupBy(
    window(col("timestamp"), "1 minute"),
    col("customer_id")
).agg(
    {"amount": "sum"}
).withColumnRenamed("sum(amount)", "total_spent")

# Output to console
query = df_agg.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
