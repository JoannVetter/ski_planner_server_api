import os

from fastapi import APIRouter, Depends

from src.auth_utils import get_current_active_user
from src.data_fetch.mongo_data_fetcher import MongoDBDataFetcher

# TODO : Add this as a docker secret instead for safer option
mongo_connection_url = os.getenv("MONGO_CONNECTION_URL")
data_fetcher = MongoDBDataFetcher(mongo_connection_url, "ski_planner", "users")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
    responses={200: {"description": "Operation successful"},
               401: {"description": "Couldn't connect to the database, wrong credentials."},
               403: {"description": "Operation not authorized."},
               404: {"description": "User not found."},
               }
)


@router.get("/users/{username}/friends")
async def get_user_friends(username: str):
    return data_fetcher.get_user_friends(username)


@router.get("/users/{username}/equipment")
async def get_user_equipment(username: str):
    return data_fetcher.get_user_equipment(username)