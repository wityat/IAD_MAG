def graph_coloring_min_available_color_algorithm(graph):
    graph.set_sorted_vertices_by_degree()

    for vertex in graph.sorted_vertices:
        min_color = graph.get_min_available_color(vertex)
        graph.color_vertex(min_color, vertex)

    return max(graph.colors_clusters)
