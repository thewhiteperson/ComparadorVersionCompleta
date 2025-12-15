from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

if not MONGO_URI or not MONGO_DB:
    raise Exception("Variables de entorno de MongoDB no configuradas")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

productos_collection = db["productos"]
