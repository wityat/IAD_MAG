import time

import pytest
from models import *
from dimacs_reader import DIMACSReader


with open("results.csv", "w", newline='') as file:
    file.write(f"Shatilov Viktor;time\n")


@pytest.mark.parametrize("filename, max_time, min_or_exact_clique", [
    ("brock200_1.clq", 10, ("=", 21)),
    ("brock200_2.clq", 10, ("=", 12)),
    ("brock200_3.clq", 10, ("=", 15)),
    ("brock200_4.clq", 10, ("=", 17)),
    ("brock400_1.clq", 40, ("≥", 25)),
    ("brock400_2.clq", 40, ("≥", 25)),
    ("brock400_3.clq", 40, ("≥", 30)),
    ("brock400_4.clq", 40, ("≥", 25)),
    ("C125.9.clq", 10, ("=", 34)),
    ("gen200_p0.9_44.clq", 20, ("=", 44)),
    ("gen200_p0.9_55.clq", 20, ("=", 55)),
    ("hamming8-4.clq", 15, ("=", 16)),
    ("johnson16-2-4.clq", 3, ("=", 8)),
    ("johnson8-2-4.clq", 1, ("=", 4)),
    ("keller4.clq", 10, ("=", 11)),
    ("MANN_a27.clq", 500, ("=", 126)),
    ("MANN_a9.clq", 10, ("=", 16)),
    ("p_hat1000-1.clq", 500, ("=", 10)),
    ("p_hat1000-2.clq", 500, ("=", 46)),
    ("p_hat1500-1.clq", 1500, ("≥", 11)),
    ("p_hat300-3.clq", 35, ("=", 36)),
    ("p_hat500-3.clq", 100, ("=", 50)),
    ("san1000.clq", 1500, ("≥", 10)),
    ("sanr200_0.9.clq", 20, ("=", 42)),
    ("sanr400_0.7.clq", 40, ("=", 21)),
])
def test_find_max_clique_algorithm(filename, max_time, min_or_exact_clique):
    with open(f"DIMACS_all_ascii/{filename}", "r") as file:
        text = file.read()
        graph = DIMACSReader().read(text=text)

    start_time = time.time()
    max_clique = graph.find_max_clique()
    end_time = time.time()

    result = len(max_clique)

    with open("results.csv", "a", newline='') as file:
        formatted_time = f"{(end_time - start_time):.3f}"
        formatted_time_with_comma = formatted_time.replace('.', ',')
        file.write(f"{result};{formatted_time_with_comma}\n")

    for vertex in max_clique:
        for neighbor in max_clique:
            if neighbor != vertex:
                assert neighbor in graph.adjacency_list[vertex]

    condition, expected = min_or_exact_clique
    if condition == "≥":
        assert result >= expected, f"Expected a clique size of at least {expected}, but found {result}"
    else:  # condition == "=":
        assert result == expected, f"Expected a clique size of exactly {expected}, but found {result}"
    assert end_time - start_time <= max_time
