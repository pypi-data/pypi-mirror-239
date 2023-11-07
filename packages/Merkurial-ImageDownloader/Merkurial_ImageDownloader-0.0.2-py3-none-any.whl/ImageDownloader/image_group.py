from bs4 import BeautifulSoup
from image import Image
import requests as rs
from FileUtils.paths import Dir


class ImageGroup:
    """
        The ImageGroup Class Takes A bs4 Search Schema Then Finds All Images That Matches It At Which Point It Collects
        That List Of Matches And Sends It Off To THe ImageGroup Class For Further Processing. The ImageGroup Class Also
        Creates A meta.json File For The Group Of Images Being Created Which Will Contain Basic Information About The
        Group.
        :param bs4_schema : {"name": ["ul", "li", "a"], "attrs": {"class": "rel-link"}} - Default
    """
    def __init__(self, page_url: str, group_title: str, category_path: str | Dir = None,
                 bs4_schema=None, debug=False):
        if bs4_schema is None:
            bs4_schema = {"name": ["ul", "li", "a"], "attrs": {"class": "rel-link"}}
        self.bs4_schema = bs4_schema
        self.page_url = page_url
        self.GROUP_TITLE = group_title
        self.POINTER = Dir(category_path) if isinstance(category_path, str) else category_path
        self.urls = []
        self.successes = 0
        self.fails = 0
        self.attempts = 0
        self.group_path = ""
        self.total_group_time = 0
        self.repeats = 0
        self.DEBUG = debug


    def get_second_level_images(self):
        if self.page_url:
            res = rs.get(self.page_url)
            if res.ok:
                second_level_images = BeautifulSoup(res.text, "html.parser")
                images = second_level_images.findAll(
                    self.bs4_schema["name"], self.bs4_schema["attrs"]
                )
                num_images = len(images)
                if num_images > 0:
                    self.urls = [{"href": img.get("href")} for img in images]
                    return self.urls
        return None


    def write_meta_data(self):
        json_data = {
            "Title": self.GROUP_TITLE,
            "Group Link": self.page_url,
            "Directory": self.POINTER.path,
            "Images": {},
            "Names": {},
        }
        temp_dir = Dir(self.POINTER.path)
        temp_dir.dig(self.GROUP_TITLE)
        temp_dir.write_file("meta", json_data, "json", "w+")
        pass



    def download_images(self):
        second_level_images = self.get_second_level_images()
        if second_level_images:
            self.write_meta_data()
            for image_number, image_data in enumerate(second_level_images):
                image_pointer = Dir(self.POINTER.path)
                image_pointer.add(self.GROUP_TITLE)
                if image_pointer.check_is_dir():
                    image = Image(
                        image_data["href"],
                        (image_number + 1),
                        image_pointer,
                        self.GROUP_TITLE,
                        self.page_url,
                    )
                    (
                        image_path,
                        success,
                        fail,
                        attempt,
                        repeat,
                        download_time,
                    ) = image.download_image()
                    self.successes += success
                    self.fails += fail
                    self.attempts += attempt
                    self.repeats += repeat
                    self.total_group_time += download_time

        return (
            self.successes,
            self.fails,
            self.attempts,
            self.repeats,
            self.group_path,
            self.total_group_time,
        )
