import requests

from src.config.log_config import get_logger


def scrape_reviews(html_content):
    return {
        'verdict': '',
        'pros': [],
        'cons': []
    }


def load_page_content(page_url):
    logger.info("[load_page_content] -> Loading page using requests")

    """
    Using requests library as it is not javascript rendered. 
    But keeping it as commented as finally we might need to scrape it as well
    """
    # with sync_playwright() as p:
    #     browser = p.chromium.launch(headless=False)
    #     page = browser.new_page()
    #
    #     page.goto(page_url)
    #     page.wait_for_selector('.post-content-with-advert')
    #
    #     logger.info('[load_page_content] -> Completed loading content')
    #
    #     return page.locator('div.post-content-with-advert').inner_html()

    response = requests.get(page_url)

    if response.status_code == 200:
        return response.text
    else:
        logger.error(f"Failed to fetch URL. Status code: {response.status_code}")


if __name__ == '__main__':
    logger = get_logger()

    logger.info("Started execution")

    page_content = load_page_content(f'https://www.trustedreviews.com/reviews/iphone-12-pro-max')
    reviews = scrape_reviews(page_content)

    logger.info("Completed execution")
