import requests
import pymongo
from datetime import datetime , timezone
from settings import Config

# Use the environment variables
print(f'Database URL: {Config.MONGODB_HOST}')
print(f'Secret Key: {Config.MONGODB_PORT}')

# MongoDB Configuration
MONGO_URI = "mongodb://"+Config.MONGODB_HOST+":"+Config.MONGODB_PORT+"/"
DB_NAME = Config.MONGODB_COLLECTION_NAME
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

# # Function to fetch and store API data
def fetch_and_store(api_name, endpoint, headers=None, params=None):
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Store raw response in MongoDB
        db.api_responses.insert_one({
            "api_name": api_name,
            "endpoint": endpoint,
            "response_data": data,
            "response_status_code": response.status_code,
            "schema_metadata": {k: type(v).__name__ if not isinstance(v, list) else "list" for k, v in data.items()} if not isinstance(data, list) else "list",
            "ingestion_timestamp": datetime.now(timezone.utc)
        })
        print(f"Data from {api_name} stored successfully.")
    except Exception as e:
        print(f"Error fetching data from {api_name}: {e}")

# Example Usage
fetch_and_store(
    api_name= Config.API_NAME,
    endpoint= Config.API_URL,
    headers={"Authorization": Config.GITHUB_AUTH_TOKEN}
)
