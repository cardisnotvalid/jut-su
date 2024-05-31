import re
from urllib.parse import urlparse
from typing import List, Dict, Any

from selectolax.parser import HTMLParser

from .models import *
from .logger import logger
from .session import Session

class JutSu:
    url_base = "https://jut.su"
    url_anime = url_base + "/anime"

    def __init__(self, session: Session = None) -> None:
        self.session = session or Session()
    
    def __enter__(self) -> "JutSu":
        return self
    
    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        self.session.close()

    def search(self, query: str, page: int = 1) -> List[Search]:
        payload = {
            "ajax_load": "yes",
            "show_search": query,
            "start_from_page": page}
        html = self.session.download_html(self.url_anime, payload)
        if not html:
            logger.error("Не удалось выполнить поиск")
            return False

        tree = HTMLParser(html)
        result = []
        for item in tree.css(".tooltip_of_the_anime"):
            content = HTMLParser(item.attributes["content"])
            body = content.css_first(".tooltip_title_in_anime")

            name = body.text(strip=True)
            url = self.url_base + body.attributes["href"]
            result.append(Search(name=name, url=url))

        return result

    def get_anime(self, anime: Search) -> Anime:
        html = self.session.download_html(anime.url)
        if not html:
            logger.error("Не удалось получить аниме")
            return False

        tree = HTMLParser(html)
        episodes = []
        for item in tree.css("a.video"):
            url = self.url_base + item.attributes["href"]
            id, season = 1, 1

            m_film = re.search(r"\/film-(\d+)", url)
            if m_film:
                id = m_film.group(1)
                season = 0
            else:
                m_season = re.search(r"\/season-(\d+)", url)
                if m_season:
                    season = m_season.group(1)

                m_id = re.search(r"\/episode-(\d+)", url)
                if m_id:
                    id = m_id.group(1)
            episodes.append(Episode(id=str(id), season=str(season), url=url))

        return Anime(name=anime.name, episodes=episodes, url=anime.url)

    def get_episode_video(self, episode: Episode) -> List[Video]:
        html = self.session.download_html(episode.url)
        if not html:
            logger.error("Не удалось получить видео")
            return False

        m_blocked = re.findall(r"block_video_text", html)
        if m_blocked:
            logger.error("Видео недоступно")
            return False

        tree = HTMLParser(html)
        videos = []

        for item in tree.css("source"):
            quality = item.attributes["label"]
            url = item.attributes["src"]
            ext = urlparse(url).path.rsplit(".", 1)[-1]
            videos.append(Video(quality=quality, ext=ext, url=url))

        return videos
