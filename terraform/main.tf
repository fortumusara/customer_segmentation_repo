# terraform/main.tf

provider "snowflake" {
  user     = "YOUR_USERNAME"
  password = "YOUR_PASSWORD"
  account  = "YOUR_ACCOUNT_ID"
  region   = "YOUR_REGION" # e.g., "us-west-2"
}

# Create a database
resource "snowflake_database" "customer_db" {
  name = "CUSTOMER_DB"
}

# Create a schema
resource "snowflake_schema" "public" {
  name     = "PUBLIC"
  database = snowflake_database.customer_db.name
}

# Create a warehouse
resource "snowflake_warehouse" "customer_wh" {
  name      = "CUSTOMER_WH"
  size      = "SMALL"
  comment   = "Warehouse for Customer Segmentation ETL"
  auto_suspend = 60
  auto_resume  = true
}

# Create a table for storing customer transactions
resource "snowflake_table" "customer_spend" {
  name     = "CUSTOMER_SPEND"
  database = snowflake_database.customer_db.name
  schema   = snowflake_schema.public.name

  column {
    name = "customer_id"
    type = "STRING"
  }

  column {
    name = "total_spent"
    type = "FLOAT"
  }

  column {
    name = "category"
    type = "STRING"
  }

  column {
    name = "timestamp"
    type = "TIMESTAMP"
  }
}

output "snowflake_database" {
  value = snowflake_database.customer_db.name
}

output "snowflake_warehouse" {
  value = snowflake_warehouse.customer_wh.name
}
