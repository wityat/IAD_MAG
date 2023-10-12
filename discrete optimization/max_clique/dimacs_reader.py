import re
from models import Graph


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
            line_split = line.replace("\n", "").split(" ")
            if line.startswith("c"):
                pass
            elif line.startswith("p edge"):
                graph.num_vertices = int(line_split[-2])
                graph.num_edges = int(line_split[-1])
            elif line.startswith("e"):
                graph.adjacency_list.update(line_split[1], line_split[2])
                graph.adjacency_list.update(line_split[2], line_split[1])
        return graph
