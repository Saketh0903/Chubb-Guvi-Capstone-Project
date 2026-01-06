CREATE TABLE IF NOT EXISTS capstone.default.silver_companies (
    ticker STRING,
    company_name STRING,
    sector STRING,
    industry STRING,
    country STRING,
    exchange STRING,
    currency STRING,
    is_active BOOLEAN,

    silver_processed_timestamp TIMESTAMP
)
USING DELTA;

CREATE TABLE IF NOT EXISTS capstone.default.silver_daily_prices (
    ticker STRING,
    trade_date DATE,

    open_price DOUBLE,
    high_price DOUBLE,
    low_price DOUBLE,
    close_price DOUBLE,
    adjusted_close DOUBLE,
    volume BIGINT,

    silver_processed_timestamp TIMESTAMP
)
USING DELTA;

CREATE TABLE IF NOT EXISTS capstone.default.silver_traders (
    trader_id STRING,
    trader_type STRING,
    initial_cash DOUBLE,
    base_currency STRING,
    created_at TIMESTAMP,

    silver_processed_timestamp TIMESTAMP
)
USING DELTA;

CREATE TABLE IF NOT EXISTS capstone.default.silver_trades (
    trade_id STRING,
    trader_id STRING,
    ticker STRING,
    trade_date DATE,
    trade_time TIMESTAMP,

    side STRING,
    quantity INT,
    price DOUBLE,
    trade_value DOUBLE,

    silver_processed_timestamp TIMESTAMP
)
USING DELTA;

CREATE TABLE IF NOT EXISTS capstone.default.silver_fx_rates (
    fx_date DATE,
    from_currency STRING,
    to_currency STRING,
    fx_rate DOUBLE,
    ingestion_timestamp TIMESTAMP,
    source_file STRING,
    load_type STRING,
    silver_processed_timestamp TIMESTAMP
)
USING DELTA;

CREATE TABLE IF NOT EXISTS capstone.default.silver_watermark (
    table_name STRING,
    last_processed_timestamp TIMESTAMP
) USING DELTA;