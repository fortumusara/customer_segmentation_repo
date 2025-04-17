# kafka_producer/send_transactions.py

from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime

# ✅ Updated Kafka configuration
KAFKA_BROKER = '192.168.82.154:9092'  # Replace with your actual host IP if different
TOPIC_NAME = 'bank-transactions'     # ✅ Correct topic name

# Sample data
CUSTOMERS = ['C001', 'C002', 'C003', 'C004']
CATEGORIES = ['grocery', 'fuel', 'entertainment', 'travel', 'utilities']

# Kafka JSON producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_transaction():
    return {
        "CUSTOMER_ID": random.choice(CUSTOMERS),
        "AMOUNT": round(random.uniform(5.0, 250.0), 2),
        "CATEGORY": random.choice(CATEGORIES),
        "TIMESTAMP": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    print("⏳ Sending mock transactions to Kafka...")
    try:
        while True:
            txn = generate_transaction()
            print(f"Sending: {txn}")
            producer.send(TOPIC_NAME, txn)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n✅ Transaction stream stopped.")
