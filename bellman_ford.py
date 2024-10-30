import networkx as nx
import matplotlib.pyplot as plt
from graph import Graph, TEST_GRAPH
from scraper import *
from graph import Graph
from collections import defaultdict


class BellmanFord(Graph):
    def __init__(self, graph_dict: dict) -> None:
        super().__init__(graph_dict)
        self.path = None

    def find_shortest_path(self, start: str, goal: str) -> list:
        """
        Compute the shortest path from the start node to the goal node using the Bellman-Ford algorithm.

        Args:
            start: The starting vertex (source)
            goal: The target vertex (goal)

        Returns:
            path: List of vertices that make up the shortest path, or an empty list if no path is found.
        """
        # Initialize distances to infinity and set the distance of the start node to 0
        distances = defaultdict(lambda: float("inf"))
        distances[start] = 0
        came_from = {start: None}  # Track the path

        # Relax edges up to (number of vertices - 1) times
        for _ in range(len(self.graph) - 1):
            for vertex in self.graph:
                for neighbor, weight in self.graph[vertex].items():
                    if distances[vertex] + weight < distances[neighbor]:
                        distances[neighbor] = distances[vertex] + weight
                        came_from[neighbor] = vertex

        # Check for negative weight cycles
        for vertex in self.graph:
            for neighbor, weight in self.graph[vertex].items():
                if distances[vertex] + weight < distances[neighbor]:
                    raise ValueError("Graph contains a negative weight cycle")

        # Generate and return the path if the goal is reachable
        if distances[goal] == float("inf"):
            return []  # No path found
        return self.generate_path(came_from, goal)

    def generate_path(self, came_from: dict, curr_node: str):
        """
        Generate the path from start to goal after running Bellman-Ford algorithm.

        Args:
            came_from: A dictionary mapping each node to the node it was reached from.
            curr_node: The current node (goal) to backtrack from.

        Returns:
            A list of nodes representing the shortest path from start to goal.
        """
        path = [curr_node]
        while came_from[curr_node]:
            curr_node = came_from[curr_node]
            path.append(curr_node)

        path.reverse()  # Reverse the path to get it from start to goal
        self.path = path
        return path

    def visualize(self, start, end):
        """
        Visualize the graph and the shortest path using NetworkX and Matplotlib.

        Args:
            start: The start node to highlight.
            end: The goal node to highlight.
        """
        if self.path:
            G = nx.Graph()
            for vertex, neighbors in self.graph.items():
                for neighbor, weight in neighbors.items():
                    G.add_edge(vertex, neighbor, weight=weight)

            plt.figure(figsize=(12, 8))  # Adjust the size as needed
            pos = nx.spring_layout(G, k=1)  # Increase k for more space between nodes

            node_colors = [
                "pink" if node == start else
                "orange" if node == end else
                ("lightgreen" if node in self.path else "lightblue")
                for node in G.nodes()
            ]
            nx.draw(
                G,
                pos,
                with_labels=True,
                node_color=node_colors,
                node_size=300,  # Smaller node size
                font_size=10,
                font_weight="bold",
                width=0.5  # Thinner edges
            )
            plt.show()
        else:
            raise TypeError("No path has been calculated")


if __name__ == "__main__":
    bellman_ford = BellmanFord(TEST_GRAPH)
    result = bellman_ford.find_shortest_path(start="Node2", goal="Node34")
    print(result)
    bellman_ford.visualize(start="Node2", end="Node34")
