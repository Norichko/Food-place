from pymongo import MongoClient, GEOSPHERE
from app.core.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["food_place"]

users_collection = db["users"]
restaurants_collection = db["restaurants"]
dishes_collection = db["dishes"]
reviews_collection = db["reviews"]

restaurants_collection.create_index([("location", GEOSPHERE)])