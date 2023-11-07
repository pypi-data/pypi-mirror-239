import json
import os
import urllib.request
from time import time, sleep
import imghdr
from urllib.error import URLError
from http.client import RemoteDisconnected
from FileUtils.paths import Dir
from datetime import datetime


class Image:
    """
        The Image Class Takes An Image Link And Downloads It Returning The Results Of What It Did. It Also Writes
        Into The meta.json The Image Name And Number. Image Name Is The Title Name + The Number Provided + 1. So If
        Using This Class As A Standalone, You Should Put The Number 0 As The Image Number Argument, Unless You Want To
        Give It The Number 2 As The First Image.
    """
    def __init__(
            self, url: str, image_number: int, group_path: str | Dir, group_title_and_filename: str, page_url: str
    ):
        self.url = url
        self.group_path = group_path
        self.POINTER = Dir(group_path) if isinstance(group_path, str) else group_path
        self.GROUP_TITLE_AND_FILENAME = group_title_and_filename
        self.page_url = page_url
        self.image_number = image_number
        self.success = 0
        self.fail = 0
        self.attempt = 0
        self.image_time = 0
        self.start_time = 0
        self.http_message = ""
        self.image_path = ""

    def handle_not_save_error(self, image_path: str, error: str):
        date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log = f"""Image: {image_path}\nError: {error}\nPage Url: 
{self.page_url}\nImage Url:{self.url}\nTime: {date_and_time}\n\n"""

        with open(os.path.join(os.getcwd(), "logs/error_log"), "a+") as err_log:
            err_log.write(str(log))
        print(f"Connection Error: {image_path} Continues To Fail Moving On")

    def handle_save_success(self, group_json_file_path: str, filename: str):
        image_num = str(self.image_number)
        try:
            with open(group_json_file_path, "r+", newline="\n") as group_file:
                json_data = json.load(group_file)

            json_data["Images"][image_num] = self.url
            json_data["Names"][image_num] = filename
        except FileNotFoundError:
            json_data = {"Title": self.GROUP_TITLE_AND_FILENAME,
                         "Group Link": self.page_url,
                         "Directory": self.group_path,
                         "Images": {image_num: self.url},
                         "Names": {image_num: filename}
                         }

        with open(group_json_file_path, "w+", encoding="utf-8") as group_file:
            json.dump(json_data, group_file, indent=4)

    def download_single_image(self, write_to_files=True):
        # print("Downloading Single Image")
        # success, fail, attempt
        #    0       0       0

        if self.POINTER.check_is_dir():
            self.group_path = self.POINTER.path
            num_files = len(os.listdir(self.group_path))
            if num_files <= self.image_number+1:
                this_filename = f"{self.GROUP_TITLE_AND_FILENAME}_{self.image_number}"
                self.image_path = os.path.join(self.group_path, this_filename)
                group_json_file = os.path.join(self.group_path, "meta.json")
                if not os.path.isfile(self.image_path):
                    if self.url:
                        count = 0
                        going = True
                        while going:
                            try:
                                (
                                    save_path,
                                    self.http_message,
                                ) = urllib.request.urlretrieve(self.url, self.image_path)
                                self.rename_image(self.image_path)
                                if write_to_files:
                                    self.handle_save_success(group_json_file, this_filename)
                                return 1, 0, 1, self.image_path
                            except URLError as error:
                                count += 1
                                if count == 10:
                                    self.handle_not_save_error(self.image_path, str(error))
                                    return 0, 1, 1, self.image_path
                                else:
                                    sleep(0.2)
                                    continue
                            except RemoteDisconnected as error:
                                count += 1
                                if count == 10:
                                    self.handle_not_save_error(self.image_path, str(error))
                                    return 0, 1, 1, self.image_path
                                else:
                                    sleep(0.2)
                                    continue

                            except FileNotFoundError as error:
                                count += 1
                                if count == 10:
                                    self.handle_not_save_error(self.image_path, str(error))
                                    return 0, 1, 1, self.image_path
                                else:
                                    sleep(0.2)
                                    continue

                            except ValueError as error:
                                count += 1
                                if count == 10:
                                    self.handle_not_save_error(self.image_path, str(error))
                                    return 0, 1, 1, self.image_path
                                else:
                                    sleep(0.2)
                                    continue

                            except BaseException as error:
                                count += 1
                                if count == 10:
                                    self.handle_not_save_error(self.image_path, str(error))
                                    return 0, 1, 1, self.image_path
                                else:
                                    sleep(0.2)
                                    continue

                    else:
                        print("No URL Available In download_single_image")
                        return 0, 0, 1, self.image_path
                else:
                    self.handle_not_save_error(self.image_path, "Image At Image Path Was Broken")
                    return 0, 0, 1, self.image_path
            else:
                return 0, 0, 1, self.image_path
        else:
            return 0, 0, 0, self.image_path

    @staticmethod
    def rename_image(old_file_path):
        type_of_image = imghdr.what(old_file_path)
        if type_of_image:
            if type_of_image not in old_file_path:
                new_image_name = f"{old_file_path}.{type_of_image}"
                os.rename(old_file_path, new_image_name)

    def download_image(self):
        self.start_time = time()

        if self.url:

            (
                self.success,
                self.fail,
                self.attempt,
                self.image_path
            ) = self.download_single_image()

        repeat = self.attempt - self.success

        image_time = time() - self.start_time
        # print("Returning")
        return self.image_path, self.success, self.fail, self.attempt, repeat, image_time
