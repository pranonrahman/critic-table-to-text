from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from src.config.log_config import get_logger
from src.util.common_extractor import extract_from_list
from src.util.file_io import read_list_from_file, write_json
from src.util.text_normalizer import tokenize_text, remove_trailing_colon


def get_page_content(page_url: str):
    logger.info('[get_page_content] -> Started loading content')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(page_url)
        page.wait_for_selector('#content')

        page.click('a[href="#review"]')
        page.wait_for_selector('#review')
        review_section_content = page.locator('#review').inner_html()

        # Navigate to the specs section
        page.click('a[href="#specs"]')
        page.wait_for_selector('.facts-table-container')
        specs_content = page.locator('div#specs').inner_html()

        lab_data_content = None

        link_count = page.locator('a[href="#lab-data"]').count()

        if link_count > 0:
            # Navigate to the lab data section
            page.click('a[href="#lab-data"]')
            page.wait_for_selector('#lab-data')
            lab_data_content = page.locator('div#lab-data').inner_html()

        logger.info('[get_page_content] -> Completed loading content')
        return review_section_content, specs_content, lab_data_content


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


def extract_from_table(section):
    """
    :param section: html selection
    :return: json where key is first column and value is second column of each row
    """
    table_data = dict()

    for row in section.find_all('tr'):
        key = remove_trailing_colon(tokenize_text(row.find_all('th')[0].text))
        value = tokenize_text(row.find_all('td')[0].text)

        if key and value:
            table_data[key] = value

    return table_data


def extract_lab_data_table(soup):
    data = {}
    rows = soup.find_all('tr')

    current_category = None
    headers = [th.text.strip() for th in rows[0].find_all('th')]

    for row in rows:
        th = row.find('th')
        td = row.find_all('td')

        if th:
            # Extract the category when a <th> element is found
            current_category = th.text.strip()
            data[current_category] = {}
        elif current_category and len(td) == 3:
            # Extract subcategories and values when <td> elements are found
            subcategory = td[0].text.strip()
            values = {
                headers[1]: td[1].text.strip(),
                headers[2]: td[2].text.strip(),
            }

            data[current_category][subcategory] = values

    return data


def scrape_lab_data(page_content):
    logger.info('[scrape_lab_data] -> scraping lab data')

    soup = BeautifulSoup(page_content, 'html.parser')

    return extract_lab_data_table(
        soup.find('table', {'class': 'table'})
    )


if __name__ == '__main__':
    logger = get_logger()

    parsed_data = list()

    for url in read_list_from_file('../run-repeat/resources/crawled_url.txt'):
        logger.info(f'Scraping url: {url[:-1]}')
        review_content, spec_content, lab_data_content = get_page_content(url)

        reviews = scrape_review_pros_cons(page_content=review_content)
        specs = scrape_specs(page_content=spec_content)

        lab_data = None

        if lab_data_content is not None:
            lab_data = scrape_lab_data(lab_data_content)

        parsed_content = {
            'score': reviews['score'],
            'verdict': reviews['text_review'],
            'pros': reviews['pros'],
            'cons': reviews['cons'],
            'specs': specs
        }

        if lab_data is not None:
            parsed_content['lab_data'] = lab_data

        parsed_data.append(parsed_content)

    write_json(parsed_data, 'resources/data_with_lab_data.json')
