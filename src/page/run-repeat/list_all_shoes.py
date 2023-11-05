import requests
from bs4 import BeautifulSoup

from src.config.log_config import get_logger
from src.util.file_io import write_list_to_file

all_shoe_set = set()
already_requested_map = dict()


def get_links_from_html(html_content):
    try:
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find and extract URLs from the HTML elements
        links = [link.get('href') for link in soup.find_all('a')]

        filtered_urls = [url for url in links if url.startswith("https://runrepeat.com/sitemap/")]

        actual_urls = [url for url in links if url.startswith("https://runrepeat.com/")
                       and not url.startswith("https://runrepeat.com/sitemap/")
                       and not url.startswith("https://runrepeat.com/catalog/")
                       ]

        for actual_url in actual_urls:
            all_shoe_set.add(actual_url)

        for filtered_url in filtered_urls:
            make_request(filtered_url)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def make_request(url):
    if already_requested_map.get(url, -1) != -1:
        return

    logger.info(f'[list_all_shoes - make_request] - {url}')
    already_requested_map[url] = 1

    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        get_links_from_html(html_content)
    else:
        print(f"Failed to fetch sitemap URL. Status code: {response.status_code}")


if __name__ == "__main__":
    logger = get_logger()

    logger.info("[list_all_shoes] - Started execution")

    sitemap_url = "https://runrepeat.com/sitemap/"

    make_request(sitemap_url)

    logger.info("[list_all_shoes] - Completed making request")
    logger.info("[list_all_shoes] - Started writing files")

    write_list_to_file(all_shoe_set, '../run-repeat/resources/crawled_url.txt')

    logger.info("[list_all_shoes] - Completed writing files")
    logger.info("[list_all_shoes] - Completed execution")
