from motor.motor_asyncio import AsyncIOMotorClient
import os

db_client = AsyncIOMotorClient(os.environ["MONGO_CONNECTION"])
db = db_client["mygpt"]
