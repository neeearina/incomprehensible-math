from collections import deque
from typing import List


class WeightedGraph:
    """Класс для работы с графом, заданным матрицей весов."""

    def __init__(self, weight_matrix: List[List[int]]):
        """Сохраняет матрицу весов и строит список смежности."""
        self.w = weight_matrix
        self.n = len(weight_matrix)
        self.adj_list = self._build_adj_list()

    @classmethod
    def from_file(cls, filename: str) -> "WeightedGraph":
        """Создаёт граф, читая и проверяя матрицу весов из файла."""
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

        if not matrix:
            raise ValueError("Файл пуст или не содержит матрицу.")

        n = len(matrix)

        # Проверка квадратности
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица весов должна быть квадратной.")

        # Проверка значений
        for i in range(n):
            for j in range(n):
                val = matrix[i][j]
                if val < 0:
                    raise ValueError("Матрица весов не должна содержать отрицательные числа.")
                if i == j and val != 0:
                    raise ValueError("Матрица содержит петли (ненулевая диагональ).")

        # Не требуем симметричности — граф может быть ориентированным
        return cls(matrix)

    def _build_adj_list(self) -> List[List[int]]:
        """Строит список смежности из матрицы весов."""
        adj: List[List[int]] = [[] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if self.w[i][j] > 0:
                    adj[i].append(j)
        return adj

    def bfs_iterative(self, start: int) -> List[int]:
        """Выполняет нерекурсивный поиск в ширину (BFS) от вершины start."""
        visited = [False] * self.n
        order: List[int] = []
        queue = deque([start])
        visited[start] = True

        while queue:
            v = queue.popleft()
            order.append(v)
            for u in self.adj_list[v]:
                if not visited[u]:
                    visited[u] = True
                    queue.append(u)

        return order

    def dfs_iterative(self, start: int) -> List[int]:
        """Выполняет нерекурсивный поиск в глубину (DFS) от вершины start."""
        visited = [False] * self.n
        order: List[int] = []
        stack = [start]

        while stack:
            v = stack.pop()
            if visited[v]:
                continue
            visited[v] = True
            order.append(v)
            # Чтобы обход был «естественным», соседей можно добавлять в стек в обратном порядке
            for u in reversed(self.adj_list[v]):
                if not visited[u]:
                    stack.append(u)

        return order


def print_matrix(matrix: List[List[int]]) -> None:
    """Печатает матрицу в удобочитаемом виде."""
    for row in matrix:
        print(" ".join(f"{x:3d}" for x in row))


def print_adj_list(adj_list: List[List[int]]) -> None:
    """Печатает список смежности с вершинами, нумеруемыми с 1."""
    for i, neighbors in enumerate(adj_list):
        # +1, чтобы показать вершины, начиная с 1
        neighbors_str = ", ".join(f"v{v+1}" for v in neighbors) if neighbors else "∅"
        print(f"v{i+1}: {neighbors_str}")


def print_order(order: List[int], label: str) -> None:
    """Печатает порядок обхода вершин с указанной подписью."""
    # +1, чтобы выводить вершины, нумеруя их с 1
    numbered = [f"v{v+1}" for v in order]
    print(f"{label}: {' → '.join(numbered) if numbered else '(нет вершин)'}")


def main() -> None:
    """
    Главная функция:
    - считывает имя файла с матрицей весов;
    - строит список смежности;
    - выполняет нерекурсивные BFS и DFS;
    - выводит результаты.
    """
    filename = input("Введите имя файла с матрицей весов: ").strip()

    print("\nШаг 1. Чтение и проверка матрицы весов")
    try:
        graph = WeightedGraph.from_file(filename)
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Программа завершена из-за некорректных данных.")
        return

    print("Матрица весов успешно загружена.\n")

    print("Исходная матрица весов:")
    print_matrix(graph.w)

    print("\nПостроенный список смежности (по строкам, 1..n):")
    print_adj_list(graph.adj_list)

    # Выбор стартовой вершины
    print("\nШаг 2. Выбор стартовой вершины")
    print(f"Количество вершин в графе: {graph.n}")
    raw = input("Введите номер стартовой вершины (1..n), Enter по умолчанию = 1: ").strip()

    if raw == "":
        start = 0
    else:
        try:
            s = int(raw)
            if not (1 <= s <= graph.n):
                raise ValueError
            start = s - 1
        except ValueError:
            print("Некорректный ввод. Используется вершина 1 по умолчанию.")
            start = 0

    print(f"\nСтартовая вершина: v{start+1}")

    print("\n=== Шаг 3. Поиск в ширину (BFS) ===")
    bfs_order = graph.bfs_iterative(start)
    print_order(bfs_order, "Порядок обхода BFS")

    print("\n=== Шаг 4. Поиск в глубину (DFS, нерекурсивный) ===")
    dfs_order = graph.dfs_iterative(start)
    print_order(dfs_order, "Порядок обхода DFS")

    print("\nРабота программы завершена.")


if __name__ == "__main__":
    main()