from src.jutsu import JutSu
from src.logger import logger
from src.session import Session

if __name__ == "__main__":
    jutsu = JutSu()
    try:
        r_search = jutsu.search("дворецкий")
        print(r_search)
        r_anime = jutsu.get_anime(r_search.pop(0))
        print(r_anime)
        r_video = jutsu.get_episode_video(r_anime.episodes.pop(0))
        print(r_video)
    except Exception as err:
        logger.error("Произошла ошибка: %s", err)
    finally:
        jutsu.close()
