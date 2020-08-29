import shutil
import time
import uuid
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from app.config import load_config

config = load_config()


class Scraper():
    def __init__(self, url: str, media_counts: str):
        self.url = url
        self.profile_name = self.get_profile_name(self.url)
        self.media_counts = media_counts
        self.downloaded_media_path = config.downloaded_media_path

        self.max_scroll_times = config.max_page_scroll_times

        self.web_driver = webdriver.Chrome(
            config.chrome_driver_path, keep_alive=True)
        self.web_driver.get(url=self.url)

    def scroll_page(self):
        self.web_driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # TODO: Make this sleep configurable.
        time.sleep(0.750)

    @staticmethod
    def generate_media_id():
        return str(uuid.uuid1())

    @staticmethod
    def is_media_url(url: str):
        return url.find("media") != -1

    @staticmethod
    def get_media_format(media_url: str):
        query = urlparse(media_url).query
        fmt = parse_qs(query)["format"]
        return fmt[0]

    # TODO: Implement threading.
    def download_all_media(self, media_urls: list):
        print("About to download {} media".format(
            len(media_urls)))
        for url in media_urls:
            id = self.generate_media_id()
            self.download_media(id, url)

    def download_media(self, media_id: str, media_url: str):
        file_name = "{}-{}.{}".format(self.profile_name,
                                      media_id,
                                      self.get_media_format(media_url))
        res = requests.get(media_url, stream=True)

        # TODO: Learn wb and shutil behavior.
        with open("{}/{}".format(self.downloaded_media_path,
                                 file_name), "wb") as o:
            shutil.copyfileobj(res.raw, o)

        print("[OK] {}".format(file_name))

        # TODO: Learn del behavior.
        del res

    @ staticmethod
    def get_profile_name(profile_url: str):
        return profile_url.split("twitter.com/")[-1]

    def start(self):
        print("Starting scraper "
              + "{ "
              + "url: {}, ".format(self.url)
              + "media_counts: {} ".format(self.media_counts)
              + "}")

        cur_scroll_times = 0
        media_src_urls = set([])

        while True:
            is_finished = False

            # scroll page to get more media
            self.scroll_page()
            cur_scroll_times += 1
            print(
                "Scrolling pages [{}/{}]".format(cur_scroll_times,
                                                 self.max_scroll_times))

            page_source = self.web_driver.page_source

            soup = BeautifulSoup(page_source, "html.parser")
            # NOTE: We define media as both image and video, but only image
            # that is currently supported.
            # TODO: Add support to scrape videos.
            raw_images = soup.find_all(name="img")

            for raw_image in raw_images:
                src_url = raw_image["src"]

                if self.is_media_url(src_url):
                    media_src_urls.add(src_url)

                if len(media_src_urls) >= self.media_counts:
                    print("Desired number of media ({}) are found".format(
                        len(media_src_urls)))
                    is_finished = True
                    break

            print("Received {} media images".format(
                len(media_src_urls)))

            if (cur_scroll_times == self.max_scroll_times) and not is_finished:
                print("Maximum page scrolling ({}) is reached".format(
                    self.max_scroll_times))
                is_finished = True

            if is_finished:
                print("Scraping is finished")
                break

        print("Quitting web driver")
        self.web_driver.quit()

        print("Downloading media")
        self.download_all_media(media_src_urls)
