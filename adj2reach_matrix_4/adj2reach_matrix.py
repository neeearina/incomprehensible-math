from collections import deque
from typing import List


class Graph:
    """Класс для работы с графом по матрице смежности."""

    def __init__(self, adjacency_matrix: List[List[int]]):
        self.adj = adjacency_matrix
        self.n = len(adjacency_matrix)

    @classmethod
    def from_file(cls, filename: str) -> "Graph":
        """Создаёт граф, читая и проверяя матрицу смежности из файла."""
        matrix: List[List[int]] = []

        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    row_str = line.strip().split()
                    if not row_str:
                        continue
                    try:
                        row = [int(x) for x in row_str]
                    except ValueError:
                        raise ValueError("Матрица содержит нечисловые значения.")
                    matrix.append(row)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{filename}' не найден.")

        # Проверка: матрица не пустая
        if not matrix:
            raise ValueError("Файл пуст или не содержит матрицу.")

        # Проверка: квадратная матрица
        n = len(matrix)
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица смежности должна быть квадратной.")

        # Проверка: элементы только 0 или 1
        for row in matrix:
            for x in row:
                if x not in (0, 1):
                    raise ValueError("Матрица смежности должна содержать только 0 и 1.")

        return cls(matrix)

    def neighbors(self, v: int) -> List[int]:
        """Возвращает список соседей вершины v (куда есть ребро)."""
        return [u for u, has_edge in enumerate(self.adj[v]) if has_edge == 1]

    def bfs_reachable(self, start: int) -> List[bool]:
        """Находит достижимые вершины из start с помощью BFS."""
        reachable = [False] * self.n
        queue = deque([start])
        reachable[start] = True  # вершина достижима сама из себя

        while queue:
            v = queue.popleft()
            for u in self.neighbors(v):
                if not reachable[u]:
                    reachable[u] = True
                    queue.append(u)

        return reachable

    def reachability_matrix(self) -> List[List[int]]:
        """Строит и возвращает матрицу достижимости."""
        reach = [[0] * self.n for _ in range(self.n)]

        for v in range(self.n):
            reachable = self.bfs_reachable(v)
            for u in range(self.n):
                reach[v][u] = 1 if reachable[u] else 0

        return reach


def print_matrix(matrix: List[List[int]]) -> None:
    """Печатает матрицу в удобном виде."""
    if not matrix:
        print("(пустая матрица)")
        return
    for row in matrix:
        print(" ".join(f"{x:2d}" for x in row))


def main() -> None:
    """Главная функция: чтение файла, вывод матриц и сообщений."""
    filename = input("Введите имя файла с матрицей смежности: ").strip()

    print("\nШаг 1. Чтение и проверка матрицы смежности")
    try:
        graph = Graph.from_file(filename)
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Программа завершена из-за некорректных данных.")
        return

    print("Матрица смежности успешно загружена.\n")
    print("Исходная матрица смежности:")
    print_matrix(graph.adj)

    print("\nШаг 2. Построение матрицы достижимости")
    reach = graph.reachability_matrix()

    print("\nМатрица достижимости:")
    print_matrix(reach)

    print("\nРабота программы завершена успешно.")


if __name__ == "__main__":
    main()