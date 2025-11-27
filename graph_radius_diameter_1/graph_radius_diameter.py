from collections import deque
from math import inf


class Graph:
    """Класс для работы с неориентированным графом по матрице смежности."""

    def __init__(self, adjacency_matrix):
        self.adj = adjacency_matrix
        self.n = len(adjacency_matrix)

    @classmethod
    def from_file(cls, filename):
        """Создаёт граф, читая матрицу смежности из файла."""
        matrix = []

        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    row = line.strip().split()
                    if row:
                        # проверка: элементы должны быть числами
                        if not all(x.isdigit() for x in row):
                            raise ValueError("Матрица содержит недопустимые символы.")
                        row = [int(x) for x in row]
                        matrix.append(row)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{filename}' не найден.")

        # Проверка, что матрица не пустая
        if not matrix:
            raise ValueError("Файл пуст или не содержит матрицу.")

        # Проверка, что матрица квадратная
        n = len(matrix)
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица должна быть квадратной.")

        # Проверка, что матрица состоит из 0 и 1
        for row in matrix:
            if any(x not in (0, 1) for x in row):
                raise ValueError("Матрица должна содержать только 0 и 1.")

        # Проверка симметричности матрицы (граф неориентированный)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != matrix[j][i]:
                    raise ValueError("Матрица должна быть симметричной (неориентированный граф).")

        return cls(matrix)

    def neighbors(self, v):
        """Возвращает список соседей вершины v."""
        return [u for u, has_edge in enumerate(self.adj[v]) if has_edge]

    def bfs_distances(self, start):
        """Считает расстояния от вершины start до всех остальных (BFS)."""
        dist = [inf] * self.n
        dist[start] = 0
        queue = deque([start])

        while queue:
            v = queue.popleft()
            for u in self.neighbors(v):
                if dist[u] is inf:
                    dist[u] = dist[v] + 1
                    queue.append(u)

        return dist

    def eccentricity(self, v):
        """Возвращает эксцентриситет вершины v."""
        return max(self.bfs_distances(v))

    def is_connected(self):
        """Проверяет, связен ли граф."""
        return all(d is not inf for d in self.bfs_distances(0))

    def diameter(self):
        """Вычисляет диаметр графа."""
        ecc = [self.eccentricity(v) for v in range(self.n)]
        return int(max(ecc))

    def radius(self):
        """Вычисляет радиус графа."""
        ecc = [self.eccentricity(v) for v in range(self.n)]
        return int(min(ecc))


def print_matrix(matrix):
    """Печатает матрицу в красивом виде."""
    for row in matrix:
        print(" ".join(map(str, row)))


def main():
    """Точка входа."""
    filename = input("Введите имя файла с матрицей: ").strip()

    try:
        graph = Graph.from_file(filename)
    except Exception as e:
        print(f"Произошла ошибка при чтении: {e}")
        return

    print("Загруженная матрица смежности из файла:\n")
    print_matrix(graph.adj)

    print("\nРезультат:")

    if not graph.is_connected():
        print("Граф несвязный, поэтому радиус и диаметр не определены.")
        return

    d = graph.diameter()
    r = graph.radius()

    print(f"Диаметр графа: {d}")
    print(f"Радиус графа: {r}")


if __name__ == "__main__":
    main()
