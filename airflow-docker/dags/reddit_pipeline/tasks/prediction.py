import pandas as pd

def run_model():
    # Read the preprocessed data
    df = pd.read_csv("/opt/airflow/dags/data/preprocessed_data.csv")

    # Simulate predictions
    df["predictions"] = ["positive" if "important" in text else "neutral" for text in df["cleaned_text"]]

    # Save the predicted data
    df.to_csv("/opt/airflow/dags/data/predicted_data.csv", index=False)

    print("Prediction completed. Data saved to predicted_data.csv.")
