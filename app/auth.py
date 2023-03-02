from typing import Union, Any
from datetime import datetime
from fastapi import Request
from utils.utils import config
from jose import jwt
from pydantic import ValidationError
from database.mongodb import find_user_with_email


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("token")
        if token is None:
            return None
        payload = jwt.decode(
            token, config["JWT_SECRET_KEY"], algorithms=[
                config["JWT_ALGORITHM"]]
        )
        token_data = payload
        if datetime.fromtimestamp(token_data["exp"]) < datetime.now():
            return None
    except (jwt.JWTError, ValidationError) as ex:
        return None

    user = await find_user_with_email(token_data["sub"])
    if user is None:
        return None
    return {"user": user, "token": token}
