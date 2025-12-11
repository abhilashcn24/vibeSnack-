from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "vibesnack"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_db():
    return db

def get_snacks_collection():
    return db["snacks"]

def get_history_collection():
    return db["history"]
