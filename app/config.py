import os


class Config:
    def __init__(self):
        # chrome driver
        self.chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
        self.downloaded_media_path = os.getenv("DOWNLOADED_MEDIA_PATH")
        self.max_page_scroll_times = int(os.getenv("MAX_PAGE_SCROLL_TIMES", 5))


def load_config():
    return Config()
