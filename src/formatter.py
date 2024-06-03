from typing import NamedTuple, TypedDict

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


class Formatter:
    # [('/life-no-game/', 'Нет игры - нет жизни'), ('/basilisk/', 'Василиск')]
    def format_search(self, data):
        return [SearchInfo(URL_BASE + url, name) for url, name in data]

    # [('/life-no-game/episode-1.html', '', '1'), ('/life-no-game/episode-2.html', '', '2'), ('/life-no-game/episode-3.html', '', '3'), ('/life-no-game/episode-4.html', '', '4'), ('/life-no-game/episode-5.html', '', '5'), ('/life-no-game/episode-6.html', '', '6'), ('/life-no-game/episode-7.html', '', '7'), ('/life-no-game/episode-8.html', '', '8'), ('/life-no-game/episode-9.html', '', '9'), ('/life-no-game/episode-10.html', '', '10'), ('/life-no-game/episode-11.html', '', '11'), ('/life-no-game/episode-12.html', '', '12'), ('/life-no-game/film-1.html', '1')]
    def format_episodes(self, data):
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

    # [('https://r330101.kujo-jotaro.com/no-game-no-life/4.1080.b22075da4c416efb.mp4?hash1=de1d226a6bd758fcf05674394d485920&hash2=02a16d57e0cc8aa55ab2278a26719acf', 'video/mp4', 'ru', '1080p', '1080'), ('https://r330101.kujo-jotaro.com/no-game-no-life/4.720.f9f8fc2124a988ce.mp4?hash1=ac30b7c19e2a364e5a8a3d7b2cacf2e6&hash2=9e9bdf390db7f7354423053dd3c7a1e4', 'video/mp4', 'ru', '720p', '720'), ('https://r330101.kujo-jotaro.com/no-game-no-life/4.360.f8782881d559ec6e.mp4?hash1=1f5c653d170047aebd2540428a9bc28b&hash2=98ba77ebcbb57c3646e9c1e8e18e7791', 'video/mp4', 'ru', '360p', '360')]
    def format_videos(self, data):
        return [VideoInfo(*item) for item in data]
