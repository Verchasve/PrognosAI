import pymongo
import requests
import json
from settings import Config

# MongoDB connection
MONGO_URI = "mongodb://"+Config.MONGODB_HOST+":"+Config.MONGODB_PORT+"/"
DB_NAME = Config.MONGODB_SERVICENOW_COLLECTION
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections for raw API responses and normalized data
api_response_col = db["api_response"]
normalized_data_col = db["normalized_data"]

# ServiceNow API
def fetch_servicenow_data():
    url = "https://your-instance.service-now.com/api/now/table/incident"
    headers = {"Authorization": "Bearer your_token"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        api_response_col.insert_many(response.json().get("result", []))
        normalize_servicenow_data(response.json().get("result", []))

# Jira API
def fetch_jira_data():
    url = "https://your-domain.atlassian.net/rest/api/3/search"
    headers = {"Authorization": "Bearer your_token"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        api_response_col.insert_many(response.json().get("issues", []))
        normalize_jira_data(response.json().get("issues", []))

# Normalize data
def normalize_servicenow_data(data):
    normalized = [
        {
            "ticket_id": item["sys_id"],
            "type": "incident",
            "description": item["short_description"],
            "status": item["state"],
            "resolution": item.get("close_notes"),
        }
        for item in data
    ]
    normalized_data_col.insert_many(normalized)

def normalize_jira_data(data):
    normalized = [
        {
            "ticket_id": item["id"],
            "type": "task",
            "description": item["fields"]["summary"],
            "status": item["fields"]["status"]["name"],
            "resolution": item["fields"]["resolution"],
        }
        for item in data
    ]
    normalized_data_col.insert_many(normalized)

# Fetch data
fetch_servicenow_data()
fetch_jira_data()
