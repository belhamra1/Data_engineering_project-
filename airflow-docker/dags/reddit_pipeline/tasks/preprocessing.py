import json
import pandas as pd

def preprocess_data():
    # Read the raw data
    with open("/opt/airflow/dags/data/raw_data.json", "r") as f:
        data = json.load(f)

    # Convert to DataFrame for preprocessing
    df = pd.DataFrame(data)

    # Preprocess: Lowercase the text and strip whitespace
    df["cleaned_text"] = df["text"].str.lower().str.strip()

    # Save the preprocessed data
    df.to_csv("/opt/airflow/dags/data/preprocessed_data.csv", index=False)

    print("Preprocessing completed. Data saved to preprocessed_data.csv.")
