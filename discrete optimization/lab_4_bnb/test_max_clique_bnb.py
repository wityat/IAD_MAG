import time

import pytest
from dimacs_reader import DIMACSReader


with open("results.csv", "w", newline='') as file:
    file.write("")

@pytest.mark.parametrize("filename, clique_size", [
    ("brock200_1.clq", 21),
    ("brock200_2.clq", 12),
    ("brock200_3.clq", 15),
    ("brock200_4.clq", 17),
    # ("c-fat200-1.clq", 12),
    # ("c-fat200-2.clq", 24),
    # ("c-fat200-5.clq", 58),
    # ("c-fat500-1.clq", 14),
    # ("c-fat500-10.clq", 126),
    # ("c-fat500-2.clq", 26),
    # ("c-fat500-5.clq", 64),
    ("C125.9.clq", 34),
    ("gen200_p0.9_44.clq", 44),
    # ("gen200_p0.9_55.clq", 55),
    # ("johnson8-2-4.clq", 4),
    # ("johnson8-4-4.clq", 14),
    # ("johnson16-2-4.clq", 8),
    # ("hamming6-2.clq", 32),
    # ("hamming6-4.clq", 4),
    # ("hamming8-2.clq", 128),
    # ("hamming8-4.clq", 16),
    ("keller4.clq", 11),
    # ("MANN_a9.clq", 16),
    ("MANN_a27.clq", 126),
    ("MANN_a45.clq", 345),
    ("p_hat300-1.clq", 8),
    ("p_hat300-2.clq", 25),
    ("p_hat300-3.clq", 36),
    # ("san200_0.7_1.clq", 30),
    ("san200_0.7_2.clq", 18),
    # ("san200_0.9_1.clq", 70),
    # ("san200_0.9_2.clq", 60),
    ("san200_0.9_3.clq", 44),
    ("sanr200_0.7.clq", 18),  # Corrected the filename format
])
def test_find_max_clique_algorithm(filename, clique_size):
    with open(f"DIMACS_all_ascii/{filename}", "r") as file:
        text = file.read()
        graph = DIMACSReader().read(text=text)

    start_time = time.time()
    max_clique = graph.bnb_find_max_clique()
    end_time = time.time()

    result = len(max_clique)

    with open("results.csv", "a", newline='') as file:
        formatted_time = f"{(end_time - start_time):.3f}"
        formatted_time_with_comma = formatted_time.replace('.', ',')
        file.write(f"{filename};{formatted_time_with_comma}\n")


    for vertex in max_clique:
        for neighbor in max_clique:
            if neighbor != vertex:
                assert neighbor in graph.adjacency_list[vertex]

    assert result == clique_size, f"Expected a clique size of exactly {clique_size}, but found {result}"