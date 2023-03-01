from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.user import UserSchema
from utils.utils import validate_signup_data, hash_password, check_password, make_new_user_dict, validate_login_data, create_access_token
from database.mongodb import insert_user, find_user_with_email
from app.auth import get_current_user
# app configurations
templates = Jinja2Templates(directory="templates")
api_router = APIRouter()


# ===================== Un-protected routes =========================


@api_router.get("/signup", tags=["Signup"], response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "errors": []})


@api_router.get("/", tags=["Login"], response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "errors": []})


@api_router.post("/signup")
async def handle_signup(request: Request):
    # extract form data
    signup_data = await request.form()
    # validate form data
    errors = validate_signup_data(signup_data)
    if len(errors) > 0:
        return templates.TemplateResponse("signup.html", {"request": request, "errors": errors})
    # split fields
    username = signup_data["username"]
    email = signup_data["email"]
    password = signup_data["password"]
    # check if user already exists
    is_already_user = await find_user_with_email(email)
    if is_already_user is not None:
        return templates.TemplateResponse("signup.html", {"request": request, "errors": ["Email already present. Login instead"]})
    # hash password
    password = hash_password(password)
    # make new user dict
    new_user = make_new_user_dict(username, email, password)
    # insert user into mongodb
    insert_ack = await insert_user(new_user)
    if insert_ack is False:
        return templates.TemplateResponse("signup.html", {"request": request, "errors": ["Internal Server Error"]})
    print(f"{username} named new user created !")
    return templates.TemplateResponse("login.html", {"request": request, "errors": []})


@api_router.post("/login")
async def handle_login(request: Request):
    form_data = await request.form()
    email = form_data["email"]
    password = form_data["password"]
    # validate login data
    errors = validate_login_data(form_data)
    if len(errors) > 0:
        return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
    user = await find_user_with_email(email)
    if user == None:
        return templates.TemplateResponse("login.html", {"request": request, "errors": ["User doesn't exist."]})
    is_password_matched = check_password(password, user["password"])
    if is_password_matched == False:
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": ["Password incorrect."]})
    access_token = create_access_token(email)
    response = templates.TemplateResponse(
        "app.html", {"request": request, "user": user,  "token": access_token})
    response.set_cookie("token", access_token)
    return response


# ============== Protected Routes ==============

@api_router.get("/app")
async def handle_app(request: Request, user=Depends(get_current_user)):
    if user is None:
        return templates.TemplateResponse("login.html", {"request": request, "errors": ["Authentication failed. Login"]})
    response = templates.TemplateResponse(
        "app.html", {"request": request, "user": user["user"],  "token": user["token"]})
    response.set_cookie("token", user["token"])
    return response
