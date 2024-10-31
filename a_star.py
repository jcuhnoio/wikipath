from graph import Graph
from heapq import heapify, heappop, heappush
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
from collections import defaultdict
from scraper import *
from scipy.spatial.distance import cosine
import time
import fasttext
import fasttext.util

class AStar(Graph):
    def __init__(self, graph_dict: dict) -> None:
        super().__init__(graph_dict)
        self.graph = graph_dict
        self.heuristic_cache = {}
        self.model = fasttext.load_model('cc.en.300.bin')
      
    
    def find_path(self, start, end):
        """
        From a given start article and end article, computes a path of links
        to traverse across Wikipedia from the start to the end.

        Args:
            start (string): Title of the start article.
            end (string): Title of the end article.
        Returns:
            path (list of strings): A list showing the path from the start article
                to the end article.
        """
        # Initialize sets, scores, and queue as before
        pq = [(0, start)]
        heapify(pq)
        visited = set()
        came_from = {start: None}
        g_score = defaultdict(
            lambda: float("inf"), {key: float("inf") for key in self.graph}
        )
        g_score[start] = 0
        f_score = defaultdict(
            lambda: float("inf"), {key: float("inf") for key in self.graph}
        )
        end_vector = self.model.get_word_vector(end)
        f_score[start] = self.find_heuristic(start, end)

        start_time = time.time()
        while pq:
            _, curr_node = heappop(pq)
            if curr_node in visited:
                continue
            visited.add(curr_node)
            print(curr_node)

            if curr_node.lower() == end.lower():
                print(f"Total time {time.time() - start_time}")
                print(f"Pages visited {len(visited)}")
                return self.generate_path(came_from, curr_node)

            
            get_links_and_weights(self, curr_node, end_vector)



            for neighbor, weight in self.graph[curr_node].items():
                tentative_g_score = g_score[curr_node] + weight
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = curr_node
                    g_score[neighbor] = tentative_g_score
                    h_score = self.find_heuristic(neighbor, end)
                    f_score[neighbor] = tentative_g_score + h_score
                    heappush(pq, (f_score[neighbor], neighbor))

        return None
    
    def generate_path(self, came_from, curr_node):
        """
        Generates a list representing the path to traverse.

        Args:
            came_from (dict): Contains all paths
        """

        path = [curr_node]

        while came_from[curr_node]:
            curr_node = came_from[curr_node]
            path.append(curr_node)

        path.reverse()

        return path
        
    def find_heuristic(self, start, end):
        if (start, end) not in self.heuristic_cache:
            start_vec = self.model.get_word_vector(start)
            end_vec = self.model.get_word_vector(end)
            similarity = 1 - cosine(start_vec, end_vec)
            heuristic = (1 - similarity) + 1e-5
            self.heuristic_cache[(start, end)] = heuristic
        return self.heuristic_cache[(start, end)]
    
    def visualize(self, path=None):
        G = nx.Graph()

        # Add edges to the graph
        for vertex, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(vertex, neighbor, weight=0.1)

        pos = nx.spring_layout(G)

        # Set node colors based on whether they are part of the final path
        node_colors = ['lightblue' if node not in path else 'lightgreen' for node in G.nodes()]

        # Set labels only for nodes in the path
        node_labels = {node: node if node in path else "" for node in G.nodes()}

        # Draw the graph with custom node labels
        nx.draw(G, pos, labels=node_labels, node_color=node_colors, node_size=500, font_size=10, font_weight='bold')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.show()



if __name__ == "__main__":
   
    test = AStar({})
    path = test.find_path("Graph Theory", "K-pop")
    print(path)
    #test.visualize(path)