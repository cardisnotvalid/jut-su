import os
from typing import Union

from .paths import DIR_OUTPUT

def create_anime_dir(name: str, season: Union[str, int]) -> str:
    name_dir = os.path.join(DIR_OUTPUT, name)
    season_dir = os.path.join(name_dir, f"Сезон {season}")
    os.makedirs(season_dir, exist_ok=True)
    return season_dir

def reset_file(filepath: str) -> None:
    if os.path.isfile(filepath):
        with open(filepath, "wb") as file:
            file.truncate(0)
