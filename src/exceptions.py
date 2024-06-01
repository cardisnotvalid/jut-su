class ResponseStatusCodeError(Exception):
    def __init__(self, status_code: int, reason: str | None = None):
        self.status_code = status_code
        self.reason = reason

    def __str__(self) -> str:
        return f"Статус: {self.status_code} ({self.reason})"

class CantGetRequestContent(Exception):
    pass

class CantGetSourceVideo(Exception):
    pass

class SourceVideoIsBlocked(Exception):
    pass
