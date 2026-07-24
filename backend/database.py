from pymongo import MongoClient
from backend.config import MONGO_URI, DATABASE_NAME


print("Connecting MongoDB...")


try:

    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000
    )


    # Test connection
    client.admin.command("ping")


    print("MongoDB Connected Successfully")


    db = client[DATABASE_NAME]


    conversation_collection = db["conversations"]

    memory_collection = db["memory"]


except Exception as e:

    print("MongoDB Connection Failed")
    print(e)


    conversation_collection = None
    memory_collection = None