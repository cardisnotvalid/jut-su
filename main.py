import os
from typing import List
from collections import defaultdict

import questionary

from src.models import *
from src.jutsu import JutSu
from src.logger import logger
from src.session import Session
from src.utils import create_anime_dir

def quest_search(jutsu: JutSu) -> Search:
    search_answer = questionary.text("Поиск:").ask()
    if not search_answer:
        questionary.print("Вы ничего не ввели. Введите название аниме")
        return quest_search(jutsu)

    if search_answer == "q":
        exit(0)

    r_search = jutsu.search(search_answer)
    if not r_search:
        if r_search is False:
            questionary.print("Произошла ошибка")
            exit(1)
        else:
            questionary.print("Ничего не найдено")

        action_answer = questionary.select(
            "Действие:", 
            choices=["Поиск", "Выйти"]).ask()
        if action_answer == "Поиск":
            return quest_search(jutsu)
        else:
            exit(0)

    return r_search

def quest_anime(jutsu, data: List[Search]) -> Anime:
    if not data:
        exit(1)

    choice_list = [item.name for item in data]
    anime_answer = questionary.select(
        "Выбрите аниме:",
        choices=choice_list).ask()

    target = next(item for item in data if item.name == anime_answer)
    return jutsu.get_anime(target)

def quest_episode(jutsu, data: Anime):
    if not data:
        exit(1)

    choice_list = defaultdict(list)
    for item in data.episodes:
        choice_list[item.season].append(item.id)

    season_answer = questionary.select(
        "Выберите сезон:",
        choices=choice_list).ask()

    episode_answer = questionary.select(
        "Выберите эпизод:",
        choices=choice_list[season_answer]).ask()

    return next((
        item for item in data.episodes 
        if item.id == episode_answer and
            item.season == season_answer), None)

def quest_video(jutsu: JutSu, data: Episode) -> Video:
    if not data:
        exit(1)

    r_video = jutsu.get_episode_video(data)
    if not r_video:
        logger.error("Не удалось получить видео")
        exit(1)

    choice_list = [item.quality for item in r_video]
    quality_answer = questionary.select(
        "Выберите качество видео:",
        choices=choice_list).ask()

    return next((
        item for item in r_video 
        if item.quality == quality_answer), None)

def main() -> None:
    jutsu = JutSu()
    try:
        r_search = quest_search(jutsu)
        r_anime = quest_anime(jutsu, r_search)
        r_episode = quest_episode(jutsu, r_anime)
        r_video = quest_video(jutsu, r_episode)

        dir_path = create_anime_dir(r_anime.name, r_episode.season)
        filename = f"{r_episode.id}.{r_video.ext}"
        filepath = os.path.join(dir_path, filename)

        if not jutsu.session.download_video(r_video.url, filepath):
            logger.error("Не удалось скачать видео")
        else:
            logger.info(
                "%s. Сезон %s. Эпизод %s успешно скачалось",
                r_anime.name, r_episode.season, r_episode.id)
    finally:
        jutsu.close()

if __name__ == "__main__":
    main()
