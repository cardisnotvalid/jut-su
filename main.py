from urllib.parse import urlparse

import questionary
from questionary import Choice

from src.paths import DIR_OUTPUT
from src.session import Session
from src.jutsu import JutSu, Anime, Season, Video
from src.logger import logger


def quest_search(jutsu: JutSu) -> list[Anime]:
    search_answer = questionary.text("Поиск:").ask()
    if not search_answer:
        questionary.print("Вы ничего не ввели. Введите название аниме")
        return quest_search(jutsu)
    if search_answer == "q":
        exit(0)
    search_result = jutsu.search(search_answer)
    if not search_result:
        questionary.print("Ничего не найдено")
        action = questionary.select(
            "Действие:", 
            choices=["Поиск", "Выйти"]
        ).ask()
        if action == "Поиск":
            return quest_search(jutsu)
        else:
            exit(0)
    return search_result


def quest_anime(jutsu, animes: list[Anime]) -> Anime:
    anime = questionary.select(
        "Выбрите аниме:", 
        choices=[Choice(item["name"], item) for item in animes]
    ).ask()
    return jutsu.get_anime(anime)


def quest_episode(jutsu, anime: Anime) -> tuple[str, str]:
    season_id = questionary.select(
        "Выберите сезон:",
        choices=anime["episodes"]
    ).ask()
    episode_url = questionary.select(
        "Выберите эпизод:",
        choices=[
            Choice(str(i+1), anime["episodes"][season_id][i]) 
            for i in range(len(anime["episodes"][season_id]))
        ]
    ).ask()
    return (season_id, episode_url)


def quest_video(jutsu: JutSu, url: str) -> str:
    vidoes = jutsu.get_episode_videos(url)
    return questionary.select(
        "Выберите качество видео:",
        choices=[Choice(video.quality, video.url) for video in vidoes]
    ).ask()


if __name__ == "__main__":
    jutsu = JutSu()
    try:
        finded_animes = quest_search(jutsu)
        anime = quest_anime(jutsu, finded_animes)
        (season_id, episode_url) = quest_episode(jutsu, anime)
        video_url = quest_video(jutsu, episode_url)

        dir_anime = DIR_OUTPUT / anime["name"]
        dir_season = dir_anime / f"Сезон {season_id}"
        dir_season.mkdir(parents=True, exist_ok=True)

        parsed_video_url = urlparse(video_url)
        url_info = parsed_video_url.path.rsplit("/", 1)[-1]
        episode_id, *_, video_ext = url_info.split(".")

        file_name = f"{episode_id}.{video_ext}"
        file_path = dir_season / file_name

        jutsu.session.download_video(video_url, file_path)
        logger.info(
            "%s. Сезон %s. Эпизод %s успешно скачалось", 
            anime["name"], season_id, file_name
        )
    finally:
        jutsu.close()

