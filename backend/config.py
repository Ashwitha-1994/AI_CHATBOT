import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL_NAME = os.getenv("MODEL_NAME")

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))