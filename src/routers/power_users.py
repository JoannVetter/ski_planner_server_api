import os

from fastapi import APIRouter, Depends

from src.auth_utils import get_current_active_user
from src.data_fetch.mongo_data_fetcher import MongoDBDataFetcher
from src.models import PowerUser

router = APIRouter(
    prefix="/power_users",
    tags=["power_users"],
    dependencies=[Depends(get_current_active_user)],
    responses={200: {"description": "Operation successful"},
               401: {"description": "Couldn't connect to the database, wrong credentials."},
               403: {"description": "Operation not authorized."},
               404: {"description": "User not found."},
               }
)

# TODO : Add this as a docker secret instead for safer option
mongo_connection_url = os.getenv("MONGO_CONNECTION_URL")
data_fetcher = MongoDBDataFetcher(mongo_connection_url, "ski_planner", "power_users")


@router.post("/power_user/add/")
async def add_power_user(new_power_user: PowerUser, new_password: str):
    ...


@router.post("/power_user/modify/")
async def modify_power_user_password(new_power_user: PowerUser, new_password: str):
    ...


@router.post("/power_user/delete/")
async def delete_power_user(new_power_user: PowerUser, new_password: str):
    ...


@router.post("/power_user/disable/")
async def disable_power_user(new_power_user: PowerUser, new_password: str):
    ...
