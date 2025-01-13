import pymongo
from global_logger import global_logger

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "saas_integration"

def get_mongo_client():
    try:
        client = pymongo.MongoClient(MONGO_URI)
        global_logger.info("MongoDB client connected successfully.")
        return client
    except pymongo.errors.ConnectionError as e:
        global_logger.error(f"Failed to connect to MongoDB: {e}")
        return None

def get_database(client):
    return client[DATABASE_NAME]
