from pymongo import MongoClient

# MongoDB connection settings
MONGO_CLIENT_URL = "mongodb+srv://root:netweb@cluster0.7qpqqjr.mongodb.net/"  # Update this to use the MongoDB container hostname
DB_NAME = "sample_analytics"


class MongoConnectionManager:
    def __init__(self):
        self.mongodb_client = MongoClient(MONGO_CLIENT_URL)
    
def get_database(self):
    try:
        database = self.mongodb_client[DB_NAME]
        return database
    
    except Exception as e:
        raise "database connection lost."
    
