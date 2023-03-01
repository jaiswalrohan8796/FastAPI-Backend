from validate_email import validate_email
from dotenv import dotenv_values
import bcrypt
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

config = dotenv_values()


def validate_signup_data(data):
    errors = []
    error_message = " is required"
    required_fields = ["username", "email", "password"]
    for field in required_fields:
        if data[field] is None or data[field] == "":
            errors.append(field + error_message)
    if (validate_email(data["email"])):
        return errors
    else:
        errors.append("Email format is incorrect")
    return errors


def validate_login_data(data):
    errors = []
    error_message = " is required"
    required_fields = ["email", "password"]
    for field in required_fields:
        if data[field] is None or data[field] == "":
            errors.append(field + error_message)
    if (validate_email(data["email"])):
        return errors
    else:
        errors.append("Email format is incorrect")
    return errors


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def make_new_user_dict(username, email, hashed_password):
    return {
        "username": username,
        "email": email,
        "password": hashed_password,
        "todos": []
    }


def create_access_token(subject: Union[str, Any]) -> str:
    token_expire_mins = config["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"]
    expires_delta = float(
        token_expire_mins) if token_expire_mins is not None else 30
    to_encode = {"exp": datetime.utcnow(
    ) + timedelta(minutes=expires_delta), "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, config["JWT_SECRET_KEY"], config["JWT_ALGORITHM"])
    return encoded_jwt

