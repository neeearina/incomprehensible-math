from collections import deque
from typing import List


class WeightedGraph:
    """Класс для работы с неориентированным графом, заданным матрицей весов."""

    def __init__(self, weight_matrix: List[List[int]]):
        self.w = weight_matrix
        self.n = len(weight_matrix)

    @classmethod
    def from_file(cls, filename: str):
        """
        Создаёт граф, читая и проверяя матрицу весов из файла.
        0 - отсутствие ребра (вне диагонали), >0 - наличие ребра.
        """
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

        # Матрица не должна быть пустой
        if not matrix:
            raise ValueError("Файл пуст или не содержит матрицу.")

        n = len(matrix)

        # Матрица должна быть квадратной
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица должна быть квадратной.")

        # Проверка значений и диагонали
        for i in range(n):
            for j in range(n):
                val = matrix[i][j]
                if val < 0:
                    raise ValueError("Матрица весов не должна содержать отрицательные числа.")
                if i == j and val != 0:
                    raise ValueError("Матрица содержит петли (ненулевая диагональ).")

        # Проверка симметричности (неориентированный граф)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != matrix[j][i]:
                    raise ValueError("Матрица весов должна быть симметричной (неориентированный граф).")

        return cls(matrix)

    def neighbors(self, v: int) -> List[int]:
        """Возвращает список соседей вершины v (по положительным весам)."""
        return [u for u, w in enumerate(self.w[v]) if w > 0]

    def edges_count(self) -> int:
        """Возвращает количество рёбер графа."""
        m = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.w[i][j] > 0:
                    m += 1
        return m

    def is_connected(self) -> bool:
        """Проверяет, связен ли граф (одна компонента)."""
        if self.n == 0:
            return False

        visited = [False] * self.n
        queue = deque([0])
        visited[0] = True

        while queue:
            v = queue.popleft()
            for u in self.neighbors(v):
                if not visited[u]:
                    visited[u] = True
                    queue.append(u)

        return all(visited)

    def is_tree(self) -> bool:
        """Проверяет, является ли граф деревом."""
        # У дерева с n вершинами должно быть ровно n-1 ребро и граф должен быть связным
        if not self.is_connected():
            return False
        if self.edges_count() != self.n - 1:
            return False
        return True

    def tree_height_from_root(self, root: int = 0) -> int:
        """
        Вычисляет высоту дерева при корне root.
        Высота = максимальное расстояние от root до любой вершины (в рёбрах).
        Предполагается, что граф уже является деревом.
        """
        dist = [-1] * self.n
        dist[root] = 0
        queue = deque([root])

        while queue:
            v = queue.popleft()
            for u in self.neighbors(v):
                if dist[u] == -1:
                    dist[u] = dist[v] + 1
                    queue.append(u)

        return max(dist)


def print_matrix(matrix: List[List[int]]) -> None:
    """Печатает матрицу в удобочитаемом виде."""
    for row in matrix:
        print(" ".join(f"{x:3d}" for x in row))


def main() -> None:
    """
    Главная функция:
    - считывает имя файла с матрицей весов;
    - определяет, является ли граф деревом;
    - если нет — выводит '-';
    - если да — выводит высоту дерева (от вершины 1).
    """
    filename = input("Введите имя файла с матрицей весов: ").strip()

    print("\nШаг 1. Чтение и проверка матрицы")
    try:
        graph = WeightedGraph.from_file(filename)
    except Exception as e:
        print(f"Ошибка: {e}")
        print("\nГраф некорректен, считаем что он не является деревом.")
        print("\nВывод программы:")
        print("-")
        return

    print("Матрица весов успешно загружена.\n")
    print("Исходная матрица весов:")
    print_matrix(graph.w)

    print("\nШаг 2. Проверка, является ли граф деревом")
    if not graph.is_tree():
        print("Граф не является деревом.")
        print("\nВывод программы:")
        print("-")
        return

    print("Граф является деревом.")

    print("\nШаг 3. Вычисление высоты дерева")
    height = graph.tree_height_from_root(root=0)  # корень — вершина 1 (индекс 0)
    print(f"Высота дерева (от вершины 1): {height}")

    print("\nВывод программы:")
    print(height)


if __name__ == "__main__":
    main()