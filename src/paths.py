import os
from urllib.parse import urlparse


URL_BASE = "https://jut.su"
URL_ANIME = f"{URL_BASE}/anime"

DIR_BASE = os.getcwd()
DIR_OUTPUT = os.path.join(DIR_BASE, "output")

os.makedirs(DIR_OUTPUT, exist_ok=True)


def get_video_filename(url):
    parsed_url = urlparse(url)
    (video_id, *_, video_ext) = parsed_url.path.rsplit("/", 1)[-1].split(".")
    return f"{video_id}.{video_ext}"


def get_output_filepath(filename):
    return os.path.join(DIR_OUTPUT, filename)
