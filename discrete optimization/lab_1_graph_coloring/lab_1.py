import csv

import requests
import time
from typing import Iterable


class AdjacencyList(dict):
    def __init__(self):
        super().__init__()

    def update(self, v1, v2):
        v1 = int(v1)
        v2 = int(v2)
        if not self.get(v1):
            self[v1] = set()
        if v2 not in self[v1]:
            self[v1].add(v2)


class Graph:
    def __init__(self):
        self.num_vertices = 0
        self.num_edges = 0
        self.adjacency_list = AdjacencyList()
        self.colors_clusters = AdjacencyList()
        self.colored_vertices = set()
        self.sorted_vertices = None
        self.set_sorted_vertices = None

    def color_vertex(self, color: int, vertex: int):
        self.colors_clusters.update(color, vertex)
        self.colored_vertices.add(vertex)

    def uncolor_vertex(self, color: int, vertex: int):
        self.colors_clusters[color].remove(vertex)
        self.colored_vertices.remove(vertex)

    def color_vertices(self, color: int, vertices: Iterable):
        for vertex in vertices:
            if vertex not in self.colored_vertices:
                self.color_vertex(color, vertex)

    def get_max_not_colored_vertex(self):
        for v in self.sorted_vertices:
            if v not in self.colored_vertices:
                yield v

    def get_not_adjacency_vertices_by_color(self, color):
        adjacency_vertices = set()
        for vertex in self.colors_clusters[color]:
            adjacency_vertices.update(self.adjacency_list[vertex])
        return self.set_sorted_vertices - adjacency_vertices - self.colored_vertices

    def get_min_available_color(self, vertex: int) -> int:
        adjacent_colors = set(self.get_color_of_vertex(neigh) for neigh in self.adjacency_list[vertex])
        color = 1
        while color in adjacent_colors:
            color += 1
        return color

    def get_color_of_vertex(self, vertex):
        for color, vertices in self.colors_clusters.items():
            if vertex in vertices:
                return color

    def get_max_vertex_by_degree(self, vertices):
        return sorted(vertices, key=lambda k: len(self.adjacency_list[k]), reverse=True)[0]

    def set_sorted_vertices_by_degree(self):
        self.sorted_vertices = sorted(self.adjacency_list, key=lambda k: len(self.adjacency_list[k]), reverse=True)
        self.set_sorted_vertices = set(self.sorted_vertices)


class DIMACSReader:
    def __init__(self):
        pass

    def read(self, filename: str = None, text: str = None):
        if filename:
            with open(filename, "r") as file:
                text = file.read()
        return self.process(text)

    def process(self, text):
        graph = Graph()
        for line in text.split("\n"):
            line_split = line.replace("\n", "").split(" ")
            if line.startswith("c"):
                pass
            elif line.startswith("p edge"):
                graph.num_vertices = int(line_split[-2])
                graph.num_edges = int(line_split[-1])
            elif line.startswith("e"):
                graph.adjacency_list.update(line_split[1], line_split[2])
                graph.adjacency_list.update(line_split[2], line_split[1])
        return graph


def graph_coloring_largest_first_algorithm(graph: Graph):
    graph.set_sorted_vertices_by_degree()
    color = 1
    while len(graph.colored_vertices) < graph.num_vertices:
        graph.color_vertex(color, next(graph.get_max_not_colored_vertex()))

        while not_adjacency_vertices := graph.get_not_adjacency_vertices_by_color(color):
            graph.color_vertex(color, graph.get_max_vertex_by_degree(not_adjacency_vertices))

        color += 1
    return graph.colors_clusters


def graph_coloring_min_available_color_algorithm(graph: Graph):
    graph.set_sorted_vertices_by_degree()

    for vertex in graph.sorted_vertices:
        min_color = graph.get_min_available_color(vertex)
        graph.color_vertex(min_color, vertex)

    return graph.colors_clusters



x = [
    ("myciel3.col", 0.01, 4),
    ("myciel7.col", 0.08, 8),
    ("school1.col", 0.4, 15),
    ("school1_nsh.col", 0.3, 21),
    ("anna.col", 0.04, 11),
    ("miles1000.col", 0.04, 42),
    ("miles1500.col", 0.25, 73),
    ("le450_5a.col", 0.2, 11),
    ("le450_15b.col", 0.2, 18),
    ("queen11_11.col", 0.15, 16),
]
def coloring_algorithm(filename, expected_time, max_colors):
    text = requests.get(f"https://mat.tepper.cmu.edu/COLOR/instances/{filename}").text
    graph = DIMACSReader().read(text=text)

    start_time = time.time()
    colors_clusters = graph_coloring_largest_first_algorithm(graph)
    end_time = time.time()
    print(filename, f"{(end_time - start_time):.3f}", len(colors_clusters))

    for color, vertices in colors_clusters.items():
        for vertex in vertices:
            for neighbor in graph.adjacency_list[vertex]:
                assert neighbor not in colors_clusters.get(color, [])

    if not len(colors_clusters) <= max_colors:
        print(f"Expected a quantity colors clusters of at most {max_colors}, but found {len(colors_clusters)}")
    if not end_time - start_time <= expected_time:
        print(f"Expected time of at most {expected_time}, but there is {end_time - start_time}")

for file in x:
    coloring_algorithm(*file)
