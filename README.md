# 🏦 Finance Data Lake - AWS Pipeline

> Serverless Data Lake on AWS using S3, Glue, and Athena for financial data analysis with cost optimization.

[![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20Glue%20%7C%20Athena-orange)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)

---

## 📋 Table of Contents

- [Description](#description)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [Cost Optimization](#cost-optimization)
- [Example Queries](#example-queries)

---

## 🎯 Description

Serverless Data Lake that processes **12 financial data entities** (customers, accounts, transactions, loans, etc.) with Medallion architecture (raw/processed/analytics) and cost optimization through Parquet and lifecycle policies.

**Problem solved:** Centralize dispersed financial data into a queryable Data Lake with SQL, optimized for < $5/month operational costs.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AWS Data Lake                        │
├─────────────────────────────────────────────────────────┤
│  📁 S3 (rherediaiam-datalake-2026)                     │
│  ├── raw/finance/               [CSV, partitioned]     │
│  ├── processed/finance/         [Parquet, 30% smaller]│
│  ├── analytics/reports/         [Aggregations]        │
│  └── athena-results/            [Query outputs]        │
│                                                         │
│  🕷️  AWS Glue Data Catalog                              │
│  ├── Database: datalake_db                             │
│  └── Tables: 24 (12 CSV + 12 Parquet)                 │
│                                                         │
│  🔍 Amazon Athena - SQL queries on S3                  │
└─────────────────────────────────────────────────────────┘
```

**🎨 Interactive Architecture Diagram:**
Open `aws-pipeline-architecture.excalidraw.json` in:
- **VS Code** with [Excalidraw Extension](https://marketplace.visualstudio.com/items?itemName=pomdtr.excalidraw-editor)
- **Online Editor** at https://excalidraw.com (File → Open → Upload JSON)

---

## 🛠️ Technologies

- **S3**: Object storage
- **Glue**: Automatic cataloging
- **Athena**: Serverless SQL queries
- **Python 3.13** + boto3 + pandas + pyarrow

---

## 🚀 Setup

```bash
# Install dependencies
uv sync

# Configure credentials
cp .env.example .env
# Edit .env with your AWS credentials
```

---

## 📦 Usage

```bash
# 1. Create bucket and structure
uv run python scripts/01_setup_s3.py

# 2. Upload CSV data
uv run python scripts/03_upload_to_s3.py

# 3. Catalog with Glue
uv run python scripts/05_setup_glue.py

# 4. Transform to Parquet
uv run python scripts/07_transform_to_parquet.py

# 5. Lifecycle policies
uv run python scripts/09_setup_lifecycle.py
```

---

## 💰 Cost Optimization

- **Parquet**: 30% compression vs CSV
- **Partitioning**: Queries 10x faster
- **Lifecycle**: raw → Glacier (83% savings)
- **Total**: < $2/month

---

## 🔍 Example Queries

```sql
-- View tables
SHOW TABLES IN datalake_db;

-- Count customers
SELECT COUNT(*) FROM datalake_db.parquet_customers;

-- Top cities
SELECT city, COUNT(*) as total
FROM datalake_db.parquet_customers
GROUP BY city
ORDER BY total DESC;
```

---

## 👤 Author

**Ricardo Heredia**

---

⭐ **AWS Data Lake - Portfolio Project**
