"""
Implementation of Dijkstra's Algorithm

1. Initialize the graph with the source node to take the value of 0 and all other nodes infinity. Start with the source as the “current node”.

2. Visit all neighboring nodes of the current node and update their values to the cumulative sum of weights (distances) from the source.
   If a neighbor’s current value is smaller than the cumulative sum, it stays the same. Mark the “current node” as finished.

3. Mark the unfinished minimum-value node as the “current node”.

4. Repeat steps 2 and 3 until all nodes are finished.
"""

import networkx as nx
import matplotlib.pyplot as plt
from graph import Graph
from scraper import *
from heapq import heapify, heappop, heappush
from collections import defaultdict

EPSILON = 10**-8


class Dijkstra(Graph):

    def __init__(self, graph_dict: dict) -> None:
        super().__init__(graph_dict)
        self.path = None

    def find_shortest_path(self, start: str, goal: str) -> dict:
        """
        Given a starting vertex, compute the shortest distance from starting vertex to every other vertex

        Args:
            start: vertex to start from; this is a key for the graph dictionary

        Returns:
            distances: dictionary containing shortest distance form starting vertex for every other vertex
        """

        # Store vertices we already visited
        visited = set()

        # Initialize all distances between `start` to other nodes to infinity, start node will get 0
        distances = defaultdict(
            lambda: float("inf"), {key: float("inf") for key in self.graph}
        )
        distances[start] = 0

        # Priotiry queue of vertices we need to visit, elements are in (distance, vertex) form
        pq = [(0, start)]
        heapify(pq)

        came_from = {start: None}

        # When pq is empty, that means we visited every vertex
        while pq:
            cur_dist, cur_node = heappop(pq)
            get_links_and_weights(self, cur_node)

            if cur_node.lower() == goal.lower():
                return self.generate_path(came_from, cur_node)

            if cur_node in visited:
                continue

            else:
                visited.add(cur_node)

                # Iterate through current vertex neighbots
                for neighbor, weight in self.graph[cur_node].items():
                    if neighbor not in visited:
                        # If current distance value is larger than the cumulative sum, it updates
                        tent_dist = cur_dist + weight
                        if tent_dist < distances[neighbor]:
                            came_from[neighbor] = cur_node
                            distances[neighbor] = tent_dist
                            heappush(pq, (tent_dist, neighbor))

        return distances

    def generate_path(self, came_from: dict, curr_node: str):
        """
        Given a starting vertex and a goal vertex, compute the shortest distance between the two vertices

        Args:
            start: vertex to start from; this is a key for the graph dictionary
            goal: vertex to end at; this is a key for this graph dictionary

        Returns:
            path: list of vertices that make up the shortest path
        """
        path = [curr_node]
        while came_from[curr_node]:
            curr_node = came_from[curr_node]
            path.append(curr_node)

        path.reverse()
        self.path = path
        return path

    def visualize(self):
        if self.path:
            G = nx.Graph()

            for vertex, neighbors in self.graph.items():
                for neighbor, weight in neighbors.items():
                    G.add_edge(vertex, neighbor, weight=weight)

            pos = nx.spring_layout(G)
            node_colors = [
                "lightblue" if node not in self.path else "lightgreen"
                for node in G.nodes()
            ]
            nx.draw(
                G,
                pos,
                with_labels=True,
                node_color=node_colors,
                node_size=500,
                font_size=10,
                font_weight="bold",
            )
            edge_labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            plt.show()
        else:
            raise TypeError("No path has been calculated")


if __name__ == "__main__":
    dijk = Dijkstra({})
    result = dijk.find_shortest_path(start="Alnico", goal="Magnetic field")
    print(result)
    dijk.visualize()
