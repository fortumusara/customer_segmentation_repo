# kafka_producer/send_transactions.py

from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'bank-transactions'

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
        "customer_id": random.choice(CUSTOMERS),
        "amount": round(random.uniform(5.0, 250.0), 2),
        "category": random.choice(CATEGORIES),
        "timestamp": datetime.utcnow().isoformat()
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
