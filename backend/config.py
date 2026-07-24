import os
from dotenv import load_dotenv

load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "chatbot_db"
)

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "openrouter/free"
)

TEMPERATURE = float(
    os.getenv("TEMPERATURE", 0.5)
)

MAX_TOKENS = int(
    os.getenv("MAX_TOKENS", 1500)
)


print("Mongo URI Loaded:")
print(MONGO_URI)