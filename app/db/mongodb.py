from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")  # e.g. mongodb://localhost:27017
client = AsyncIOMotorClient(MONGO_URI)

db = client["virtual_tryon"]
tryon_collection = db["tryon_records"]
