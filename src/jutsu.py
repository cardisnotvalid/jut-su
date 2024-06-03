from requests import HTTPError

from .paths import URL_ANIME
from .session import BaseSession
from .extractor import Extractor
from .formatter import Search, Episodes, Video


class JutSu:
    def __init__(self):
        self.session = BaseSession()
        self.extractor = Extractor()

    def search_anime(self, query: str, page: int = 1) -> list[Search]:
        data = dict(ajax_load="yes", start_from_page=page, show_search=query)
        try:
            response = self.session.request("POST", URL_ANIME, data=data)
            response.raise_for_status()
            return self.extractor.extract_search_data(response.text)
        except HTTPError:
            raise NotImplementedError

    def get_anime_episodes(self, url: str) -> Episodes:
        try:
            response = self.session.request("GET", url)
            response.raise_for_status()
            return self.extractor.extract_anime_episodes(response.text)
        except HTTPError:
            raise NotImplementedError

    def get_episode_videos(self, url: str) -> list[Video]:
        try:
            response = self.session.request("GET", url)
            response.raise_for_status()
            return self.extractor.extract_videos(response.text)
        except HTTPError:
            raise NotImplementedError
