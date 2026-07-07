# Enterprise Multi-Cloud Data Engineering Platform
Developed by Luel Gebreselassie | Technical Data Engineer
An end-to-end cloud data pipeline engineered to ingest, process, and store live global aviation transponder logs in real time. This platform bridges production software infrastructure with high-level corporate business intelligence.

## 🏗️ Platform System Architecture
The pipeline is designed using a modern decoupled data lakehouse framework:
1. **Extraction (Python & Docker):** A containerized Python application connects to live aerospace API telemetry streams to extract real-time aircraft coordinates, velocities, and altitudes.
2. **Orchestration (Apache Airflow):** Automates chronological task dependencies and schedules daily workflows directly into an enterprise storage landing zone.
3. **Processing (Azure Databricks & Spark):** Implements a Medallion Architecture (Bronze -> Silver -> Gold layers) using PySpark to clean, filter, and structure massive, messy logs.
4. **Warehousing (Snowflake):** Loads highly optimized relational data tables to handle low-latency analytics query tracking.
5. **Analytics (Power BI):** Connects reporting suites directly to the warehouse layer via DirectQuery to deliver live operational flight logistics dashboards.

## 🛠️ Tech Stack & Tool Grid
* **Languages:** Python, SQL, PySpark
* **Cloud Infrastructure:** Microsoft Azure (Blob Storage, Data Factory)
* **Data Processing & Lakehouse:** Azure Databricks, Apache Spark, Snowflake
* **Workflow Automation & Containers:** Apache Airflow, Docker, Docker Compose
* **Business Intelligence:** Microsoft Power BI

## 🚀 Getting Started Locally
To spin up this data pipeline container inside your local environment, ensure you have Docker installed and run the following terminal sequences:

```bash
# Clone the enterprise data platform repository
git clone https://github.com

# Build the custom Python data extraction image
docker build -t aviation-extractor .

# Run the automated telemetry pipeline container
docker run -v \$(pwd)/data_lake:/app/data_lake aviation-extractor
