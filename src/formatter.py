from typing import NamedTuple, TypedDict

from .paths import URL_BASE


class Series(NamedTuple):
    id: str
    url: str


class Film(Series):
    pass


class Episode(Series):
    pass


class Episodes(TypedDict):
    id: str
    series: list[Series]


class Search(NamedTuple):
    name: str
    url: str


class Video(NamedTuple):
    label: str
    source: str


class DataFormatter:
    try:
        def format(self, data):
            pass
    except Exception as err:
        raise NotImplementedError(err)


class SearchFormatter(DataFormatter):
    def format(self, data):
        result = []
        for url, name in data:
            result.append(Search(name, URL_BASE + url))
        return result


class EpisodeFormatter(DataFormatter):
    def format(self, data):
        result = {}
        for item in data:
            if len(item) == 3:
                (url, season, episode) = item
                if not season:
                    season = "1"
                if season not in result:
                    result[season] = []
                result[season].append(Episode(episode, URL_BASE + url))
            elif len(item) == 2:
                (url, film) = item
                if "0" not in result:
                    result["0"] = []
                result["0"].append(Film(film, URL_BASE + url))
            else:
                raise NotImplementedError("Unknown episode")
        return Episodes(**result)


class VideoFormatter(DataFormatter):
    def format(self, data):
        result = []
        for item in data:
            result.append(Video(label=item[1], source=item[0]))
        return result


class Formatter:
    def _format(self, data, formatter):
        return formatter.format(data)

    def format_search(self, data):
        return self._format(data, SearchFormatter())

    def format_episodes(self, data):
        return self._format(data, EpisodeFormatter())

    def format_videos(self, data):
        return self._format(data, VideoFormatter())
