from douban import DoubanBookUtil
from spinner import Spinner
from zhipu import ZhipuaiUtil
import configparser
import os


def read_config(config_path="config.ini"):
    """Read and return the API keys from the configuration file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            "The configuration file 'config.ini' was not found. Ensure it's in the correct path."
        )

    config = configparser.ConfigParser()
    config.read(config_path)

    if "API" not in config:
        raise KeyError("The 'API' section is missing in the configuration file.")

    if "DOUBAN_API_KEY" not in config["API"] or "ZHIPU_API_KEY" not in config["API"]:
        raise KeyError("Essential API keys are missing in the configuration file.")

    return config["API"]["DOUBAN_API_KEY"], config["API"]["ZHIPU_API_KEY"]


def main():
    book_title = input("Please enter the book title:")
    # Read API key from configuration file or environment variable
    config = configparser.ConfigParser()
    config.read("config.ini")

    douban_book_util = DoubanBookUtil(config["API"]["DOUBAN_API_KEY"])
    zhipuai_util = ZhipuaiUtil(config["API"]["ZHIPU_API_KEY"])

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
    except Exception as e:
        spinner.stop()
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
