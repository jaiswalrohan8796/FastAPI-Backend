from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import api_router
from database.mongodb import MONGODB_CLIENT, config


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)


@app.on_event("startup")
async def startup_mongodb():
    app.mongodb_client = MONGODB_CLIENT
    app.db = app.mongodb_client[config["DB_NAME"]]
    print("Connected to MongoDB")


@app.on_event("shutdown")
async def shutdown_mongodb():
    app.mongodb_client.close()
    print("Disconnected to MongoDB")
