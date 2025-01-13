from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import timedelta

from reddit_pipeline.tasks.scraping import scrape_reddit
from reddit_pipeline.tasks.preprocessing import preprocess_data
from reddit_pipeline.tasks.prediction import run_model
from reddit_pipeline.tasks.deployment import deploy_visualization
from reddit_pipeline.tasks.training import run_model_for_training
from reddit_pipeline.tasks.llm_labels import generate_text
from reddit_pipeline.tasks.model_replacement import replace_model

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
    
    
    # Task 3': Run Predictions of the labels 
    task_predict_label = PythonOperator(
        task_id="generate_text",
        python_callable=generate_text,
    )
    
    # Task 4': Run model training
    task_train_model = PythonOperator(
        task_id="run_model_for_training",
        python_callable=run_model_for_training,
    )

       # Task 5': Replace Trained Model
    task_replace_model = PythonOperator(
        task_id="replace_model",
        python_callable=replace_model,  # Replace the model with a new one after training
    )




  # Step 1: Scrape Reddit data first, followed by preprocessing
task_scrape >> task_preprocess

# Step 2: After preprocessing, run predictions and label generation in parallel
task_preprocess >> [task_predict, task_predict_label]

# Step 3: After generating labels, train the model
task_predict_label >> task_train_model

# Step 4: After training, replace the existing model
task_train_model >> task_replace_model

# Step 5: Use the replaced model to run predictions
task_replace_model >> task_predict

# Step 6: Deploy and visualize depends on the outcomes of both predictions and label generation
[task_predict, task_predict_label] >> task_deploy