from abc import abstractmethod
from typing import Dict, List


class DataFetcherInterface:

    @abstractmethod
    def get_user_equipment(self, user: str) -> Dict:
        ...

    def get_user_friends(self, user: str) -> List:
        ...
