-- ========================================
-- CSV vs Parquet Performance Comparison
-- ========================================

-- 1. Query CSV (raw zone)
SELECT COUNT(*) as total_customers_csv
FROM datalake_db.finanzas_customers;

-- 2. Query Parquet (processed zone) - SAME DATA
SELECT COUNT(*) as total_customers_parquet
FROM datalake_db.parquet_customers;

-- 3. Comparación de tamaño escaneado
-- Ejecutá ambas queries y mirá "Data scanned" en Athena

-- ========================================
-- Query más compleja - Clientes por ciudad
-- ========================================

-- CSV version
SELECT
    city,
    COUNT(*) as customer_count
FROM datalake_db.finanzas_customers
GROUP BY city
ORDER BY customer_count DESC
LIMIT 5;

-- Parquet version (SAME query, menor costo)
SELECT
    city,
    COUNT(*) as customer_count
FROM datalake_db.parquet_customers
GROUP BY city
ORDER BY customer_count DESC
LIMIT 5;

-- ========================================
-- Proyección de columnas (Parquet brilla aquí)
-- ========================================

-- Parquet: solo lee columnas necesarias
SELECT customer_id, email
FROM datalake_db.parquet_customers
LIMIT 10;

-- CSV: lee TODAS las columnas aunque solo uses 2
SELECT customer_id, email
FROM datalake_db.finanzas_customers
LIMIT 10;
