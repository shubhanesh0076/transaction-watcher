# app/mongodb.py

from pymongo import MongoClient
from fastapi import FastAPI

# MongoDB connection settings
MONGO_CLIENT_URL = "mongodb+srv://root:netweb@cluster0.7qpqqjr.mongodb.net/"  # Update this to use the MongoDB container hostname
DB_NAME = "sample_analytics"

# MongoDB client instance (initialized as None)
mongodb_client = None
database = None

def startup_db_client(app: FastAPI):
    global mongodb_client, database
    mongodb_client = MongoClient(MONGO_CLIENT_URL)
    database = mongodb_client[DB_NAME]

def shutdown_db_client(app: FastAPI):
    global mongodb_client
    if mongodb_client is not None:
        mongodb_client.close()

def get_database():
    return database
