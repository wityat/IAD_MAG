from tqdm import tqdm
import itertools


def get_all_subsets(s):
    all_subsets = []
    for length in range(1, len(s) + 1):
        subs = itertools.combinations(s, length)
        all_subsets += list(subs)
    return all_subsets


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

    def check_clique(self, clique):
        for vertex in clique:
            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in clique:
                    return False
        return True

    """
    # поделить отсортированный по степени вершин массив на сеты в словарь, где ключ - степень верштин, а в ссете индексы вершин
    выбрать те сеты, где количество элементов больше или равно степени
    в полученных множествах запустить проверку каждая с каждой, если какая-то из вершин указывает не на наше множество - удаляем
    Делать пока или не пройдем все вершины в множестве и не подтвердим клику или количество элементов множества станет больше степени множества
    """
    def find_max_clique(self):
        self.set_sorted_vertices_by_degree()

        for vertex in self.sorted_vertices:
            degree = self.get_vertex_degree(vertex)
            self.same_degree_groups.update(degree, vertex)

        max_clique = set()
        sorted_degrees = sorted(self.same_degree_groups, key=lambda k: k, reverse=True)

        for degree in tqdm(sorted_degrees):
            if degree <= len(max_clique):
                break

            group = set()
            for d in sorted_degrees:
                if d >= degree:
                    group |= self.same_degree_groups[d]

            for vertex in group:
                adjacency_vertices = self.adjacency_list[vertex]
                adjacency_vertices_subsets = get_all_subsets(adjacency_vertices)
                for subset in adjacency_vertices_subsets:
                    if group >= subset > len(max_clique) and self.check_clique(subset):
                        max_clique = subset


        return max_clique
