from collections import defaultdict
from models import ThreeHeap, BinomialHeap


def dijkstra_three_heap(graph, start):
    three_heap = ThreeHeap()
    distances = defaultdict(lambda: float('inf'))
    distances[start] = 0
    three_heap.insert((0, start))

    while three_heap.heap:
        current_distance, current_node = three_heap.extract_min()
        for neighbor, weight in graph[current_node]:
            distance = distances[current_node] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                three_heap.insert((distance, neighbor))

    return distances


def dijkstra_binomial_heap(graph, start):
    binomial_heap = BinomialHeap()
    distances = defaultdict(lambda: float('inf'))
    distances[start] = 0
    binomial_heap.insert((0, start))

    while binomial_heap.head is not None:
        current_distance, current_node = binomial_heap.extract_min()
        for neighbor, weight in graph[current_node]:
            distance = distances[current_node] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                binomial_heap.insert((distance, neighbor))

    return distances
