import json
from typing import List, Dict

from interface_data_fetcher import DataFetcherInterface


class FakeDataFetcher(DataFetcherInterface):

    def __init__(self, filename):
        self.filename = filename

    def _get_user_data(self, user) -> Dict:
        with open(self.filename, "r") as data_file:
            whole_data = json.load(data_file)
        user_data = whole_data.get("users").get(user)

        if user_data is None:
            raise AttributeError("User does not exist.")
        else:
            return user_data

    def get_user_friends(self, user) -> List:
        user_data = self._get_user_data(user)
        return user_data.get("friends")

    def get_user_equipment(self, user: str) -> Dict:
        user_data = self._get_user_data(user)
        return user_data.get("equipment")