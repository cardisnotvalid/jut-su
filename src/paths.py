from pathlib import Path


URL_BASE = "https://jut.su"
URL_ANIME = f"{URL_BASE}/anime"

DIR_BASE = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_BASE / "output"

DIR_OUTPUT.mkdir(exist_ok=True)
