import requests


class DoubanBookUtil:
    """Utility class for interacting with Douban Book Search API."""

    def __init__(self, api_key: str) -> None:
        """Initialize the util with the necessary API key."""
        self.api_url = "https://api.douban.com/v2/book/search"
        self.api_key = api_key

    def get_book_intro(self, book_title):
        """Retrieve the introduction of a book from Douban API based on the book's title.

        Args:
            book_title (str): The title of the book to search for.

        Returns:
            str: The book's introduction if found; otherwise, an error message.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
        }

        data = {"q": book_title, "apikey": self.api_key}

        response = requests.post(url=self.api_url, headers=headers, json=data)

        if response.status_code == 200:
            data = response.json()
            book_info = data["books"][0]
            return book_info["summary"]
        else:
            raise f"API request failed with status code {response.status_code}"
