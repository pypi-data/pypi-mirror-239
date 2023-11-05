# Book Post Generator

This is a command-line application that generates promotional content for books using data from Douban and custom promotional strategies.

## Installation

To install `book_post_generator`, run this command in your terminal:

```bash
pip install book_post_generator
```

This is the preferred method to install book_post_generator, as it will always install the most recent stable release.

If you have Poetry installed and prefer to use it for installation, run:

```bash
poetry add book_post_generator
```

## Usage
Once installed, you can run the application with the following command:

```bash
book-post-generator
```

The program will prompt you to enter the book title and then retrieve the book information to generate promotional content.

## Configuration
Before the first run, make sure to create a config.ini file in your working directory with the following structure:

```ini
[API]
DOUBAN_API_KEY = your_douban_api_key_here
ZHIPU_API_KEY = your_zhipu_api_key_here
```

Replace your_douban_api_key_here and your_zhipu_api_key_here with your actual API keys.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
