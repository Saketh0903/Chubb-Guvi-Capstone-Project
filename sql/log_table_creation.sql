-- Bronze log
CREATE TABLE IF NOT EXISTS capstone.default.bronze_log (
    log_id STRING,
    table_name STRING,
    source_system STRING,
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP
) USING DELTA;

-- Silver log
CREATE TABLE IF NOT EXISTS capstone.default.silver_log (
    log_id STRING,
    table_name STRING,
    source_system STRING,
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP
) USING DELTA;

-- Gold log
CREATE TABLE IF NOT EXISTS capstone.default.gold_log (
    log_id STRING,
    table_name STRING,
    source_system STRING,
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP
) USING DELTA;