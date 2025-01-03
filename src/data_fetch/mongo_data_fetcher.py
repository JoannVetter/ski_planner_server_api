from typing import Dict, List

import pymongo
from pymongo.errors import OperationFailure
from fastapi import HTTPException

from .interface_data_fetcher import DataFetcherInterface


class MongoDBDataFetcher(DataFetcherInterface):

    def __init__(self, connection_url, db_name, collection_name):
        self.client = pymongo.MongoClient(connection_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_user_data(self, user: str) -> Dict:
        query = {"username": user}
        try:
            user_data = self.collection.find(query)[0]
        except IndexError:
            raise HTTPException(status_code=404, detail="User not found.")
        except OperationFailure:
            raise HTTPException(status_code=401, detail="Couldn't connect to the database, wrong credentials.")
        return user_data

    def get_user_specific(self, user:str, specific: str, return_type: type):
        specific_data = self.get_user_data(user).get(specific)
        return specific_data if specific_data is not None else return_type()

    def get_user_equipment(self, user: str) -> Dict:
        return self.get_user_specific(user, "equipment", return_type=Dict)

    def get_user_friends(self, user: str) -> List:
        return self.get_user_specific(user, "friends", return_type=List)

