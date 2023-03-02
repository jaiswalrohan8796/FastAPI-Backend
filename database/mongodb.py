from dotenv import dotenv_values
from pymongo import MongoClient
from typing import Dict
from uuid import uuid4

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


async def delete_todo_by_id(email, todo_id):
    filter = {"email": email}
    delete_todo_operation = {"$pull": {"todos": {"id": todo_id}}}
    res = USER_COLLECTION.update_one(
        filter=filter, update=delete_todo_operation)
    if res.modified_count == 1:
        return True
    return False


async def add_todo(email, todo_text):
    filter = {"email": email}
    add_todo_operation = {
        "$push": {"todos": {"id": str(uuid4()), "desc": todo_text}}}
    res = USER_COLLECTION.update_one(filter=filter, update=add_todo_operation)
    if res.modified_count == 1:
        return True
    return False


async def find_todo_by_id(email, todo_id):
    user = await find_user_with_email(email)
    if user:
        for todo in user["todos"]:
            if todo_id == todo["id"]:
                return todo
    return None


async def edit_todo_by_email_todo_id(email, todo_id, todo_data):
    user = await find_user_with_email(email)
    if user:
        for todo in user["todos"]:
            if todo_id == todo["id"]:
                todo["desc"] = todo_data
                break
        filter = {"email": user["email"]}
        save_operation = {"$set": {"todos": user["todos"]}}
        res = USER_COLLECTION.update_one(filter=filter, update=save_operation)
        if res.modified_count == 1:
            return True
    return False
