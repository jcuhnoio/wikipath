from bs4 import BeautifulSoup
import requests


def get_html(URL):
    """
    Gets html from a URL.
    """
    response = requests.get(URL)

    return response.text


def get_links(URL):
    """
    Gets all the links in the body content of the wiki page.

    Args:
        html (string): A string containing html.

    Returns:
        A list of URLs.
    """
    html = get_html(URL)
    soup = BeautifulSoup(html, "html.parser")
    container_div = soup.find("div", class_="mw-body-content")
    anchors = container_div.find_all("a")

    # Apply filters so that it only returns wikipedia links.
    anchors = [a for a in anchors if not a.get('class')]
    anchors = [a for a in anchors if a.get('href').startswith('/wiki')]

    wiki_url = 'https://en.wikipedia.org'

    result_url = [f"{wiki_url}{a.get('href')}" for a in anchors]

    return result_url

