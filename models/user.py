from pydantic import BaseModel, EmailStr, validator
from typing import List, Union
from uuid import uuid4, UUID


class Todo(BaseModel):
    id: UUID = uuid4()
    desc: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


def get_user(user_data):
    return {
        "username": user_data.username,
        "email": user_data.email,
        "password": user_data.password,
        "todos": []
    }
