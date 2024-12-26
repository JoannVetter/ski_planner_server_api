import os

import uvicorn
from fastapi import FastAPI

from mongo_data_fetcher import MongoDBDataFetcher

app = FastAPI()

# For testing purposes uniquely
mongo_connection_url = os.getenv("MONGO_CONNECTION_URL")
data_fetcher = MongoDBDataFetcher(mongo_connection_url, "ski_planner", "users")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/{username}/friends")
async def get_user_friends(username: str):
    return data_fetcher.get_user_friends(username)

@app.get("/users/{username}/equipment")
async def get_user_equipment(username: str):
    return data_fetcher.get_user_equipment(username)

if __name__ == "__main__":
    uvicorn.run(app)