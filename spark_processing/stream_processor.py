import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

# Load environment variables from .env file (if needed)
load_dotenv()

# Define Kafka message schema
schema = StructType() \
    .add("CUSTOMER_ID", StringType()) \
    .add("AMOUNT", DoubleType()) \
    .add("CATEGORY", StringType()) \
    .add("TIMESTAMP", StringType())  # Will cast later to timestamp

# Initialize SparkSession with Kafka support
spark = SparkSession.builder \
    .appName("KafkaToParquetProcessor") \
    .getOrCreate()

# Read from Kafka
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "bank-transactions") \
    .option("startingOffsets", "latest") \
    .load()

# Parse and clean Kafka JSON messages
df_parsed = df_raw.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("TIMESTAMP", col("TIMESTAMP").cast(TimestampType()))

# Save raw cleaned transactions
df_parsed.writeStream \
    .format("parquet") \
    .option("path", "output/raw_transactions/") \
    .option("checkpointLocation", "checkpoints/raw") \
    .outputMode("append") \
    .start()

# Add watermark to allow aggregation on event time
df_with_watermark = df_parsed.withWatermark("TIMESTAMP", "2 minutes")

# Perform aggregation: total spent per customer per 1-minute window
df_agg = df_with_watermark.groupBy(
    window(col("TIMESTAMP"), "1 minute"),
    col("CUSTOMER_ID")
).agg({"AMOUNT": "sum"}) \
    .withColumnRenamed("sum(AMOUNT)", "TOTAL_SPENT")

# Format the final output
df_final = df_agg.select(
    col("window.start").alias("WINDOW_START"),
    col("window.end").alias("WINDOW_END"),
    col("CUSTOMER_ID"),
    col("TOTAL_SPENT")
)

# Write aggregated results to disk
df_final.writeStream \
    .format("parquet") \
    .option("path", "output/segmented_customers/") \
    .option("checkpointLocation", "checkpoints/segmented") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
