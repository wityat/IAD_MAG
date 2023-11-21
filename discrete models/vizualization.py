import networkx as nx
import matplotlib.pyplot as plt


def viz_graph(graph):
    # Создаем пустой граф
    G = nx.Graph()

    # Добавляем ребра и их веса в граф
    for node, edges in graph.items():
        for edge, weight in edges:
            G.add_edge(node, edge, weight=weight)

    # Визуализируем граф
    pos = nx.spring_layout(G)  # расположение узлов
    nx.draw(G, pos, with_labels=True)  # рисуем узлы и ребра
    labels = nx.get_edge_attributes(G, 'weight')  # получаем веса ребер
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)  # рисуем веса ребер
    plt.show()
    return G


def viz_distances_in_graph(G, distances):
    # Визуализируем граф с расстояниями
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Добавляем расстояния до узлов
    for node, distance in distances.items():
        plt.text(pos[node][0], pos[node][1] + 0.1, str(distance), horizontalalignment='center')

    plt.show()
