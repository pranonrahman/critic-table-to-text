import json
import time

import requests
from bs4 import BeautifulSoup

from src.config.log_config import get_logger
from src.util.common_extractor import extract_from_list, make_key_value_pair
from src.util.file_io import read_list_from_file, write_json, write_list_to_file
from src.util.text_normalizer import tokenize_text


def scrape_reviews(html_content):
    logger.info(f'Scrapping reviews')

    soup = BeautifulSoup(html_content, 'html.parser')

    try:
        scrapped_verdict = tokenize_text(soup.find('div', {'class': 'verdict-title-section'}).find_next('p').text)
        scrapped_pros = extract_from_list(soup.find('ul', {'class': 'product-pros-list'}))
        scrapped_cons = extract_from_list(soup.find('ul', {'class': 'product-cons-list'}))
    except Exception as e:
        logger.error(f'Couldn\'t verdicts: {e}')
        scrapped_verdict = ""
        scrapped_pros = []
        scrapped_cons = []

    return scrapped_verdict, scrapped_pros, scrapped_cons


def scrape_full_specs(html_content):
    logger.info(f'Scrapping full specs')

    soup = BeautifulSoup(html_content, 'html.parser')

    try:
        full_specs_div = soup.find('div', {'class': 'spec-comparison'})

        key = full_specs_div.find_all('div', {'class': 'table-cell-data-title'})
        value = full_specs_div.find_all('div', {'class': 'table-cell-data-value'})

        specs = make_key_value_pair(key, value[1:])
    except Exception as e:
        logger.error(f'Couldn\'t scrape full specs: {e}')
        specs = None

    return specs


def scrape_lab_specs(html_content):
    logger.info(f'Scrapping lab specs')

    soup = BeautifulSoup(html_content, 'html.parser')

    try:
        lab_test_div = soup.find('div', {'class': 'test-comparison'})

        key = lab_test_div.find_all('div', {'class': 'table-cell-data-title'})
        value = lab_test_div.find_all('div', {'class': 'table-cell-data-value'})

        lab_test_specs = make_key_value_pair(key, value[1:])
    except Exception as e:
        logger.error(f'Couldn\'t scrape lab specs: {e}')
        lab_test_specs = None

    return lab_test_specs


def load_page_content(page_url):
    logger.info("Loading page using requests")

    """
    Using requests library as it is not javascript rendered. 
    But keeping it as commented as finally we might need to scrape it as well
    """
    # with sync_playwright() as p:
    #     browser = p.chromium.launch(headless=False)
    #     page = browser.new_page()
    #
    #     page.goto(page_url)
    #     page.wait_for_selector('div.post-content-with-advert')
    #
    #     logger.info('[load_page_content] -> Completed loading content')
    #
    #     return page.locator('div.post-content-with-advert').inner_html()

    try:
        response = requests.get(page_url, stream=True)
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"Failed to fetch URL. Status code: {response.status_code}")
    except Exception as e:
        logger.error('Couldn\'t load the file')
        return None


if __name__ == '__main__':
    logger = get_logger()

    all_reviews = list()
    skipped_links = list()
    missing_lab_data_links = list()
    missed_download = list()

    logger.info("Started execution")

    for url in read_list_from_file('../trusted-reviews/resources/all_crawled_reviews.txt'):
        logger.info(f'URL -> {url[:-1]}')

        page_content = load_page_content(page_url=url)

        if page_content is None:
            missed_download.append(url)
            time.sleep(60)
            continue

        verdict, pros, cons = scrape_reviews(page_content)
        full_specs = scrape_full_specs(page_content)
        lab_test_data = scrape_lab_specs(page_content)

        if (len(pros) == 0 and len(cons) == 0) or full_specs is None:
            skipped_links.append(url)
            logger.warning(f'Did not save data: URL -> {url[:-1]}')
            continue

        data = {
            'verdict': verdict,
            'pros': pros,
            'cons': cons,
            'specs': full_specs,
        }

        if lab_test_data is not None:
            data['lab_data'] = lab_test_data
        else:
            logger.warning(f'Missing lab data -> {url[:-1]}')
            missing_lab_data_links.append(url)

        all_reviews.append(data)
        logger.info(f'Appended data to all reviews')

        logger.critical(f'Saved {len(all_reviews)} data')

    write_json(all_reviews, './resources/data.json')
    write_list_to_file(skipped_links, './resources/all_skipped.txt')
    write_list_to_file(missing_lab_data_links, './resources/missing_lab_data.txt')
    write_list_to_file(missed_download, './resources/missed_download.txt')

    logger.info("Completed execution")
