from bs4 import BeautifulSoup
import requests
from graph import Graph
import fasttext
import numpy as np

model = fasttext.load_model('cc.en.300.bin')

def get_html(URL):
    """
    Gets html from a URL.
    """
    response = requests.get(URL)

    return response.text


def get_links_weight_1(graph: Graph, URL):
    """
    Gets all the links in the body content of the wiki page.

    Args:
        URL (string): A string that represents the URL of the current page.
        graph (Class graph): A graph class to add to.

    Returns:
        A Graph() object.
    """
    html = get_html(URL)
    soup = BeautifulSoup(html, "html.parser")
    container_div = soup.find("div", class_="mw-body-content")
    anchors = container_div.find_all("a")

    # Apply filters so that it only returns wikipedia links.
    anchors = [a for a in anchors if not a.get("class")]
    anchors = [a for a in anchors if a.get("href").startswith("/wiki")]

    wiki_url = "https://en.wikipedia.org"

    result_url = [f"{wiki_url}{a.get('href')}" for a in anchors]

    for link in result_url:
        graph.add_edge(URL, link, 1)
    return graph


def get_links_and_weights(graph: Graph, URL):
    """
    Gets all the links and adds a weight to each link. A weight is equal to the
    Euclidean distance between the text embedding vector value of the title of
    the current page and the link. For creating the embedding, the OpenAI API is
    used.

    Args:
        URL (string): A string that represents the URL of the current page.
        graph (Class graph): A graph class to add to.

    Returns:
        A Graph() object.
    """
    html = get_html(URL)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("span", class_="mw-page-title-main").contents[0]
    title_vector = model.get_word_vector(title)
    container_div = soup.find("div", class_="mw-body-content")
    anchors = container_div.find_all("a")

    # Apply filters so that it only returns wikipedia links.
    anchors = [a for a in anchors if not a.get("class")]
    anchors = [a for a in anchors if a.get("href").startswith("/wiki")]

    wiki_url = "https://en.wikipedia.org"

    for a in anchors:
        link_vector = model.get_word_vector(a.attrs['title'])
        vector_dist = np.linalg.norm(title_vector - link_vector)
        graph.add_edge(URL, f"{wiki_url}{a.get('href')}", vector_dist)
    return graph

