from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import timedelta

from reddit_pipeline.tasks.scraping import scrape_reddit
from reddit_pipeline.tasks.preprocessing import preprocess_data
from reddit_pipeline.tasks.prediction import run_model
from reddit_pipeline.tasks.deployment import deploy_visualization

# Define the default arguments for the DAG
default_args = {
    "owner": "airflow",  # Owner of the DAG
    "depends_on_past": False,  # Do not wait for past runs
    "retries": 1,  # Retry once in case of failure
    "retry_delay": timedelta(minutes=5),  # Wait 5 minutes before retrying
    "email_on_failure": False,  # Disable email notifications for failures
    "email_on_retry": False,  # Disable email notifications for retries
}

# Define the DAG
with DAG(
    dag_id="reddit_pipeline",
    start_date=datetime(2024, 12, 21),
    schedule_interval=None,  # Manual trigger for testing
    catchup=False,  # No backfilling
    default_args=default_args,  # Use the default_args dictionary
) as dag:

    # Task 1: Scrape Reddit Data
    task_scrape = PythonOperator(
        task_id="scrape_reddit",
        python_callable=scrape_reddit,
    )

    # Task 2: Preprocess Data
    task_preprocess = PythonOperator(
        task_id="preprocess_data",
        python_callable=preprocess_data,
    )

    # Task 3: Run Predictions
    task_predict = PythonOperator(
        task_id="run_model",
        python_callable=run_model,
    )

    # Task 4: Deploy and Visualize
    task_deploy = PythonOperator(
        task_id="deploy_visualization",
        python_callable=deploy_visualization,
    )

    # Set task dependencies
    task_scrape >> task_preprocess >> task_predict >> task_deploy
