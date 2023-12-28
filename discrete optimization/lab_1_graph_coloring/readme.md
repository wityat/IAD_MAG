# GRAPH COLORING PROBLEM

Здесь представлены решения для лабораторной работы по раскраске графов:

- [graph_coloring.py](./graph_coloring.py) - алгоритмы
- [models.py](./models.py) - класс Graph с нужными методами и класс AdjacencyList листа смежности
- [dimacs_reader.py](./dimacs_reader.py) - класс DIMACSReader для чтения файлов в формате DIMACS и создания Graph
- [test_graph_coloring.py](./test_graph_coloring.py) - тесты на алгоритмы

Тесты написаны на основе следующей таблицы:

| Instance        | Time in sec | Colors |
|-----------------|-------------|--------|
| myciel3.col     | ≤ 0.01      | ≤ 4    |
| myciel7.col     | ≤ 0.08      | ≤ 8    |
| school1.col     | ≤ 0.4       | ≤ 15   |
| school1_nsh.col | ≤ 0.3       | ≤ 21   |
| anna.col        | ≤ 0.04      | ≤ 11   |
| miles1000.col   | ≤ 0.04      | ≤ 42   |
| miles1500.col   | ≤ 0.25      | ≤ 73   |
| le450_5a.col    | ≤ 0.2       | ≤ 11   |
| le450_15b.col   | ≤ 0.2       | ≤ 18   |
| queen11_11.col  | ≤ 0.15      | ≤ 16   |


### Полученные результаты
- [Алгоритм где каждый раз выбирается вершина с самой высокой степенью](https://htmlpreview.github.io/?https://github.com/wityat/IAD_MAG/blob/master/discrete%20optimization/graph_coloring/graph_coloring_largest_first_algorithm.html)
- [Алгоритм где все вершины также отсортированы по не возрастанию и для каждой выбирается минимальный доступный цвет](https://htmlpreview.github.io/?https://github.com/wityat/IAD_MAG/blob/master/discrete+optimization/graph_coloring/graph_coloring_min_available_color_algorithm.html)

Таким образом graph_coloring_min_available_color_algorithm - показал лучший результат, однако для следующих датасетов ему не удалось найти оптимальный путь
- school1.col   32 <= 15
- school1_nsh.col 32 <= 15
- miles1000.col 43 <= 42
- queen11_11.col 19 <= 16
