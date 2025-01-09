import os
from dotenv import load_dotenv

# Load environment variables from 'local.env' file
load_dotenv('../local.env')

class Config:
    # API name that will be used to store the data
    API_NAME = os.getenv('api_name')
    API_URL = os.getenv('api_url')

    # GitHub Configuration
    GITHUB_AUTH_TOKEN = os.getenv('gitHub_auth_token')

    # MongoDB Configuration
    MONGODB_HOST =  os.getenv('MONGODB_HOST')
    MONGODB_PORT =  os.getenv('MONGODB_PORT')
    MONGODB_COLLECTION_NAME =  os.getenv('MONGODB_COLLECTION_NAME')
    MONGODB_SERVICENOW_COLLECTION =  os.getenv('MONGODB_SERVICE_NOW_COLLECTION')

# Optionally, check if all necessary environment variables are loaded
if not Config.MONGODB_HOST or not Config.MONGODB_PORT or not Config.MONGODB_COLLECTION_NAME:
    raise EnvironmentError('Some environment variables are missing.')
