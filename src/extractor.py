import re
from abc import ABC, abstractmethod
from typing import NamedTuple, TypedDict, Optional

from .paths import URL_BASE


class VideoInfo(NamedTuple):
    src: str
    type_: str
    language: str
    label: str
    resolution: str


class SearchInfo(NamedTuple):
    url: str
    name: str


class Film(NamedTuple):
    id: str
    url: str


class Episode(NamedTuple):
    id: str
    url: str


class Episodes(TypedDict):
    season_id: str
    series: list[Episode | Film]


class AnimeInfo(NamedTuple):
    name: str
    episodes: Episodes 
    url: str


class InfoExtractor:
    def _find_matches(self, string: str):
        try:
            match = re.findall(self._REGEX, string)
            return match
        except Exception as err:
            raise NotImplementedError(err)

    def extract(self, string: str):
        pass


class SeasonExtractor(InfoExtractor):
    _REGEX = 'href="(?P<url>/[^/]+(?:/season-(?P<season>\d+)|)/episode-(?P<episode>\d+)\.html)"'

    def extract(self, string: str):
        matches = self._find_matches(string)
        episodes = {}
        for url, season, episode_id in matches:
            if not season:
                season = "1"
            if season not in episodes:
                episodes[season] = []
            episode = Episode(episode_id, URL_BASE + url)
            episodes[season].append(episode)
        return Episodes(**episodes)


class FilmExtractor(InfoExtractor):
    _REGEX = r'href="(?P<url>/[^/]+/film-(?P<film>\d+)\.html)"'

    def extract(self, string: str):
        matches = self._find_matches(string)
        episodes = {"0": []}
        for url, film_id in matches:
            film = Film(film_id, URL_BASE + url)
            episodes["0"].append(film)
        return Episodes(**episodes)


class VideoExtractor(InfoExtractor):
    _REGEX = '<source src="(?P<src>[^"]+)" type="(?P<type>[^"]+)" lang="(?P<lang>[^"]+)" label="(?P<label>[^"]+)" res="(?P<res>[^"]+)"/>' 

    def extract(self, string: str) -> VideoInfo:
        matches = self._find_matches(string)
        return [VideoInfo(*match) for match in matches]


class AnimeExtractor(InfoExtractor):
    _REGEX = '"tooltip_pad_in_anime"><a href="(?P<href>[^"]+)" class="[^"]+">(?P<title>[^<]+)'

    def extract(self, string: str):
        matches = self._find_matches(string)
        return [SearchInfo(URL_BASE + url, name) for url, name in matches]


class Extractor:
    def __init__(self,
                 anime_extractor: InfoExtractor = AnimeExtractor(),
                 season_extractor: InfoExtractor = SeasonExtractor(),
                 film_extractor: InfoExtractor = FilmExtractor(),
                 video_extractor: InfoExtractor = VideoExtractor()):
        self.anime_extractor = anime_extractor
        self.season_extractor = season_extractor
        self.film_extractor = film_extractor
        self.video_extractor = video_extractor

    def extract_search_data(self, content: str):
        return self.anime_extractor.extract(content)

    def extract_anime_episodes(self, content: str):
        episodes = self.season_extractor.extract(content)
        episodes.update(self.film_extractor.extract(content))
        return episodes

    def extract_videos(self, content: str):
        return self.video_extractor.extract(content)

