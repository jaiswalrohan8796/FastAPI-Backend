from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.user import UserSchema
from utils.utils import validate_signup_data, hash_password, check_password, make_new_user_dict, validate_login_data
from database.mongodb import insert_user, find_user_with_email
# app configurations
templates = Jinja2Templates(directory="templates")
api_router = APIRouter()


# =========== GET Routes ==============

# Home Page (Login)
@api_router.get("/app", tags=["Home"], response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("app.html", {"request": request, "errors": []})
# Signup Page


@api_router.get("/signup", tags=["Signup"], response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "errors": []})

# Login


@api_router.get("/", tags=["Login"], response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "errors": []})

# =============== POST Routes ==========================


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
async def handler_login(request: Request):
    # extract data
    form_data = await request.form()
    # validate data
    errors = validate_login_data(form_data)
    if len(errors) > 0:
        return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
    # extract data
    email = form_data["email"]
    password = form_data["password"]
    # check user exists
    user_exists = await find_user_with_email(email)
    if user_exists is None:
        return templates.TemplateResponse("login.html", {"request": request, "errors": ["User doesn't exist. Please login."]})
    print(user_exists)
    # check password
    is_password_matched = check_password(password, user_exists["password"])
    print(is_password_matched)
    if is_password_matched == False:
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": ["Password incorrect."]})
    else:
        print("Logged in")
        return templates.TemplateResponse("app.html", {"request": request, "errors": []})
