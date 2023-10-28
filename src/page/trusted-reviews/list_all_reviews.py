import logging

import requests
from bs4 import BeautifulSoup

from src.config.log_config import configure_logger
from src.configs import LOG_LEVEL, APPLICATION_NAME

configure_logger(APPLICATION_NAME, log_level=LOG_LEVEL)
logger = logging.getLogger(APPLICATION_NAME)

all_reviews_set = set()
already_requested_links = dict()


def list_all_link_from_page(html_content):
    logger.info(f'[list_all_link_from_page - scraping page]')

    try:
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        all_links_for_month = soup.find("ul", {"class": "archive-list-condensed"})

        # Find and extract URLs from the HTML elements
        links = [link.get('href') for link in all_links_for_month.find_all('a')]
        review_links = [url for url in links if url.startswith("https://www.trustedreviews.com/reviews/")]

        for link in review_links:
            all_reviews_set.add(link)

        logger.info(f'[list_all_link_from_page] completed listing  page: collected {len(review_links)} pages')

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def make_request(url):
    logger.info(f'[list_all_reviews - make_request] - {url}')

    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text

        list_all_link_from_page(html_content)
    else:
        print(f"Failed to fetch sitemap URL. Status code: {response.status_code}")


if __name__ == "__main__":
    logger.info("[list_all_reviews] - Started execution")

    month = 10
    year = 2023

    while year >= 2008:
        while month > 0:
            page_url = f'https://www.trustedreviews.com/archive/{year}/{month}'
            make_request(page_url)

            month -= 1
        year -= 1
        month = 12

    logger.info("[list_all_reviews] - Completed making request")
    logger.info("[list_all_reviews] - Started writing files")

    with open('../trusted-reviews/resources/all_crawled_reviews.txt', 'w', encoding='utf-8') as f:
        for item in all_reviews_set:
            f.write(item + '\n')

    logger.info("[list_all_reviews] - Completed writing files")
    logger.info("[list_all_reviews] - Completed execution")
