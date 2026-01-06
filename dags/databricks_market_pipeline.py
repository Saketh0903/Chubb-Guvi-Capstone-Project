from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from datetime import timedelta
import logging
import os
from logging.handlers import RotatingFileHandler

# -------------------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------------------

LOG_DIR = "/opt/airflow/logs/custom"
LOG_FILE = f"{LOG_DIR}/databricks_market_pipeline.log"

os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger():
    logger = logging.getLogger("market_pipeline")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # Log to Airflow task logs (stdout)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Log to file (rotating)
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()


default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
}


def log_pipeline_start(**context):
    ingest_date = context["ds"]
    logger.info("======================================")
    logger.info("Starting Databricks Market Pipeline")
    logger.info(f"Ingest Date (logical): {ingest_date}")
    logger.info("======================================")

def log_pipeline_end(**context):
    logger.info("======================================")
    logger.info("Databricks Market Pipeline completed successfully")
    logger.info("======================================")


with DAG(
    dag_id="databricks_market_pipeline",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="0 2 * * *",  # Daily at 02:00
    catchup=False,
    tags=["databricks", "bronze", "silver", "gold"],
) as dag:

    start_logging = PythonOperator(
        task_id="log_pipeline_start",
        python_callable=log_pipeline_start,
        provide_context=True,
    )

    run_databricks_job = DatabricksRunNowOperator(
        task_id="run_market_pipeline_job",
        databricks_conn_id="databricks_default",
        job_id=640556658361294,
        notebook_params={
            # Run pipeline for previous day
            "ingest_date": "{{ macros.ds_add(ds, -1) }}"
        },
    )

    end_logging = PythonOperator(
        task_id="log_pipeline_end",
        python_callable=log_pipeline_end,
        provide_context=True,
    )

    # Task Dependencies
    start_logging >> run_databricks_job >> end_logging
