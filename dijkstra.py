from graph import Graph
from heapq import heapify, heappop, heappush

def dijkstra(start, end, graph: Graph):

    # Store nodes we already visited
    visited = set()

    # Initialize all distances between `start` to other nodes to infinity, start node will get 0
    distances = {key: float('inf') for key in graph} 
    distances[start] = 0

    pq = [(0, start)]

    while len(visited) != len(graph):
        # Iterate through root vertex's neighboring vertices
        for vertex, weight in graph[start].items():
            if vertex not in visited:
                if distances[vertex] + weight < distances[vertex]:
                    distances[vertex] += weight

        visited.append(start)


    return None



if __name__ == "__main__":
    test_graph = graph = {
                            "A": {"B": 3, "C": 3},
                            "B": {"A": 3, "D": 3.5, "E": 2.8},
                            "C": {"A": 3, "E": 2.8, "F": 3.5},
                            "D": {"B": 3.5, "E": 3.1, "G": 10},
                            "E": {"B": 2.8, "C": 2.8, "D": 3.1, "G": 7},
                            "F": {"G": 2.5, "C": 3.5},
                            "G": {"F": 2.5, "E": 7, "D": 10},
                        }
