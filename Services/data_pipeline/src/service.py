from datetime import datetime , timezone
from settings import Config
from dateutil.parser import parse
from mongo_client import get_mongo_client, get_database
from global_logger import global_logger
# MongoDB connection 
client = get_mongo_client()
db = get_database(client)

# Collections  normalized data
normalized_data_collection = db["sanitized_data"]
servicenow_data_collection = db["snow_ied"]
jira_data_collection = db["jira_data"]

# Load data from ServiceNow and JIRA collections
service_now_data = list(servicenow_data_collection.find())
jira_data = list(jira_data_collection.find())

# Define normalization functions
def calculate_duration(created_at, updated_at):
    if(created_at == None or updated_at == None):
        return 0
    created = parse(created_at) 
    updated = parse(updated_at)  
    return (updated - created).total_seconds() / 3600  # Convert to hours

def normalize_priority(priority):
    priority_map = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
    return priority_map.get(priority, 0)  # Default to 0 if priority not found


def normalize_data(data, source):
    normalized = []
    for record in data:
        normalized.append({
            "eid": record.get("incident_id") or record.get("story_id"),
            "short_description": record.get("short_description") or record.get("summary"),
            "description": record.get("description", ""),
            "priority": normalize_priority(record.get("priority", "")),
            "type": record.get("type") or ("Incident" if source == "servicenow" else "Story"),
            "status": record.get("state") or record.get("status"),
            "created_at": record.get("created_at"),
            "updated_at": record.get("updated_at"),
            "time_to_resolve": calculate_duration(record.get("created_at"), record.get("updated_at")),
            "category": record.get("category") or record.get("labels", ""),
            "assignee": record.get("assigned_to") or record.get("assignee"),
            "resolution": record.get("resolution", "No resolution provided")
        })
    return normalized

 
def main():
    # Normalize data
    normalized_servicenow = normalize_data(service_now_data, "servicenow")
    normalized_jira = normalize_data(jira_data, "jira")

    # Insert normalized data into MongoDB
    normalized_data_collection.insert_many(normalized_servicenow + normalized_jira)
    global_logger.info("Normalized data inserted into MongoDB.")

if __name__ == "__main__":
    main()