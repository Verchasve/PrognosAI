import pymongo
from global_logger import global_logger
from settings import Config

# MongoDB Configuration 
MONGO_URI = "mongodb://"+Config.MONGODB_HOST+":"+Config.MONGODB_PORT+"/"
DB_NAME = Config.MONGODB_COLLECTION_NAME

def get_mongo_client():
    try:
        client = pymongo.MongoClient(MONGO_URI)
        global_logger.info("MongoDB client connected successfully.")
        return client
    except pymongo.errors.ConnectionError as e:
        global_logger.error(f"Failed to connect to MongoDB: {e}")
        return None

def get_database(client):
    return client[DB_NAME]
