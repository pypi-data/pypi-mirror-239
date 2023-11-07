from bs4 import BeautifulSoup
from time import time
from inputs import TakeInput
from FileUtils.paths import Dir
from images_page import ImagesPage


class ImagePuller:
    """
    ImagePuller Grabs A List Of Links From An HTML Document, Removes Any Possible Duplicates And Hands The Links In
    Proper Format To The Images Page Class For Further Processing.
    """
    def __init__(
        self,
        file_loc,
        root_dir_path=None,
        unknown_category="Unknown",
        remove_duplicates=True,
        display_final_stats=True,
        per_page_stats=False,
        start_num=None,
        stop_num=None,
        debug=False,
    ):
        # GLOBALS
        self.ROOT_DIR = root_dir_path
        self.TOTAL_NUM_PAGES = 0
        self.NUM_PAGES_TO_DOWNLOAD = 0
        self.TOTAL_TIME_TO_COMPLETE = 0
        self.TOTAL_PAGE_SUCCESSES = 0
        self.TOTAL_PAGES_FAILED = 0
        self.TOTAL_PAGE_ATTEMPTS = 0
        self.TOTAL_PAGE_REPEATS = 0
        self.TOTAL_IMAGE_SUCCESSES = 0
        self.TOTAL_IMAGES_FAILED = 0
        self.TOTAL_IMAGE_ATTEMPTS = 0
        self.TOTAL_IMAGE_REPEATS = 0
        self.EQ_NUM = 80
        self.START_NUM = start_num
        self.STOP_NUM = stop_num
        self.START_TIME = 0
        self.DEBUG = debug

        # PARAMETERS
        self.file_loc = file_loc
        self.POINTER = Dir(root_dir_path) if isinstance(root_dir_path, str) else root_dir_path
        self.UNKNOWN_CATEGORY = unknown_category
        self.per_page_stats = per_page_stats
        self.display_final_stats = display_final_stats
        self.remove_duplicates = remove_duplicates
        self.HREFS = []


    def remove_duplicate_links(self, links=True):
        with open(self.file_loc, "r") as file:
            bs = BeautifulSoup(file, features="html.parser")
            if links:
                hrefs = bs.find_all("a", href=True)
                hrefs = [
                    {"title": a.contents[0], "href": a["href"], "src": a.get("src")}
                    for a in hrefs
                ]
                hrefs = list(
                    {
                        href["href"]: href for href in hrefs
                    }.values()
                )

                hrefs = sorted(hrefs, key=lambda x: x["title"])
                self.HREFS = hrefs
            else:
                all_as = bs.find_all("a")
                self.HREFS = set(all_as)

        return self.HREFS

    def take_inputs(self):

        inputs = TakeInput(self.TOTAL_NUM_PAGES, self.START_NUM, self.STOP_NUM)
        start, stop = inputs.take_inputs()
        if start is False or stop is False:
            print("Finished For Now, Goodbye!")
            exit(0)
        else:
            self.START_NUM = start
            self.STOP_NUM = stop
            self.NUM_PAGES_TO_DOWNLOAD = self.TOTAL_NUM_PAGES - self.STOP_NUM - self.START_NUM

    def handle_total_stats(self):
        if self.display_final_stats:
            stats = {
                "time": self.TOTAL_TIME_TO_COMPLETE,
                "page_successes": self.TOTAL_PAGE_SUCCESSES,
                "page_failures": self.TOTAL_PAGES_FAILED,
                "page_attempts": self.TOTAL_PAGE_ATTEMPTS,
                "page_repeats": self.TOTAL_PAGE_REPEATS,
                "image_successes": self.TOTAL_IMAGE_SUCCESSES,
                "image_failures": self.TOTAL_IMAGES_FAILED,
                "image_attempts": self.TOTAL_IMAGE_ATTEMPTS,
                "image_repeats": self.TOTAL_IMAGE_REPEATS,
            }

            total_time = stats["time"]
            time_text = "Minutes" if total_time > 60 else "Seconds"
            display_time = total_time / 60 if total_time > 60 else total_time
            time_to_complete = rf"{round(display_time, 2)} {time_text}"

            def title_text(text: str, eq: int):
                print(text.center(eq, "-"))

            def get_left_text(text: str, text2: str, eq: int):
                print(text.ljust(int(eq / 2), " ") + text2)

            print()
            print()
            print()
            print("Final Stats:")

            get_left_text(r"Completed All Downloads In: ", time_to_complete, self.EQ_NUM)
            print("=" * self.EQ_NUM)
            title_text("  Pages ", self.EQ_NUM)
            get_left_text("TOTAL PAGES DOWNLOADED:", rf"{stats['page_successes']}", self.EQ_NUM)
            get_left_text("TOTAL PAGES FAILED:", f"{stats['page_failures']}", self.EQ_NUM)
            get_left_text("TOTAL PAGES ATTEMPTED:", f"{stats['page_repeats']}", self.EQ_NUM)
            get_left_text("TOTAL PAGES RETRIED:", f"{stats['page_attempts']}", self.EQ_NUM)
            title_text(" Images ", self.EQ_NUM)
            get_left_text("TOTAL IMAGES DOWNLOADED:", f"{stats['image_successes']}", self.EQ_NUM)
            get_left_text("TOTAL IMAGES FAILED:", f"{stats['image_failures']}", self.EQ_NUM)
            get_left_text("TOTAL IMAGES ATTEMPTED:", f"{stats['image_attempts']}", self.EQ_NUM)
            get_left_text("TOTAL IMAGES RETRIED:", f"{stats['image_repeats']}", self.EQ_NUM)
            print("=" * self.EQ_NUM)
            print()

    def get_pages(self, root_dir_path=None):
        if root_dir_path is None and self.ROOT_DIR is None:
            raise ValueError("A Root Directory Must Be Provided At Instantiation Or In Get Pages")

        self.remove_duplicate_links()
        self.TOTAL_NUM_PAGES = len(self.HREFS)
        if self.TOTAL_NUM_PAGES > 0:
            self.take_inputs()
            self.START_TIME = time()
            for attempts, page_content in enumerate(
                self.HREFS[self.START_NUM : self.STOP_NUM]
            ):
                self.TOTAL_PAGE_ATTEMPTS = attempts + 1
                image_page = ImagesPage(
                    page_content,
                    self.ROOT_DIR,
                    self.EQ_NUM,
                    self.NUM_PAGES_TO_DOWNLOAD,
                    self.TOTAL_NUM_PAGES,
                    self.TOTAL_IMAGE_SUCCESSES,
                    attempts + 1,
                    self.per_page_stats,
                    self.DEBUG
                )


                current_item_number = self.START_NUM + attempts
                print(
                    f"Trying To Download Page: {current_item_number} Of {self.STOP_NUM} Out Of: "
                    f"{self.TOTAL_NUM_PAGES}"
                )

                (
                    image_successes,
                    image_failures,
                    image_attempts,
                    image_repeats,
                    time_to_complete_page,
                ) = image_page.run_download_page()
                self.TOTAL_TIME_TO_COMPLETE += time_to_complete_page

                self.TOTAL_IMAGE_SUCCESSES += image_successes
                self.TOTAL_IMAGES_FAILED += image_failures
                self.TOTAL_IMAGE_ATTEMPTS += image_attempts
                self.TOTAL_IMAGE_REPEATS += image_repeats

                self.TOTAL_PAGE_SUCCESSES += (
                    1
                    if self.TOTAL_IMAGE_SUCCESSES > 0 and self.TOTAL_IMAGES_FAILED == 0
                    else 0
                )
                self.TOTAL_PAGES_FAILED += 1 if image_failures > 0 else 0
                self.TOTAL_PAGE_ATTEMPTS += 1 if image_attempts > 0 else 0
                self.TOTAL_PAGE_REPEATS += 1 if image_repeats > 0 else 0

        else:
            print("There Was A Problem With The Starting Paths You Entered.")

        self.TOTAL_TIME_TO_COMPLETE = time() - self.START_TIME
        self.handle_total_stats()

        return True


if __name__ == "__main__":
    html_page = "/home/merk/Internals/Internal_SSD/Shared/PycharmProjects/Personal/ALL_IMAGE_DATA/Data/htmls/ML_WOMEN.html"
    download_dir_path = "/home/merk/Internals/Internal_SSD/Shared/PycharmProjects/ImageDownloader/ImageDownloader/Temp_Check"
    imager = ImagePuller(html_page, download_dir_path)
    all_done = imager.get_pages()
    print("All Done: ", all_done)
