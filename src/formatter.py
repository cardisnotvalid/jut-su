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
    resolution: int
    extension: str
    source: str


class DataFormatter:
    def format(self, data):
        pass


class SearchFormatter(DataFormatter):
    def format(self, data):
        return [Search(name=name, url=URL_BASE+url) for url, name in data]


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
            video = Video(
                label=item[3], 
                resolution=item[4], 
                extension=item[1], 
                source=item[0]
            )
            result.append(video)
        return result


class Formatter:
    def __init__(self):
        self.formatters = {
            "search": SearchFormatter,
            "episode": EpisodeFormatter,
            "video": VideoFormatter
        }

    def _get_formatter(self, formatter):
        return self.formatters[formatter]()

    def _format(self, data, formatter):
        return self._get_formatter(formatter).format(data)

    def format_search(self, data):
        return self._format(data, "search")

    def format_episodes(self, data):
        return self._format(data, "episode")

    def format_videos(self, data):
        return self._format(data, "video")
