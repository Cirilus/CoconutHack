import requests
from bs4 import BeautifulSoup
from loguru import logger


def fetch_webpage_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.debug(f"Error fetching the webpage: {e}")
        return None


def remove_html_tags(html_content):
    if html_content is None:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()
    return text_content