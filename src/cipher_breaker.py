from abc import ABC, abstractmethod
from typing import List


class CypherBreaker(ABC):
    @abstractmethod
    def __init__(self, message: str) -> None:
        self.message = message

    @staticmethod
    @abstractmethod
    def encrypt(text: str, key) -> str:
        pass

    @abstractmethod
    def break_cypher(self) -> tuple[str, dict[str, str]]:
        pass
