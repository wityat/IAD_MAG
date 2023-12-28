from models import Graph


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
