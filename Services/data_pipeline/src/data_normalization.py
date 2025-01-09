# Schema Normalization Script
# This script processes API responses into a unified format for downstream ML tasks.

import pymongo
from datetime import datetime, timezone

# MongoDB Configuration
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["saas_integration"]

def normalize_data():
    raw_data = db.api_responses.find()
    for document in raw_data:
        api_name = document["api_name"]
        raw_response = document["response_data"]

        # Example normalization: Map fields to a unified schema
        normalized = []
        for item in raw_response:
            description = item.get("description", "")
            if not description:
                description = "no description available fro this crypto repo"
            normalized.append({
                "id": item.get("id", ""),
                "name": item.get("name", ""),
                "description": description,
                "created_at": item.get("created_at", ""),
                "updated_at": item.get("updated_at", "")
            })

        # Store normalized data
        db.normalized_data.insert_one({
            "api_name": api_name,
            "unified_schema": normalized,
            "source_id": document["_id"],
            "preprocessing_timestamp": datetime.now(timezone.utc)
        })
        print(f"Normalized data stored for API: {api_name}")

# Example Usage
normalize_data()
