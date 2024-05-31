from collections import defaultdict
import questionary
from src.jutsu import JutSu

if __name__ == "__main__":
    jutsu = JutSu()
    try:
        search_query = questionary.text("Поиск:", default="Ванпанчмен").ask()

        search_result = jutsu.search(search_query)
        anime_names = [item.name for item in search_result]

        if not anime_names:
            questionary.print("Ничего не нашлось").ask()
            exit(0)

        selected_anime = questionary.select("Выберите аниме:", choices=anime_names).ask()

        d_anime = None
        for anime in search_result:
            if anime.name == selected_anime:
                d_anime = anime
                break

        anime = jutsu.anime(d_anime)

        episodes = defaultdict(list)
        for item in anime.episodes:
            episodes[str(item.season)].append(item.id)

        selected_season = questionary.select(
            "Выберите сезон:", choices=episodes.keys()).ask()
        selected_episode = questionary.select(
            "Выбрите эпизод:", choices=episodes[selected_season]).ask()

        ani_epi = None
        for item in anime.episodes:
            if item.id == selected_episode and item.season == selected_season:
                ani_epi = item
                break

        epi_video = jutsu.get_episode_videos(ani_epi)
        vi_quality = [item.quality for item in epi_video]

        selected_video = questionary.select(
            "Выбрите качество видео:", choices=vi_quality).ask()

        ani_vi = None
        for item in epi_video:
            if item.quality == selected_video:
                ani_vi = item
                break

        print("Downloading video...")
        with jutsu.session.get(ani_vi.url, stream=True) as r:
            r.raise_for_status()
            with open("video.mp4", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("Done!")
    finally:
        jutsu.close()
