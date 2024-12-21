import json

def scrape_reddit():
    # Simulate scraping data
    data = [
        {"id": 1, "title": "Post about Palestine", "text": "Important news", "created_utc": 1670000000},
        {"id": 2, "title": "Another post", "text": "Something interesting", "created_utc": 1670000500},
    ]

    # Save the dummy data to a JSON file
    with open("/opt/airflow/dags/data/raw_data.json", "w") as f:
        json.dump(data, f)

    print("Scraping completed. Data saved to raw_data.json.")
