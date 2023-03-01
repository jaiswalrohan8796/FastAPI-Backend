from dotenv import dotenv_values
from pymongo import MongoClient
from typing import Dict

config: Dict = dotenv_values()

MONGODB_CLIENT: MongoClient = MongoClient(config["MONGODB_URI"])

MONGODB_DATABASE = MONGODB_CLIENT[config["DB_NAME"]]

USER_COLLECTION = MONGODB_DATABASE["USER"]


async def insert_user(user_dict):
    res = USER_COLLECTION.insert_one(user_dict)
    return res.acknowledged


async def find_user_with_email(user_email):
    user = USER_COLLECTION.find_one({"email": user_email})
    return user
