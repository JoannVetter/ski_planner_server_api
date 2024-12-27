from typing import Dict, List

import pymongo
from fastapi import HTTPException

from .interface_data_fetcher import DataFetcherInterface


class MongoDBDataFetcher(DataFetcherInterface):

  def __init__(self, connection_url, db_name, collection_name):
    self.client = pymongo.MongoClient(connection_url)
    self.db = self.client[db_name]
    self.collection = self.db[collection_name]


  def _get_user_data(self, user: str) -> Dict:
    query = {"username": user}
    try:
      user_data = self.collection.find(query)[0]
    except IndexError:
      return {}
    return user_data

  def get_user_equipment(self, user: str) -> Dict:
    user_data = self._get_user_data(user)
    if not user_data:
      raise HTTPException(status_code=404, detail="User not found.")
    return user_data.get("equipment", {})


  def get_user_friends(self, user: str) -> List | Dict:
    user_data = self._get_user_data(user)
    if not user_data:
      raise HTTPException(status_code=404, detail="User not found.")
    return user_data.get("friends")
