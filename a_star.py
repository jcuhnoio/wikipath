from graph import Graph
from scraper import *

import time
import click
import fasttext
import fasttext.util

from collections import defaultdict
from scipy.spatial.distance import cosine
from heapq import heapify, heappop, heappush


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
            came_from (dict): Contains all articles traversed
                in the least cost path.
            curr_node (string): A string containing the current node
                being traversed.

        Returns:
            path (list of strings): The path from the current node
                to the start node.
        """

        path = [curr_node]

        while came_from[curr_node]:
            curr_node = came_from[curr_node]
            path.append(curr_node)

        path.reverse()

        return path
        
    def find_heuristic(self, start, end):
        """
        Given two articles, finds the cosine similarity between them
        and uses that as a heuristic to measure distance between topics.

        Args:
            start (string): The starting article for the heuristic.
            end (string): The ending article for the heuristic.
        
        Returns:
            heuristic (float32): A value from 1 to 0 which measures how similar
                the two topics are. A lower value is better.
        """
        if (start, end) not in self.heuristic_cache:
            start_vec = self.model.get_word_vector(start)
            end_vec = self.model.get_word_vector(end)
            similarity = 1 - cosine(start_vec, end_vec)
            heuristic = (1 - similarity) + 1e-5
            self.heuristic_cache[(start, end)] = heuristic
        return self.heuristic_cache[(start, end)]
    
@click.command()
@click.option('--start', type=str, help='Title of start article')
@click.option('--end', type=str, help='Title of end article')
def main(start, end):
    a_star = AStar({})
    path = a_star.find_path(start, end)
    print(f"Discovered Path: {path}")

if __name__ == "__main__":
   main()