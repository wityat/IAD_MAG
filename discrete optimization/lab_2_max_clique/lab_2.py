import random
import re
import time

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
            line = re.sub(r"\s+", " ", line).strip()
            line = re.sub(r'\s+', ' ', line)
            line_split = line.strip().replace("\n", "").split(" ")
            if line.startswith("c"):
                pass
            elif line.startswith("p edge"):
                graph.num_vertices = int(line_split[-2])
                graph.num_edges = int(line_split[-1])
            elif line.startswith("e"):
                graph.adjacency_list.update(line_split[1], line_split[2])
                graph.adjacency_list.update(line_split[2], line_split[1])
        return graph

if __name__ == "__main__":
    x = [
    ("brock200_1.clq", 15, ("≥", 20)),
    ("brock200_2.clq", 15, ("≥", 10)),
    ("brock200_3.clq", 15, ("≥", 14)),
    ("brock200_4.clq", 15, ("≥", 16)),
    ("brock400_1.clq", 75, ("≥", 24)),
    ("brock400_2.clq", 75, ("≥", 25)),
    ("brock400_3.clq", 75, ("≥", 24)),
    ("brock400_4.clq", 75, ("≥", 24)),
    ("C125.9.clq", 10, ("=", 34)),
    ("gen200_p0.9_44.clq", 20, ("≥", 40)),
    ("gen200_p0.9_55.clq", 20, ("≥", 48)),
    ("hamming8-4.clq", 20, ("=", 16)),
    ("johnson16-2-4.clq", 5, ("=", 8)),
    ("johnson8-2-4.clq", 5, ("=", 4)),
    ("keller4.clq", 10, ("=", 11)),
    ("MANN_a27.clq", 100, ("=", 126)),
    ("MANN_a9.clq", 5, ("=", 16)),
    ("p_hat1000-1.clq", 500, ("=", 10)),
    ("p_hat1000-2.clq", 500, ("=", 46)),
    ("p_hat1500-1.clq", 1000, ("≥", 11)),
    ("p_hat300-3.clq", 50, ("≥", 34)),
    ("p_hat500-3.clq", 150, ("≥", 49)),
    ("san1000.clq", 500, ("≥", 10)),
    ("sanr200_0.9.clq", 50, ("≥", 41)),
    ("sanr400_0.7.clq", 100, ("=", 21)),
]
    def find_max_clique_algorithm(filename, max_time, min_or_exact_clique):
        with open(f"DIMACS_all_ascii/{filename}", "r") as file:
            text = file.read()
            graph = DIMACSReader().read(text=text)

        start_time = time.time()
        max_clique = graph.greedy_find_max_clique()
        end_time = time.time()

        result = len(max_clique)

        formatted_time = f"{(end_time - start_time):.3f}"
        formatted_time_with_comma = formatted_time.replace('.', ',')
        print(f"{result};{formatted_time_with_comma}")

        for vertex in max_clique:
            for neighbor in max_clique:
                if neighbor != vertex:
                    assert neighbor in graph.adjacency_list[vertex]

        condition, expected = min_or_exact_clique
        if condition == "≥":
            if not result >= expected:
                print(f"Expected a clique size of at least {expected}, but found {result}")
        else:  # condition == "=":
            if not result == expected:
                print(f"Expected a clique size of exactly {expected}, but found {result}")
        assert end_time - start_time <= max_time

    for file in x:
        find_max_clique_algorithm(*file)
