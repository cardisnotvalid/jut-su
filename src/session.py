import time
import urllib3
from typing import Dict, Any

from .logger import logger
from .utils import reset_file

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
            else:
                logger.error(
                    "Не удалось установить соединение. Статус: %d (%s)", 
                    response.status, response.reason)
                return False
        except Exception as err:
            logger.error("Не удалось получить страницу: %s", err)
            return False

    def download_video(self, url: str, filepath: str) -> None:
        try:
            response = self.session.request("GET", url, preload_content=False)
            if response.status != 200:
                logger.error(
                    "Не удалось установить соединение. Статус: %d (%s)", 
                    response.status, response.reason)
                return False

            content_length = response.getheader("Content-Length")
            c_size = int(content_length) / (1<<20)
            d_size = 0.0

            reset_file(filepath)

            with open(filepath, "ab") as file:
                start_time = time.perf_counter()
                for chunk in response.stream(65535):
                    if chunk:
                        file.write(chunk)
                        d_size += len(chunk) / (1<<20)
                        elapsed_time = time.perf_counter() - start_time
                        speed = d_size / elapsed_time if elapsed_time > 0 else 0
                        logger.info(
                            "%.2fMB / %.2fMB [%.2fMB/s]\033[K\033[1A",
                            d_size, c_size, speed)
            return True
        except Exception as err:
            logger.error("Не удалось скачать видео: %s", err)
            return False
        finally:
            response.release_conn()
