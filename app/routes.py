from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

# app configurations
templates = Jinja2Templates(directory="templates")
api_router = APIRouter()


# =========== Routes ==============

# Home Page (Login)
@api_router.get("/", tags=["Home"])
async def home(request: Request):
	return templates.TemplateResponse("login.html", {"request": request})

# Signup Page
@api_router.post("/signup", tags=["Signup"])
async def signup(data, request: Request):
	return templates.TemplateResponse("signup.html", {"data": data})

