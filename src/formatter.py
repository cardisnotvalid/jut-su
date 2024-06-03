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
    kind: str
    series: list[Series]


class Anime(NamedTuple):
    name: str
    episodes: Episodes 
    url: str


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

    # [('/life-no-game/', 'Нет игры - нет жизни'), ('/basilisk/', 'Василиск')]
    def format_search(self, data):
        return self._format(data, "search")

    # [('/life-no-game/episode-1.html', '', '1'), ('/life-no-game/episode-2.html', '', '2'), ('/life-no-game/episode-3.html', '', '3'), ('/life-no-game/episode-4.html', '', '4'), ('/life-no-game/episode-5.html', '', '5'), ('/life-no-game/episode-6.html', '', '6'), ('/life-no-game/episode-7.html', '', '7'), ('/life-no-game/episode-8.html', '', '8'), ('/life-no-game/episode-9.html', '', '9'), ('/life-no-game/episode-10.html', '', '10'), ('/life-no-game/episode-11.html', '', '11'), ('/life-no-game/episode-12.html', '', '12'), ('/life-no-game/film-1.html', '1')]
    def format_episodes(self, data):
        return self._format(data, "episode")

    # [('https://r330101.kujo-jotaro.com/no-game-no-life/4.1080.b22075da4c416efb.mp4?hash1=de1d226a6bd758fcf05674394d485920&hash2=02a16d57e0cc8aa55ab2278a26719acf', 'video/mp4', 'ru', '1080p', '1080'), ('https://r330101.kujo-jotaro.com/no-game-no-life/4.720.f9f8fc2124a988ce.mp4?hash1=ac30b7c19e2a364e5a8a3d7b2cacf2e6&hash2=9e9bdf390db7f7354423053dd3c7a1e4', 'video/mp4', 'ru', '720p', '720'), ('https://r330101.kujo-jotaro.com/no-game-no-life/4.360.f8782881d559ec6e.mp4?hash1=1f5c653d170047aebd2540428a9bc28b&hash2=98ba77ebcbb57c3646e9c1e8e18e7791', 'video/mp4', 'ru', '360p', '360')]
    def format_videos(self, data):
        return self._format(data, "video")
