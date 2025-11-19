from cipher_breaker import CypherBreaker


class SubstitutionCypher(CypherBreaker):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    def break_cypher(self) -> tuple[str, dict[str, str]]:
        return ("", {})
