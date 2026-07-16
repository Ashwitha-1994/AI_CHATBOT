from database import memory_collection
from datetime import datetime


def get_memory(user_id):

    memory = memory_collection.find_one({"user_id": user_id})

    if memory:
        return memory

    return {
        "profile": {},
        "summary": ""
    }


def save_memory(user_id, profile, summary):

    memory_collection.update_one(

        {"user_id": user_id},

        {
            "$set": {

                "profile": profile,

                "summary": summary,

                "last_updated": datetime.utcnow()

            }

        },

        upsert=True

    )