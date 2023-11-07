import re
from bs4 import BeautifulSoup
import requests as rs
from image_group import ImageGroup
from FileUtils.paths import Dir


class ImagesPage:
    """
        ImagesPage Takes A list Of Links in {href: page_link, title: page_title} Format Cleans The Title
        And Downloads The Page To Hand Off To The ImageGroup Class For Further Processing.
        :param bs4_schema : {"name": ["li", "img", "a"], "attrs": {"class": "alt-lang-item"}} - Default
    """
    def __init__(
        self,
        content,
        root_dir_path: str | Dir,
        bs4_schema: dict | None = None,
        eq_num=80,
        num_pages_to_download=0,
        total_images_saved=0,
        total_page_attempts=0,
        per_page_stats=True,
        debug=False
    ):
        # GLOBALS
        self.TOTAL_IMAGE_SUCCESSES = 0
        self.TOTAL_PAGE_ATTEMPTS = 0
        self.PAGE_FAILURES = 0
        self.PAGE_REPEATS = 0
        self.TIME_TO_COMPLETE_PAGE = 0
        self.FAIL_MESSAGE = "None"
        self.PAGE_PATH = root_dir_path if isinstance(root_dir_path, str) else root_dir_path.path
        if bs4_schema is None:
            bs4_schema = {"name": ["li", "img", "a"], "attrs": {"class": "alt-lang-item"}}
        self.bs4_schema = bs4_schema

        # Page Variables
        self.NUM_PAGES_TO_DOWNLOAD = num_pages_to_download
        self.TITLE = ""
        self.PAGE_URL = ""
        self.GROUP_DIR = ""
        self.TOTAL_PAGES_FAILED = 0

        # Image Variables
        self.TOTAL_IMAGES_SAVED = 0
        self.TOTAL_IMAGE_ATTEMPTS = 0
        self.TOTAL_IMAGE_FAILURES = 0
        self.TOTAL_IMAGE_REPEATS = 0

        # INPUTS
        self.CONTENT = content
        self.CATEGORY = ""
        self.PER_PAGE_STATS = per_page_stats
        self.EQ_NUM = eq_num
        self.TOTAL_PAGE_ATTEMPTS = total_page_attempts
        self.TOTAL_IMAGES_SAVED = total_images_saved
        self.DEBUG = debug

        self.POINTER = Dir(root_dir_path) if isinstance(root_dir_path, str) else root_dir_path

    def get_page_content(self):
        self.TITLE = self.CONTENT["title"]
        href = self.CONTENT.get("href")
        src = self.CONTENT.get("src")
        if not href:
            if not src:
                Warning("One Of The Items Provided Did Not Contain A Link, Skipping.")
                return False, False
            else:
                href = src
        self.PAGE_URL = href
        return self.TITLE, self.PAGE_URL


    def clean_dirname(self, dirname: str = None):
        dirname = dirname if dirname else self.TITLE
        cleaned_title = dirname.replace(",", "")
        cleaned_title = " ".join(cleaned_title.split("-")[0:-1]).strip()
        string = rf"[1-9][1-9]y"
        match = re.match(string, cleaned_title)
        if match:
            match_text = match.group()
            number = match_text.split("y", 1)[0]
            new_title = dirname.replace(match_text, f"{number} years old")
            cleaned_title = new_title
        return cleaned_title

    def get_main_page_image_links(self):
        res = rs.get(self.PAGE_URL)
        if res.ok:
            main_page_images = BeautifulSoup(res.text, "html.parser")
            main_images = main_page_images.findAll(
                self.bs4_schema["name"], self.bs4_schema["attrs"]
            )
            if len(main_images) > 1:
                main_image = main_images[0]
                href = main_image.get("href")
                if href:
                    return href
        return None

    def handle_page_stats(self):
        if self.PER_PAGE_STATS:

            print(f"Group Title:        {self.TITLE}")
            print(f"G")
            print("=" * self.EQ_NUM)
            print(
                f"Page Number:          {self.TOTAL_PAGE_ATTEMPTS} | {self.NUM_PAGES_TO_DOWNLOAD} "
            )
            print(f"Completed In:       {round(self.TIME_TO_COMPLETE_PAGE, 4)} Seconds")
            print("-" * self.EQ_NUM)
            print(f"Total Successful:   {self.TOTAL_IMAGES_SAVED}")
            print(f"Total Failed:       {self.TOTAL_IMAGE_FAILURES}")
            print(f"Total Repeats:      {self.TOTAL_IMAGE_REPEATS}")

            if self.TOTAL_IMAGES_SAVED == 0 and self.TOTAL_IMAGE_FAILURES == 0 and self.TOTAL_IMAGE_REPEATS == 0:
                print("Something Went Wrong Here....")
                print("The Associated Data Is: ", )
                print(f"Group Path:         {self.GROUP_DIR}")
                print(f"Content Was:        {self.CONTENT}")
                print(f"Categorized As:     {self.CATEGORY}")
                print(f"Most Likely Was A Site Not From PornPics.com Or The Problem Was "
                      f"That It Was A Video Site Accidentally Added."
                      )

            print("=" * self.EQ_NUM)
            print()

    def run_download_page(self):
        page_title, page_link = self.get_page_content()
        if page_title and page_link:
            self.TITLE = self.clean_dirname(page_title)
            image_group = ImageGroup(page_link, self.TITLE, self.POINTER, self.DEBUG)
            (
                successes,
                failures,
                attempts,
                repeats,
                self.GROUP_DIR,
                group_download_time,
            ) = image_group.download_images()

            self.TOTAL_IMAGES_SAVED = successes
            self.TOTAL_IMAGE_SUCCESSES += self.TOTAL_IMAGES_SAVED
            self.TOTAL_IMAGE_FAILURES += failures
            self.TOTAL_IMAGE_ATTEMPTS += attempts
            self.TOTAL_IMAGE_REPEATS += repeats
            self.TIME_TO_COMPLETE_PAGE = group_download_time

        self.handle_page_stats()
        return (
            self.TOTAL_IMAGE_SUCCESSES,
            self.TOTAL_IMAGE_FAILURES,
            self.TOTAL_IMAGE_ATTEMPTS,
            self.TOTAL_IMAGE_REPEATS,
            self.TIME_TO_COMPLETE_PAGE,
        )

