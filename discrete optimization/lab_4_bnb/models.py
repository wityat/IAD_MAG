from math import floor

import cplex
from copy import copy
import random
import networkx as nx


class AdjacencyList(dict):
    def __init__(self):
        super().__init__()

    def update(self, v1, v2):
        v1 = int(v1)
        v2 = int(v2)
        if v1 not in self:
            self[v1] = set()
        if v2 not in self:
            self[v2] = set()
        self[v1].add(v2)
        self[v2].add(v1)  # Assuming undirected graph

    def is_adjacent(self, v1, v2):
        return v2 in self.get(v1, set())

    def get_non_adjacent_vertices(self, vertex):
        # Возвращает множество вершин, не смежных с данной вершиной
        return set(self.keys()) - self.get(vertex, set()) - {vertex}


class MaxCliqueSolver:
    def __init__(self, adjacency_list):
        self.eps = 0.001
        self.adjacency_list = adjacency_list
        self.num_vertices = len(adjacency_list.keys())
        self.problem = cplex.Cplex()
        # self.problem.parameters.mip.display.set(2)
        self.problem.objective.set_sense(self.problem.objective.sense.maximize)
        self.var_names = [f"x{i}" for i in self.adjacency_list.keys()]
        self.problem.variables.add(obj=[1.0] * self.num_vertices,
                                   lb=[0.0] * self.num_vertices,
                                   ub=[1.0] * self.num_vertices,
                                   types=[self.problem.variables.type.continuous] * self.num_vertices,
                                   names=self.var_names)
        self.STRATEGIES = [
            nx.coloring.strategy_largest_first,
            nx.coloring.strategy_random_sequential,
            nx.coloring.strategy_connected_sequential_bfs,
            nx.coloring.strategy_connected_sequential_dfs,
            nx.coloring.strategy_saturation_largest_first,
            nx.coloring.strategy_smallest_last,
    ]
        self.problem.set_log_stream(None)
        self.problem.set_results_stream(None)
        self.problem.set_warning_stream(None)
        self.problem.set_error_stream(None)

    @staticmethod
    def are_all_values_integers(values, eps=0.0001):
        for val in values:
            if abs(val - round(val)) >= eps:
                return False
        return True

    @staticmethod
    def get_independent_sets(graph: nx.Graph, strategies: list,
                             n_iter: int = 50, min_set_size: int = 3) -> list:
        independent_sets = set()
        for strategy in strategies:
            if strategy == nx.coloring.strategy_random_sequential:
                _n_iter = n_iter
            else:
                _n_iter = 1
            for _ in range(_n_iter):
                coloring_dct = nx.coloring.greedy_color(graph, strategy=strategy)
                color2nodes = dict()
                for node, color in coloring_dct.items():
                    if color not in color2nodes:
                        color2nodes[color] = []
                    color2nodes[color].append(node)
                for color, colored_nodes in color2nodes.items():
                    if len(colored_nodes) >= min_set_size:
                        colored_nodes = tuple(sorted(colored_nodes))
                        independent_sets.add(colored_nodes)
        independent_sets = [set(ind_set) for ind_set in independent_sets]
        return independent_sets

    def create_problem(self):
        for vertex in self.adjacency_list:
            for not_neighbor in self.adjacency_list.get_non_adjacent_vertices(vertex):
                if vertex < not_neighbor:  # Avoid adding the same constraint twice
                    self.problem.linear_constraints.add(
                        lin_expr=[[[f"x{vertex}", f"x{not_neighbor}"], [1.0, 1.0]]],
                        senses=["L"],
                        rhs=[1.0]
                    )
        graph = nx.Graph()
        for node, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                graph.add_edge(node, neighbor)
        independent_sets = self.get_independent_sets(graph, strategies=self.STRATEGIES)
        for ind_set in independent_sets:
            self.problem.linear_constraints.add(
                lin_expr=[[[f'x{i}' for i in ind_set], [1.0] * len(ind_set)]],
                senses=["L"],
                rhs=[1.0]
            )
    @staticmethod
    def get_branching_variable(numbers, eps=0.0001):
        closest_index = None
        closest_distance = float("inf")  # Инициализируем с бесконечностью

        for i, number in enumerate(numbers):
            distance = abs(number - 1)
            # Проверяем, что расстояние больше эпсилон и меньше текущего наименьшего расстояния
            if eps < distance < closest_distance:
                closest_distance = distance
                closest_index = i

        return closest_index


    def bnb_solve(self, clique_size=0, best_clique=None):
        if best_clique is None:
            best_clique = []
        try:
            self.problem.solve()
            x_vals = self.problem.solution.get_values(self.var_names)
            objective_value = self.problem.solution.get_objective_value()
        except cplex.exceptions.CplexSolverError:
            return clique_size, best_clique

        if floor(objective_value + self.eps) <= clique_size:
            return clique_size, best_clique

        # Проверяем, является ли решение целочисленным
        if self.are_all_values_integers(x_vals):
            current_clique_size = int(sum(x_vals))
            if current_clique_size > clique_size:
                best_clique = copy(x_vals)
                clique_size = current_clique_size
        else:
            # Находим переменную с дробным значением для ветвления
            branching_variable = self.get_branching_variable(x_vals)
            # Ветвление по переменной i
            original_upper_bound = self.problem.variables.get_upper_bounds(branching_variable)
            original_lower_bound = self.problem.variables.get_lower_bounds(branching_variable)
            for branch_value in [1.0, 0.0]:
                # Сначала принимаем переменную i в клику (устанавливаем x[i] = 1)
                self.problem.variables.set_upper_bounds([(branching_variable, branch_value)])
                self.problem.variables.set_lower_bounds([(branching_variable, branch_value)])
                clique_size, best_clique = self.bnb_solve(clique_size, best_clique)

                # Возвращаем оригинальные границы переменной
                self.problem.variables.set_upper_bounds([(branching_variable, original_upper_bound)])
                self.problem.variables.set_lower_bounds([(branching_variable, original_lower_bound)])

        return clique_size, best_clique

    def get_max_clique_vertices(self, best_clique):
        vertices = []
        for i, val in enumerate(best_clique):
            if abs(1.0 - round(val)) < self.eps:
                vertices.append(int(self.var_names[i].replace("x", "")))
        return vertices


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
                    if neighbor in clique_candidates:  # если этот сосед является соседом для всех кто в клике
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


    def bnb_find_max_clique(self):
        # Создание экземпляра MaxCliqueSolver

        solver = MaxCliqueSolver(self.adjacency_list)

        # Создание задачи для MaxCliqueSolver используя AdjacencyList
        solver.create_problem()

        # Решение задачи и получение максимальной клики
        # clique = self.greedy_find_max_clique()
        # cliques_as_x_vals = []
        # for i in self.adjacency_list.keys():
        #     cliques_as_x_vals.append(1.0 if i in clique else 0.0)

        # clique_size, max_clique = solver.bnb_solve(len(clique), cliques_as_x_vals)
        clique_size, max_clique = solver.bnb_solve()

        # Преобразуем индексы обратно в вершины
        max_clique_vertices = solver.get_max_clique_vertices(max_clique)

        return max_clique_vertices
