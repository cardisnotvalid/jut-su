import os
import urllib3
from typing import Dict, Any

from .logger import logger

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}

class Session:
    def __init__(self) -> None:
        self.session = urllib3.PoolManager(headers=headers)

    def __enter__(self) -> "Session":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        self.session.clear()

    def download_html(self, url: str, data: Dict[str, Any] = None) -> str:
        try:
            response = self.session.request("POST", url, fields=data)
            if response.status == 200:
                return response.data.decode("1251")
            
            logger.error(
                "Не удалось установить соединение. Статус: %d (%s)", 
                response.status, response.reason)
            return False
        except Exception as err:
            logger.error("Не удалось получить страницу: %s", err)
            return False

    def download_video(self, url: str, filepath: str) -> None:
        response = self.session.request("GET", url, preload_content=False)
        if response.status != 200:
            logger.error(
                "Не удалось установить соединение. Статус: %d (%s)", 
                response.status, response.reason)
            return False

        content_size = int(response.getheader("Content-Length")) / (1<<20)

        file = open(filepath, "ab")
        if os.path.isfile(filepath):
            file.truncate(0)

        try:
            dd_size = 0
            for chunk in response.stream(65536):
                file.write(chunk)
                dd_size += len(chunk) / (1<<20)
                logger.info(
                    "Скачано: [%.2fMB / %.2fMB]\033[0K\033[1A",
                    dd_size, content_size)
            return True
        except Exception as err:
            logger.error("Не удалось скачать видео: %s", err)
            return False
        finally:
            response.release_conn()
            file.close()
