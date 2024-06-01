import os
import urllib3
from urllib3.response import BaseHTTPResponse
from urllib3.exceptions import HTTPError
from typing import Literal, Generator

from .exceptions import CantGetRequestContent, ResponseStatusCodeError
from .logger import logger


DEFAULT_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

RequestMethod = Literal["GET", "POST"]


class Session:
    def __init__(self, headers: dict[str, str] | None = {}):
        self.headers = {"User-Agent": DEFAULT_USER_AGENT}
        self.headers.update(headers)

        self.session = urllib3.PoolManager(headers=headers)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.session.clear()

    def _request(self, method: RequestMethod, url: str, **kwargs) -> BaseHTTPResponse:
        try:
            response = self.session.request(method, url, **kwargs)
            self._check_response_status(response)
            return response
        except HTTPError:
            raise CantGetRequestContent

    def _check_response_status(self, response: BaseHTTPResponse):
        if response.status != 200:
            raise ResponseStatusCodeError(response.status, response.reason)

    def _post(self, url: str, data: dict[str, any]) -> BaseHTTPResponse:
        return self._request("POST", url, **{"fields": data})

    def _get(self, url: str, **kwargs) -> BaseHTTPResponse:
        return self._request("GET", url, **kwargs)

    def _open_response_stream(self, response: BaseHTTPResponse) -> Generator[bytes, None, None]:
        size_content = self._get_response_content_size(response)
        size_download = 0.0
        for chunk in response.stream(65535):
            size_download += len(chunk) / (1<<20)
            yield chunk
            logger.info("%.2fMB / %.2fMB\033[K\033[1A", size_download, size_content)

    def _get_response_content_size(self, response: BaseHTTPResponse) -> float:
        content_length = response.getheader("Content-Length")
        return int(content_length) / (1<<20)

    def _write_video(self, response: BaseHTTPResponse, filepath: str) -> None:
        if os.path.isfile(filepath):
            with open(filepath, "wb") as file:
                file.truncate(0)

        with open(filepath, "ab") as f:
            for chunk in self._open_response_stream(response):
                f.write(chunk)

    def get_html_content(self, url: str, data: dict[str, any] | None = None) -> str:
        response = self._post(url, data) if data else self._get(url)
        return response.data.decode("1251")

    def download_video(self, url: str, filepath: str):
        try:
            response = self._get(url, **{"preload_content": False})
            self._write_video(response, filepath)
        finally:
            response.release_conn()
