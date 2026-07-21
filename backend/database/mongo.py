import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pathlib import Path

load_dotenv(
    Path(__file__).resolve().parent.parent / ".env"
)

MONGO_URI = os.getenv("MONGO_URI")

print("MONGO_URI =", MONGO_URI)

client = MongoClient(MONGO_URI)

db = client["rag_assistant"]

chat_collection = db["chat_history"]