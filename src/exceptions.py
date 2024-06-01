class ResponseStatusCodeError(Exception):
    def __init__(self, status_code: int, reason: str):
        self.status_code = status_code
        self.reason = reason

    def __str__(self) -> str:
        return f"Статус: {self.status_code} ({self.reason})"

class CantGetRequestContent(Exception):
    pass

