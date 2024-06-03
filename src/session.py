import requests

DEFAULT_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

class BaseSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers["User-Agent"] = DEFAULT_USER_AGENT

