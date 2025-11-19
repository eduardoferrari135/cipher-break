from abc import ABC, abstractmethod


class CypherBreaker(ABC):
    @abstractmethod
    def __init__(self, message: str) -> None:
        self.message = message

    @abstractmethod
    def break_cypher(self) -> tuple[str, dict[str, str]]:
        pass
