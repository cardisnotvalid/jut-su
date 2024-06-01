from pathlib import Path


DIR_BASE = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_BASE / "output"

DIR_OUTPUT.mkdir(exist_ok=True)
