import requests

from .paths import get_video_filename, get_output_filepath


DEFAULT_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"


class BaseSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers["User-Agent"] = DEFAULT_USER_AGENT


class VideoDownloader(BaseSession):
    def __init__(self, video_url):
        super().__init__()
        self.video_url = video_url
        self.file_name = get_video_filename(self.video_url)
        self.file_path = get_output_filepath(self.file_name)

    def download(self):
        response = self.get(self.video_url, stream=True)
        try:
            with open(self.file_path, "ab") as f:
                for chunk in response.iter_content(65535):
                    if chunk:
                        print(len(chunk))
                        f.write(chunk)
            print("File saved")
        finally:
            response.close()
