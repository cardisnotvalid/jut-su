import re

from .paths import URL_BASE
from .formatter import Formatter


class InfoExtractor:
    _REGEX = r""

    def _find_matches(self, string):
        try:
            match = re.findall(self._REGEX, string)
            return match
        except Exception as err:
            raise NotImplementedError(err)

    def extract(self, string):
        pass


class SeasonExtractor(InfoExtractor):
    _REGEX = 'href="(?P<url>/[^/]+(?:/season-(?P<season>\d+)|)/episode-(?P<episode>\d+)\.html)"'

    def extract(self, string):
        return self._find_matches(string)

class FilmExtractor(InfoExtractor):
    _REGEX = r'href="(?P<url>/[^/]+/film-(?P<film>\d+)\.html)"'

    def extract(self, string):
        return self._find_matches(string)


class VideoExtractor(InfoExtractor):
    _REGEX = '<source src="(?P<src>[^"]+)" type="(?P<type>[^"]+)" lang="(?P<lang>[^"]+)" label="(?P<label>[^"]+)" res="(?P<res>[^"]+)"/>' 

    def extract(self, string):
        return self._find_matches(string)


class AnimeExtractor(InfoExtractor):
    _REGEX = '"tooltip_pad_in_anime"><a href="(?P<href>[^"]+)" class="[^"]+">(?P<title>[^<]+)'

    def extract(self, string):
        return self._find_matches(string)


class Extractor:
    def __init__(self):
        self.extractors = {
            "season": SeasonExtractor, 
            "film": FilmExtractor, 
            "video": VideoExtractor,
            "anime": AnimeExtractor
        }
        self.formatter = Formatter()

    def _get_extractor(self, name):
        return self.extractors[name]()

    def _extract(self, content, extractor):
        return self._get_extractor(extractor).extract(content)

    def extract_search_data(self, content):
        data = self._extract(content, "anime")
        return self.formatter.format_search(data)

    def extract_anime_episodes(self, content):
        episodes = self._extract(content, "season")
        episodes.extend(self._extract(content, "film"))
        return self.formatter.format_episodes(episodes)

    def extract_videos(self, content):
        data = self._extract(content, "video")
        return self.formatter.format_videos(data)

