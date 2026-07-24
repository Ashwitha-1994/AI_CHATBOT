from backend.database import conversation_collection
from datetime import datetime


def get_conversation_history(user_id: str, limit: int = 10):
    """
    Returns the last 'limit' messages for the user,
    ordered from oldest to newest.
    """

    conversations = list(
        conversation_collection.find(
            {"user_id": user_id}
        )
        .sort("_id", -1)
        .limit(limit)
    )

    conversations.reverse()

    return conversations


def save_message(
    user_id,
    role,
    message,
    sentiment=None,
    confidence=None
):

    conversation_collection.insert_one({

        "user_id": user_id,

        "role": role,

        "message": message,

        "sentiment": sentiment,

        "confidence": confidence,

        "timestamp": datetime.utcnow()

    })