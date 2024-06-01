import re
from typing import NamedTuple, TypedDict, Any
from urllib.parse import urlparse

from selectolax.parser import HTMLParser, Node

from .session import Session
from .exceptions import CantGetSourceVideo, SourceVideoIsBlocked
from .logger import logger


URL_BASE = "https://jut.su"
URL_ANIME = URL_BASE + "/anime"


class Video(NamedTuple):
    quality: str
    ext: str
    url: str

class Season(TypedDict):
    season_id: str
    episodes: list[str]

class Anime(TypedDict):
    name: str
    episodes: list[Season]
    url: str


class Parser:
    @staticmethod
    def _get_node_attr(node: Node, attribute: str) -> str:
        try:
            return node.attributes[attribute] or ""
        except KeyError:
            raise CantGetSourceVideo(f"")

    def _parse_search_info(self, html: str):
        body = HTMLParser(html).css_first(".tooltip_title_in_anime")
        name = body.text(strip=True)
        url = URL_BASE + self._get_node_attr(body, "href")
        return (name, url)

    def get_search_animes(self, html: str) -> list[Anime]:
        animes = []
        for item in HTMLParser(html).css(".tooltip_of_the_anime"):
            content = self._get_node_attr(item, "content")
            (anime_name, anime_url) = self._parse_search_info(content)
            anime = Anime(name=anime_name, episodes=[], url=anime_url)
            animes.append(anime)
        return animes

    def _find_match(self, pattern: str, string: str) -> str | None:
        match = re.search(pattern, string)
        return match.group(1) if match else None

    def _get_season_id(self, url: str) -> str:
        season_id = "1"
        if self._find_match(r"\/film-(\d+)", url):
            season_id = "0"
        else:
            if match_season := self._find_match(r"\/season-(\d+)", url):
                season_id = match_season or ""
        return season_id

    def get_anime_episodes(self, html: str) -> Season:
        episodes = {}
        for item in HTMLParser(html).css("a.video"):
            url = URL_BASE + self._get_node_attr(item, "href")
            season_id = self._get_season_id(url)
            if season_id not in episodes:
                episodes[season_id] = []
            episodes[season_id].append(url)
        return Season(**episodes)

    def _parse_video_attrs(self, source: Node) -> tuple[str, ...]:
        try:
            quality = self._get_node_attr(source, "label")
            url = self._get_node_attr(source, "src")
            ext = urlparse(url).path.rsplit(".", 1)[-1]
            return (quality, ext, url)
        except KeyError:
            raise CantGetSourceVideo

    def check_is_video_blocked(self, html: str):
        if re.findall(r"block_video_text", html):
            raise SourceVideoIsBlocked

    def get_videos(self, html: str) -> list[Video]:
        return [Video(*self._parse_video_attrs(item)) 
                for item in HTMLParser(html).css("source")]


class JutSu:
    def __init__(self, session: Session | None = None):
        self.session = session or Session()
        self.parser = Parser()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.session.close()

    def search(self, query: str, page: int = 1) -> list[Anime]:
        payload = dict(ajax_load="yes", show_search=query, start_from_page=page)
        html = self.session.get_html_content(URL_ANIME, payload)
        return self.parser.get_search_animes(html)

    def get_anime(self, anime: Anime) -> Anime:
        html = self.session.get_html_content(anime["url"])
        episodes = self.parser.get_anime_episodes(html)
        anime["episodes"] = episodes
        return anime

    def get_episode_videos(self, url: str) -> list[Video]:
        html = self.session.get_html_content(url)
        self.parser.check_is_video_blocked(html)
        return self.parser.get_videos(html)
