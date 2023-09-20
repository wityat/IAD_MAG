import time

import pytest
import requests
from graph_coloring import *
from dimacs_reader import DIMACSReader
import csv

with open("results.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["filename", "time", "num colors"])


@pytest.mark.parametrize("filename, expected_time, max_colors", [
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
])
def test_coloring_algorithm(filename, expected_time, max_colors):
    text = requests.get(f"https://mat.tepper.cmu.edu/COLOR/instances/{filename}").text
    graph = DIMACSReader().read(text=text)

    start_time = time.time()
    colors_clusters = graph_coloring_min_available_color_algorithm(graph)
    end_time = time.time()
    with open("results.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([filename, f"{(end_time - start_time):.3f}", len(colors_clusters)])

    for color, vertices in colors_clusters.items():
        for vertex in vertices:
            for neighbor in graph.adjacency_list[vertex]:
                assert neighbor not in colors_clusters.get(color, [])

    assert len(colors_clusters) <= max_colors
    assert end_time - start_time <= expected_time
