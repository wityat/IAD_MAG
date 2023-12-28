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
