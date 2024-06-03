from src import JutSu
from src.cli import start_questions


if __name__ == "__main__":
    jutsu = JutSu()
    try:
        video_url = start_questions(jutsu)
        jutsu.download_video(video_url)
    finally:
        jutsu.close()
