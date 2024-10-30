from bs4 import BeautifulSoup
import fasttext.util
import requests
from graph import Graph
import fasttext
import numpy as np
from scipy.spatial.distance import cosine

fasttext.util.download_model('en', if_exists='ignore')
print("Loading word embeddings")
model = fasttext.load_model('cc.en.300.bin')
print("Done loading word embeddings")

def get_html(URL):
    """
    Gets html from a URL.
    """
    response = requests.get(URL)

    return response.text


def get_links_weight_1(graph: Graph, article):
    """
    Gets all the links in the body content of the wiki page.

    Args:
        URL (string): A string that represents the URL of the current page.
        graph (Class graph): A graph class to add to.

    Returns:
        A Graph() object.
    """
    wiki_url = "https://en.wikipedia.org"
    html = get_html(wiki_url + "/wiki/" + article)
    soup = BeautifulSoup(html, "html.parser")
    container_div = soup.find("div", class_="mw-body-content")
    anchors = container_div.find_all("a")

    # Apply filters so that it only returns wikipedia links.
    anchors = [a for a in anchors if not a.get("class")]
    anchors = [a for a in anchors if a.get("href").startswith("/wiki")]
    anchors = [a for a in anchors if 'title' in a.attrs]
    anchors = [a for a in anchors if 'Wikipedia:' not in a.attrs['title']]
    anchors = [a for a in anchors if 'Template:' not in a.attrs['title']]
    anchors = [a for a in anchors if 'Special:' not in a.attrs['title']]
    anchors = [a for a in anchors if 'Talk:' not in a.attrs['title']]


    for a in anchors:
        anchor_title = a.attrs['title']
        graph.add_edge(article, anchor_title, 1)
    return graph


def get_links_and_weights(graph: Graph, article, end_vector):
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

    wiki_url = "https://en.wikipedia.org"
    html = get_html(wiki_url + '/wiki/' + article.replace(" ", "_"))
    soup = BeautifulSoup(html, "html.parser")

    # Compute title vector once
    title_vector = model.get_word_vector(article)

    # Retrieve links and filter in a single loop
    container_div = soup.find("div", class_="mw-body-content")
    for a in container_div.find_all("a", href=True):
        if (
            not a.get("class")  # Exclude links with a class attribute
            and a['href'].startswith("/wiki")  # Only internal Wikipedia links
            and 'title' in a.attrs  # Ensure a title attribute exists
            and not any(prefix in a['title'] for prefix in ["Wikipedia:", "Template:", "Special:", "Talk:", "Portal:"])
        ):
            anchor_title = a['title']
            link_vector = model.get_word_vector(anchor_title)

            # Directly calculate and add the heuristic distance
            similarity = 1 - cosine(end_vector, link_vector)
            weight = (1 - similarity) + 1e-5
            graph.add_edge(article, anchor_title, weight)

    return graph

def find_heuristic(start, end):
        similarity = 1 - cosine(start, end)
        heuristic = (1 - similarity) + 1e-5
        return heuristic

if __name__ == "__main__":
    test_graph = Graph({})
    get_links_weight_1(test_graph, "Dubazana")
    print(test_graph)
