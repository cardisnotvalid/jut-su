from .paths import DIR_OUTPUT

def create_anime_dir(name: str, season: str | int) -> str:
    name_dir = DIR_OUTPUT / name
    season_dir = name_dir / f"Сезон {season}"
    season_dir.mkdir(parents=True, exist_ok=True)
    return season_dir

