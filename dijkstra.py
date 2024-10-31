from scraper import *
from graph import Graph

import time
import click
from collections import defaultdict
from heapq import heapify, heappop, heappush

class Dijkstra(Graph):
    def __init__(self, graph_dict: dict) -> None:
        super().__init__(graph_dict)
        self.path = None

    def find_shortest_path(self, start: str, goal: str) -> list:
        """
        Compute the shortest path from the start node to the goal node using Dijkstra's algorithm.
        
        Args:
            start: The starting vertex (source)
            goal: The target vertex (goal)

        Returns:
            path: List of vertices that make up the shortest path, or a dictionary with distances if no path is found.
        """
        end_vector = model.get_word_vector(goal)

        visited = set()  # Keep track of visited nodes
        distances = defaultdict(lambda: float("inf"), {key: float("inf") for key in self.graph})
        distances[start] = 0  # Start node has distance 0

        # Priority queue to store (distance, vertex), initially with just the start vertex
        pq = [(0, start)]
        heapify(pq)

        # Track the path: which node we came from to get to each node
        came_from = {start: None}
        
        start_time = time.time()
        while pq:
            cur_dist, cur_node = heappop(pq)
            print(cur_node)
            # If the goal is reached, generate and return the path
            if cur_node.lower() == goal.lower():
                print(f"{time.time() - start_time} seconds elapsed")
                print(f"{len(visited)} articles visited")
                return self.generate_path(came_from, cur_node)

            if cur_node in visited:
                continue

            visited.add(cur_node)
            get_links_and_weights(self, cur_node, end_vector)

            # Process all neighbors of the current node
            for neighbor, weight in self.graph[cur_node].items():
                if neighbor not in visited:
                    # Calculate the tentative distance to this neighbor
                    tent_dist = cur_dist + weight
                    if tent_dist < distances[neighbor]:
                        came_from[neighbor] = cur_node # type: ignore
                        distances[neighbor] = tent_dist
                        heappush(pq, (tent_dist, neighbor))
        return []

    def generate_path(self, came_from: dict, curr_node: str):
        """
        Generate the path from start to goal after running Dijkstra's algorithm.

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


# Run main function with: `python3 dijkstra.py --start "START" --end "END"`
@click.command()
@click.option('--start', type=str, help='Name of starting page')
@click.option('--end', type=str, help='Name of goal page')
def main(start,end):
    dijk_dynamic = Dijkstra({})
    result = dijk_dynamic.find_shortest_path(start=start, goal=end)
    print(result)

if __name__ == "__main__":
    main()
