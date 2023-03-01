from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

# app configurations
templates = Jinja2Templates(directory="templates")
api_router = APIRouter()


# =========== GET Routes ==============

# Home Page (Login)
@api_router.get("/", tags=["Home"])
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
# Login
@api_router.get("/login", tags=["Login"])
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
# Signup Page
@api_router.get("/signup", tags=["Signup"])
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# =============== POST Routes ==========================

