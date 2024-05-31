from collections import namedtuple

__all__ = ["Search", "Video", "Anime", "Episode"]

Search = namedtuple("Search", ["name", "url"])
Video = namedtuple("Video", ["quality", "url"])
Anime = namedtuple("Anime", ["name", "episodes", "url"])
Episode = namedtuple("Episode", ["id", "season", "url"])
