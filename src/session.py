import requests

DEFAULT_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

class Session(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers["User-Agent"] = DEFAULT_USER_AGENT

    def download_html(self, url, payload=None):
        return self.post(url, data=payload).text

