import time
import random
import matplotlib.pyplot as plt
from algorithms import *


def generate_graph(n):
    """Генерация случайного графа с n вершинами."""
    graph = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:  # 50% шанс создания ребра
                weight = random.randint(1, 10)
                graph[i].append((j, weight))
                graph[j].append((i, weight))
    return graph


def test_dijkstra_three_heap():
    graph = {
        'A': [('B', 1), ('C', 3)],
        'B': [('A', 1), ('C', 2)],
        'C': [('A', 3), ('B', 2)]
    }
    distances = dijkstra_three_heap(graph, 'A')
    assert distances == {'A': 0, 'B': 1, 'C': 3}


def test_dijkstra_binomial_heap():
    graph = {
        'A': [('B', 1), ('C', 3)],
        'B': [('A', 1), ('C', 2)],
        'C': [('A', 3), ('B', 2)]
    }
    distances = dijkstra_binomial_heap(graph, 'A')
    assert distances == {'A': 0, 'B': 1, 'C': 3}

if __name__ == "__main__":

# Измерение времени выполнения алгоритмов
    sizes = range(10, 1001, 5)
    times_three_heap = []
    times_binomial_heap = []
    for n in sizes:
        graph = generate_graph(n)

        start_time = time.time()
        dijkstra_three_heap(graph, 0)
        end_time = time.time()
        times_three_heap.append(end_time - start_time)

        start_time = time.time()
        dijkstra_binomial_heap(graph, 0)
        end_time = time.time()
        times_binomial_heap.append(end_time - start_time)

    # Построение графика
    plt.plot(sizes, times_three_heap, label='ThreeHeap')
    plt.plot(sizes, times_binomial_heap, label='BinomialHeap')
    plt.xlabel('Размер графа')
    plt.ylabel('Время выполнения (сек)')
    plt.legend()
    plt.show()

