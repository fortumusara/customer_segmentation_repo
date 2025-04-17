---

# 🧠 Customer Segmentation & Personalization ETL Pipeline

This project demonstrates a real-time ETL pipeline for customer segmentation and personalized offer delivery. It integrates data from banking transactions, customer demographics, and engagement sources to build enriched customer profiles and drive marketing decisions.

---

## 🚀 Project Overview

**Goal:** Segment customers based on behavior and demographics, and deliver real-time personalized offers using modern data tools and ML algorithms.

**Technologies Used:**
- **Kafka** – Real-time transaction ingestion
- **PySpark** – Transformation and clustering (K-Means)
- **Snowflake** – Centralized data warehouse
- **AWS Glue** – ETL orchestration
- **Python APIs** – Integration with personalization platforms (e.g., Salesforce, Twilio)

---

## 🛠️ Pipeline Architecture

```
Kafka Producer → Spark Structured Streaming → Parquet Files → Snowflake
```

---

## ▶️ Quickstart

### ✅ 1. Start Kafka Producer

Simulate real-time banking transactions:

```bash
cd kafka_producer
python send_transactions.py
```

### ✅ 2. Launch Spark Streaming Job

Process the stream, write to Parquet:

```bash
cd spark_processing
spark-submit stream_processor.py
```

Parquet output folders:
- `spark_processing/output/raw_transactions`
- `spark_processing/output/segmented_customers`

### ✅ 3. Load Data to Snowflake

Use the unified driver to load raw and segmented data from Parquet to Snowflake:

```bash
python driver.py
```

This driver handles both raw and aggregated files and uploads them into the appropriate Snowflake tables:
- `CUSTOMER_SEGMENTATION.RAW_TRANSACTIONS`
- `CUSTOMER_SEGMENTATION.SEGMENTED_CUSTOMERS`

---

## 📊 Sample Use Case

> A customer in the Gold Tier with high grocery spending and low travel purchases might receive:  
> **"Earn 30% cash back on groceries this month, and 20% off your next travel booking!"**

---

## 🔮 Roadmap

- [ ] Terraform template for AWS Glue, Snowflake, Kafka
- [ ] Databricks Notebook for clustering & LTV scoring
- [ ] REST API mock for customer demographics
- [ ] Dashboard with Power BI or Streamlit

---

## 🤝 Contributions

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📄 License

MIT License © 2025 Fortune

---

## 📦 Project Structure

```bash
customer_segmentation_repo/
├── driver.py                     # Unified script to trigger Snowflake loading
├── kafka_producer/
│   └── send_transactions.py      # Simulates real-time banking transactions
├── spark_processing/
│   ├── stream_processor.py       # Processes Kafka stream using PySpark
│   └── output/                   # Parquet files (raw + segmented)
├── snowflake_loader/
│   └── load_to_snowflake.py      # Batch load logic for Snowflake
├── terraform/
│   └── main.tf                   # (Coming Soon) Infra provisioning
├── notebooks/
│   └── customer_segmentation.ipynb  # Databricks ML notebook (Coming Soon)
├── .env
├── requirements.txt
├── README.md
```

---


