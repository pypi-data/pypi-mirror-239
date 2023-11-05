from book_post_generator.douban import DoubanBookUtil
from book_post_generator.spinner import Spinner
from book_post_generator.zhipu import ZhipuaiUtil
import configparser
import fire
import os


class BookPostGenerator:
    def __init__(self):
        self.config_path = os.path.expanduser("~/.book_post_generator/config.ini")

    def init_config(self):
        config = configparser.ConfigParser()
        config["API"] = {
            "DOUBAN_API_KEY": "your-douban-api-key",
            "ZHIPU_API_KEY": "your-zhipu-api-key",
        }

        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        with open(self.config_path, "w") as configfile:
            config.write(configfile)

        print(f"Configuration file created at {self.config_path}")

    def run(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        douban_book_util = DoubanBookUtil(config["API"]["DOUBAN_API_KEY"])
        zhipuai_util = ZhipuaiUtil(config["API"]["ZHIPU_API_KEY"])
        book_title = input("Please enter the book title:")
        spinner = Spinner(message="...")
        spinner.start()
        try:
            book_intro = douban_book_util.get_book_intro(book_title)
            print(
                "Book information successfully retrieved, now generating promotional content..."
            )
            promotion_text = zhipuai_util.generate_promotion(book_intro)
            spinner.stop()
            print("\nGenerated promotional content:\n")
            print(promotion_text)
        except:
            spinner.stop()
            print("An error occurred.")


def main():
    fire.Fire(BookPostGenerator)


if __name__ == "__main__":
    main()
