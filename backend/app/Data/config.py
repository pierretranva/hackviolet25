import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://hackviolet:hackviolet@cluster0.akrxj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
DATABASE_NAME = "jobapp_db"

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]