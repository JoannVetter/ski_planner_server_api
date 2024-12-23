from fastapi import FastAPI

from fake_data_fetcher import FakeDataFetcher

app = FastAPI()

# For testing purposes uniquely
data_fetcher = FakeDataFetcher("./fake_data.json")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/{username}/friends")
async def get_user_friends(username: str):
    return data_fetcher.get_user_friends(username)

@app.get("/users/{username}/equipment")
async def get_user_equipment(username: str):
    return data_fetcher.get_user_inventory(username)