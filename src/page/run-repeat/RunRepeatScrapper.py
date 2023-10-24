import json
import logging

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from src.config.log_config import configure_logger
from src.configs import APPLICATION_NAME
from src.util.common_extractor import extract_from_list, extract_from_table
from src.util.text_normalizer import tokenize_text


def get_page_content(page_url: str):
    logger.info('[get_page_content] -> Started loading content')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(page_url)
        page.wait_for_selector('#content')

        page.click('a[href="#review"]')
        page.wait_for_selector('#review')
        review_content = page.locator('#review').inner_html()

        # Navigate to the specs section
        page.click('a[href="#specs"]')
        page.wait_for_selector('.facts-table-container')
        specs_content = page.locator('div#specs').inner_html()

        logger.info('[get_page_content] -> Completed loading content')
        return review_content, specs_content


def scrape_review_pros_cons(page_content):
    logger.info('[scrape_review_pros_cons] -> Started scraping review')

    review_score = ''
    text_review = ''
    pros_list = []
    cons_list = []

    soup = BeautifulSoup(page_content, 'html.parser')

    reviews_section = soup.find(id='product-intro')
    if reviews_section:
        review_score = reviews_section.find(id='').get_text()
        text_review = reviews_section.find("div", {"class": ""}).get_text()

    pros_and_cons_section = soup.find("section", {"class": "pros-cons-section"})

    if pros_and_cons_section:
        pros_list = extract_from_list(pros_and_cons_section.find(id="the_good"))
        cons_list = extract_from_list(pros_and_cons_section.find(id="the_bad"))

    logger.info('[scrape_review_pros_cons] -> Completed scraping review')

    return {
        'score': tokenize_text(review_score),
        'text_review': tokenize_text(text_review),
        'pros': pros_list,
        'cons': cons_list
    }


def scrape_specs(page_content):
    logger.info('[scrape_specs] -> scraping specs')

    soup = BeautifulSoup(page_content, 'html.parser')

    return extract_from_table(
        soup.find('table', {'class': 'table'})
    )


if __name__ == '__main__':
    configure_logger(APPLICATION_NAME, log_level=logging.INFO)
    logger = logging.getLogger(APPLICATION_NAME)

    parsed_data = list()

    with open('../run-repeat/resources/crawled_url.txt', 'r', encoding='utf-8') as f:
        for url in f.readlines():
            logger.info(f'Scraping url: {url[:-1]}')
            review_content, spec_content = get_page_content(url)

            reviews = scrape_review_pros_cons(page_content=review_content)
            specs = scrape_specs(page_content=spec_content)

            parsed_data.append(
                {
                    'score': reviews['score'],
                    'verdict': reviews['text_review'],
                    'pros': reviews['pros'],
                    'cons': reviews['cons'],
                    'specs': specs
                }
            )

            # print(json.dumps({
            #     'score': reviews['score'],
            #     'verdict': reviews['text_review'],
            #     'pros': reviews['pros'],
            #     'cons': reviews['cons'],
            #     'specs': specs
            # }, indent=5))

            logger.info(f'Completed url: {url[:-1]}')

    dumped_json = json.dumps(parsed_data)

    with open('resources/parsed_data_396.json', 'w', encoding='utf-8') as f:
        f.write(dumped_json)
