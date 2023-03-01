from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import api_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router)
