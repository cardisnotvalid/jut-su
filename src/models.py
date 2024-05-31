__all__ = ["Search", "Video", "Anime", "Episode"]

from collections import namedtuple

Search = namedtuple("Search", ["name", "url"])
Video = namedtuple("Video", ["quality", "ext", "url"])
Anime = namedtuple("Anime", ["name", "episodes", "url"])
Episode = namedtuple("Episode", ["id", "season", "url"])
