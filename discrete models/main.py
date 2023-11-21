import algorithms
from vizualization import *
from tests import generate_graph

def input_graph():
    # Запросим количество вершин и ребер
    num_nodes = int(input("Введите количество вершин: "))
    num_edges = int(input("Введите количество ребер: "))

    # Создадим пустой граф
    graph = {i: [] for i in range(num_nodes)}

    # Запросим информацию о каждом ребре
    for _ in range(num_edges):
        node1 = int(input("Введите вершину 1: "))
        node2 = int(input("Введите вершину 2: "))
        weight = int(input("Введите вес ребра: "))
        graph[node1].append((node2, weight))
        graph[node2].append((node1, weight))  # если граф неориентированный

    return graph

def main(algo_name: str):
    graph = generate_graph(10)
    G = viz_graph(graph)
    distances = getattr(algorithms, algo_name)(graph, 'A')
    viz_distances_in_graph(G, distances)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
