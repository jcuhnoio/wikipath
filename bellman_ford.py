from scraper import *
from graph import Graph

import time
import click
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
        end_vector = model.get_word_vector(goal)

        # Initialize distances to infinity and set the distance of the start node to 0
        distances = defaultdict(
            lambda: float("inf"), {key: float("inf") for key in self.graph}
        )
        distances[start] = 0
        came_from = {start: None}

        get_links_and_weights(self, start, end_vector)
        start_time = time.time()
        if goal in self.graph:
            came_from = {start: None, goal: start}
            print(f"{time.time() - start_time} seconds elapsed")
            return self.generate_path(came_from, goal)

        while goal not in self.graph:
            # Relax edges up to (number of vertices - 1) times
            for _ in range(len(self.graph.copy()) - 1):
                for vertex in self.graph.copy():
                    print(vertex)
                    get_links_and_weights(self, vertex, end_vector)
                    for neighbor, weight in self.graph[vertex].items():
                        if distances[vertex] + weight < distances[neighbor]:
                            distances[neighbor] = distances[vertex] + weight
                            came_from[neighbor] = vertex
                if goal in self.graph:
                    print(f"{time.time() - start_time} seconds elapsed")
                    return self.generate_path(came_from, goal)

            # Check for negative weight cycles
            for vertex in self.graph:
                for neighbor, weight in self.graph[vertex].items():
                    if distances[vertex] + weight < distances[neighbor]:
                        raise ValueError(
                            "Graph contains a negative weight cycle"
                        )

        if distances[goal] == float("inf"):
            return []  # No path found
        print(f"{time.time() - start_time} seconds elapsed")
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

        path.reverse()
        self.path = path
        return path

# Run main function with: `python3 dijkstra.py --start "START" --end "END"`
@click.command()
@click.option('--start', type=str, help='Name of starting page')
@click.option('--end', type=str, help='Name of goal page')
def main(start,end):
    bf = BellmanFord({})
    result = bf.find_shortest_path(start=start, goal=end)
    print(result)

if __name__ == "__main__":
    main()
