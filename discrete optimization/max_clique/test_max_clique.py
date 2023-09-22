import time

import pytest
from models import *
from dimacs_reader import DIMACSReader
import csv

with open("results.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["filename", "time", "num vertices"])


@pytest.mark.parametrize("filename, max_time, min_or_exact_clique", [
    ("brock200_1.clq", 15, ("≥", 20)),
    # ("brock200_2.clq", 15, ("≥", 10)),
    # ("brock200_3.clq", 15, ("≥", 14)),
    # ("brock200_4.clq", 15, ("≥", 16)),
    # ("brock400_1.clq", 75, ("≥", 24)),
    # ("brock400_2.clq", 75, ("≥", 25)),
    # ("brock400_3.clq", 75, ("≥", 24)),
    # ("brock400_4.clq", 75, ("≥", 24)),
    # ("C125.9.clq", 10, ("=", 34)),
    # ("gen200_p0.9_44.clq", 20, ("≥", 40)),
    # ("gen200_p0.9_55.clq", 20, ("≥", 48)),
    # ("hamming8-4.clq", 20, ("=", 16)),
    # ("johnson16-2-4.clq", 5, ("=", 8)),
    # ("johnson8-2-4.clq", 5, ("=", 4)),
    # ("keller4.clq", 10, ("=", 11)),
    # ("MANN_a27.clq", 100, ("=", 126)),
    # ("MANN_a9.clq", 5, ("=", 16)),
    # ("p_hat1000-1.clq", 500, ("=", 10)),
    # ("p_hat1000-2.clq", 500, ("=", 46)),
    # ("p_hat1500-1.clq", 1000, ("≥", 11)),
    # ("p_hat300-3.clq", 50, ("≥", 34)),
    # ("p_hat500-3.clq", 150, ("≥", 49)),
    # ("san1000.clq", 500, ("≥", 10)),
    # ("sanr200_0.9.clq", 50, ("≥", 41)),
    # ("sanr400_0.7.clq", 100, ("=", 21)),
])
def test_find_max_clique_algorithm(filename, max_time, min_or_exact_clique):
    with open(f"DIMACS_all_ascii/{filename}", "r") as file:
        text = file.read()
        graph = DIMACSReader().read(text=text)

    start_time = time.time()
    max_clique = graph.find_max_clique()
    end_time = time.time()

    result = len(max_clique)

    with open("results.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([filename, f"{(end_time - start_time):.3f}", result])

    for vertex in max_clique:
        for neighbor in graph.adjacency_list[vertex]:
            assert neighbor in max_clique

    condition, expected = min_or_exact_clique
    if condition == "≥":
        assert result >= expected, f"Expected a clique size of at least {expected}, but found {result}"
    else:  # condition == "=":
        assert result == expected, f"Expected a clique size of exactly {expected}, but found {result}"
    assert end_time - start_time <= max_time
