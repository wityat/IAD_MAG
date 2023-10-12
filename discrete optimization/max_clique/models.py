import random

from tqdm import tqdm


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

        self.sorted_vertices = None
        self.set_sorted_vertices = None
        self.same_degree_groups = AdjacencyList()

    def get_vertex_degree(self, vertex):
        return len(self.adjacency_list[vertex])

    def get_max_vertex_by_degree(self, vertices):
        return sorted(vertices, key=lambda k: len(self.adjacency_list[k]), reverse=True)[0]

    def set_sorted_vertices_by_degree(self):
        self.sorted_vertices = sorted(self.adjacency_list, key=lambda k: len(self.adjacency_list[k]), reverse=True)
        self.set_sorted_vertices = set(self.sorted_vertices)

    def get_random_vertices(self, vertices: list, num: int = 3):
        return random.choice(vertices[0:num])

    def greedy_find_max_clique(self):
        self.set_sorted_vertices_by_degree()
        max_clique = set()
        for x in range(int(len(self.sorted_vertices)*2.5)):
            for vertex in self.sorted_vertices:
                potential_clique = {vertex}
                sorted_neighbors = sorted(self.adjacency_list[vertex],
                                          key=lambda k: len(self.adjacency_list[k]),
                                          reverse=True)
                clique_candidates = self.adjacency_list[vertex]
                candidates_to_add = []
                for neighbor in sorted_neighbors:
                    if neighbor in clique_candidates:  # если этот сосед явялется соседом для всех кто в клике
                        candidates_to_add.append(neighbor)
                    if len(candidates_to_add) == 3:
                        vertex_to_add = random.choice(candidates_to_add)
                        potential_clique.add(vertex_to_add)
                        clique_candidates = clique_candidates & self.adjacency_list[vertex_to_add]
                        for c in candidates_to_add:
                            if c != vertex_to_add and c in clique_candidates:
                                potential_clique.add(c)
                                clique_candidates = clique_candidates & self.adjacency_list[c]
                        candidates_to_add = []
                if len(potential_clique) > len(max_clique):
                    max_clique = potential_clique

        return max_clique

    # def greedy_find_max_clique(self):
    #     self.set_sorted_vertices_by_degree()
    #     self.max_clique = set()
    #
    #     def add_neighbor_to_clique(neighbor):
    #         if all(neighbor in self.adjacency_list[v] for v in potential_clique):
    #             potential_clique.append(neighbor)
    #             if len(potential_clique) > len(self.max_clique):
    #                 self.max_clique = set(potential_clique)
    #             return neighbor
    #         else:
    #             return None
    #
    #     def step_deep(vertex):
    #         next_vertex = None
    #         sorted_neighbors = sorted(self.adjacency_list[vertex], key=lambda k: len(self.adjacency_list[k]),
    #                                   reverse=True)
    #         while not next_vertex and sorted_neighbors:
    #             neighbor = random.choice(sorted_neighbors[0:3])
    #             next_vertex = add_neighbor_to_clique(neighbor)
    #             sorted_neighbors.remove(neighbor)
    #         if next_vertex:
    #             step_deep(vertex)
    #         else:
    #             return
    #
    #     for i, vertex in enumerate(self.sorted_vertices):
    #         potential_clique = [vertex]
    #         step_deep(vertex)
    #
    #     return self.max_clique

