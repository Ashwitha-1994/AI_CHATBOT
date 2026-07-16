from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

conversation_collection = db["conversations"]
memory_collection = db["memory"]
session_collection = db["sessions"]