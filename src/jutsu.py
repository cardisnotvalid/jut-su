import re
from typing import NamedTuple
from urllib.parse import urlparse

from selectolax.parser import HTMLParser

from .session import Session
from .exceptions import CantGetSourceVideo, SourceVideoIsBlocked
from .logger import logger


class Video(NamedTuple):
    quality: str
    ext: str
    url: str

class Episode(NamedTuple):
    id: str
    season: str
    url: str

class Anime(NamedTuple):
    name: str
    episodes: list[Episode]
    url: str


class JutSu:
    url_base = "https://jut.su"
    url_anime = url_base + "/anime"

    def __init__(self, session: Session = None):
        self.session = session or Session()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.session.close()

    def _get_search_content(self, content: str) -> tuple[str, str]:
        body = HTMLParser(content).css_first(".tooltip_title_in_anime")
        return (body.text(strip=True),
                self.url_base + body.attributes["href"])

    def _extract_search(self, html: str) -> list[Anime]:
        tree = HTMLParser(html)
        result = []
        for item in tree.css(".tooltip_of_the_anime"):
            (name, url) = self._get_search_content(item.attributes["content"])
            result.append(Anime(name, [], url))
        return result

    def search(self, query: str, page: int = 1) -> list[Anime]:
        html = self.session.get_html_content(
            self.url_anime, 
            data=dict(ajax_load="yes", show_search=query, start_from_page=page))
        return self._extract_search(html)

    def _find_match(self, pattern: str, string: str) -> str | None:
        match = re.search(pattern, string)
        return match.group(1) if match else None

    def _get_film_id(self, string: str) -> str | None:
        return self._find_match(r"\/film-(\d+)", string)

    def _get_season_id(self, string: str) -> str | None:
        return self._find_match(r"\/season-(\d+)", string)

    def _get_episode_id(self, string: str) -> str | None:
        return self._find_match(r"\/episode-(\d+)", string)

    def _get_episode_season(self, url: str):
        episode_id = season = 1
        if film_id := self._get_film_id(url):
            episode_id = film_id
            season = 0
        else:
            if season_id := self._get_season_id(url):
                season = season_id
            if episode_id := self._get_episode_id(url):
                episode_id = episode_id
        return (episode_id, season)

    def _extract_episodes(self, html: str):
        episodes = []
        for item in HTMLParser(html).css("a.video"):
            url = self.url_base + item.attributes["href"]
            (episode_id, season) = self._get_episode_season(url)
            episodes.append(Episode(str(episode_id), str(season), url))
        return episodes

    def get_anime(self, anime: Anime) -> Anime:
        html = self.session.get_html_content(anime.url)
        episodes = self._extract_episodes(html)
        return Anime(anime.name, episodes, anime.url)

    def _parse_video_attrs(self, source: dict[str, str]) -> tuple[str, ...]:
        try:
            quality = source["label"]
            url = source["src"]
            ext = urlparse(url).path.rsplit(".", 1)[-1]
            return (quality, ext, url)
        except KeyError:
            raise CantGetSourceVideo

    def _extract_videos(self, html: str) -> list[Video]:
        videos = []
        for item in HTMLParser(html).css("source"):
            (quality, ext, url) = self._parse_video_attrs(item.attributes)
            videos.append(Video(quality, ext, url))
        return videos

    def _check_is_video_blocked(self, html: str):
        if re.findall(r"block_video_text", html):
            raise SourceVideoIsBlocked

    def get_episode_video(self, episode: Episode) -> list[Video]:
        html = self.session.get_html_content(episode.url)
        self._check_is_video_blocked(html)
        return self._extract_videos(html)
