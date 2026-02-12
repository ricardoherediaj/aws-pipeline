-- ========================================
-- Athena Queries - Finance Data Lake
-- Database: datalake_db
-- ========================================

-- 1. Ver tablas creadas por el crawler
SHOW TABLES IN datalake_db;

-- 2. Query básica - Contar registros
SELECT COUNT(*) FROM datalake_db.finanzas_customers;

-- 3. Query más compleja - Clientes por ciudad
SELECT
    city,
    COUNT(*) as customer_count
FROM datalake_db.finanzas_customers
GROUP BY city
ORDER BY customer_count DESC;

-- ========================================
-- QUERIES ADICIONALES (Comentadas)
-- ========================================
/*
-- Ver schema de una tabla
DESCRIBE datalake_db.finanzas_customers;

-- Contar transacciones
SELECT COUNT(*) FROM datalake_db.finanzas_transactions;

-- Top 10 clientes por balance total
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name as full_name,
    SUM(CAST(a.balance AS DOUBLE)) as total_balance
FROM datalake_db.finanzas_customers c
JOIN datalake_db.finanzas_accounts a ON c.customer_id = a.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_balance DESC
LIMIT 10;

-- Distribución de credit scores
SELECT
    CASE
        WHEN CAST(credit_score AS INTEGER) >= 750 THEN 'Excellent'
        WHEN CAST(credit_score AS INTEGER) >= 650 THEN 'Good'
        WHEN CAST(credit_score AS INTEGER) >= 550 THEN 'Fair'
        ELSE 'Poor'
    END as score_category,
    COUNT(*) as customer_count
FROM datalake_db.finanzas_customers
GROUP BY 1
ORDER BY customer_count DESC;

-- Préstamos activos
SELECT
    l.loan_type,
    COUNT(*) as num_loans,
    SUM(CAST(l.amount AS DOUBLE)) as total_amount
FROM datalake_db.finanzas_loans l
WHERE l.status = 'active'
GROUP BY l.loan_type
ORDER BY total_amount DESC;
*/
