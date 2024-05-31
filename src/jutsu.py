import re
import json
from collections import namedtuple

from selectolax.parser import HTMLParser

from .session import Session

URL_BASE = "https://jut.su"
URL_ANIME = f"{URL_BASE}/anime"

REGEX_FILM = r"\/film-(\d+)"
REGEX_SEASON = r"\/season-(\d+)"
REGEX_EPISODE = r"\/episode-(\d+)"
REGEX_BLOCKED = r"block_video_text"

Search = namedtuple("Search", ["name", "url"])
Video = namedtuple("Video", ["quality", "url"])
Anime = namedtuple("Anime", ["name", "episodes", "url"])
Episode = namedtuple("Episode", ["id", "season", "url"])

class JutSu:
    def __init__(self):
        self.session = Session()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()

    def close(self):
        self.session.close()

    def search(self, query, page=1):
        payload = {
            "ajax_load": "yes",
            "start_from_page": page,
            "show_search": query,
        }
        html = self.session.download_html(URL_ANIME, payload)
        return self.parse_search(html)

    def anime(self, anime):
        html = self.session.download_html(anime.url)
        episodes = self.parse_episodes(html)
        return Anime(name=anime.name, episodes=episodes, url=anime.url)

    def get_episode_videos(self, episode):
        html = self.session.download_html(episode.url)
        return self.parse_video(html)

    @staticmethod
    def parse_search(html):
        tree = HTMLParser(html)
        result = []

        for item in tree.css(".tooltip_of_the_anime"):
            content = HTMLParser(item.attributes["content"])
            body = content.css_first(".tooltip_title_in_anime")

            anime = Search(
                name=body.text(strip=True),
                url=URL_BASE + body.attributes["href"])
            result.append(anime)

        return result

    @staticmethod
    def parse_episodes(html):
        tree = HTMLParser(html)
        episodes = []

        for item in tree.css("a.video"):
            url = URL_BASE + item.attributes["href"]

            id, season = 1, 1
            match_film = re.search(REGEX_FILM, url)
            if match_film:
                id = match_film.group(1)
                season = 0
            else:
                match_season = re.search(REGEX_SEASON, url)
                if match_season:
                    season = match_season.group(1)

                match_id = re.search(REGEX_EPISODE, url)
                if match_id:
                    id = match_id.group(1)

            episode = Episode(id=id, season=season, url=url)
            episodes.append(episode)

        return episodes

    @staticmethod
    def parse_video(html):
        match_blocked = re.findall(REGEX_BLOCKED, html)
        if match_blocked:
            print("Video is not available")
            return None

        tree = HTMLParser(html)
        videos = []

        for item in tree.css("source"):
            attrs = item.attributes
            video = Video(quality=attrs["label"], url=attrs["src"])
            videos.append(video)

        return videos
