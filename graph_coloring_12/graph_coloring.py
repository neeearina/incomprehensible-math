from typing import List, Optional


class Graph:
    """Класс для работы с неориентированным графом, заданным матрицей весов."""

    def __init__(self, adjacency_matrix: List[List[int]]):
        """Сохраняет матрицу смежности и строит список смежности."""
        self.adj = adjacency_matrix
        self.n = len(adjacency_matrix)
        self.adj_list = self._build_adjacency_list()

    @classmethod
    def from_weight_matrix_file(cls, filename: str) -> "Graph":
        """
        Создаёт граф, читая матрицу весов из файла и преобразуя её в матрицу смежности.

        Формат:
        - квадратная матрица n x n;
        - 0 на диагонали (нет петель);
        - 0 вне диагонали — ребра нет;
        - положительное число вне диагонали — есть ребро (вес игнорируем, важен сам факт).
        """
        matrix: List[List[int]] = []

        # Чтение файла
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

        # Проверки
        if not matrix:
            raise ValueError("Файл пуст или не содержит матрицу.")

        n = len(matrix)

        # Квадратность
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица должна быть квадратной.")

        # Значения и диагональ
        for i in range(n):
            for j in range(n):
                val = matrix[i][j]
                if val < 0:
                    raise ValueError("Матрица весов не должна содержать отрицательные значения.")
                if i == j and val != 0:
                    raise ValueError("Матрица содержит петли (ненулевая диагональ).")

        # Симметричность (неориентированный граф)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != matrix[j][i]:
                    raise ValueError("Матрица должна быть симметричной (неориентированный граф).")

        # Строим матрицу смежности 0/1
        adj = [[1 if matrix[i][j] > 0 else 0 for j in range(n)] for i in range(n)]

        return cls(adj)

    def _build_adjacency_list(self) -> List[List[int]]:
        """Строит список смежности из матрицы смежности."""
        adj_list: List[List[int]] = [[] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if self.adj[i][j] == 1:
                    adj_list[i].append(j)
        return adj_list

    def is_safe_color(self, v: int, color: int, colors: List[int]) -> bool:
        """Проверяет, можно ли покрасить вершину v в цвет color."""
        for u in self.adj_list[v]:
            if colors[u] == color:  # сосед уже имеет этот цвет
                return False
        return True

    def _color_with_k(self, k: int) -> Optional[List[int]]:
        """
        Пытается раскрасить граф в k цветов (точно).
        Возвращает список цветов для вершин (0..n-1) или None, если не получилось.
        """
        colors = [0] * self.n  # 0 - не раскрашена, цвета 1..k

        # Для лучшей эффективности красим вершины в порядке убывания степени
        order = sorted(range(self.n), key=lambda v: -len(self.adj_list[v]))

        def backtrack(idx: int) -> bool:
            if idx == self.n:
                return True
            v = order[idx]
            for c in range(1, k + 1):
                if self.is_safe_color(v, c, colors):
                    colors[v] = c
                    if backtrack(idx + 1):
                        return True
                    colors[v] = 0
            return False

        if backtrack(0):
            return colors
        return None

    def chromatic_number(self) -> (int, List[int]):
        """
        Находит хроматическое число графа и одну из оптимальных раскрасок.
        Возвращает (χ(G), список цветов).
        """
        for k in range(1, self.n + 1):
            coloring = self._color_with_k(k)
            if coloring is not None:
                return k, coloring

        # Теоретически k <= n всегда, до сюда не доходим
        return self.n, [i + 1 for i in range(self.n)]


def print_matrix(matrix: List[List[int]]) -> None:
    """Печатает матрицу в удобном виде."""
    for row in matrix:
        print(" ".join(f"{x:2d}" for x in row))


def main() -> None:
    """
    Главная функция:
    - считывает матрицу весов из файла;
    - преобразует её в матрицу смежности;
    - находит хроматическое число и раскраску;
    - выводит результаты.
    """
    filename = input("Введите имя файла с матрицей весов (смежность по весам): ").strip()

    print("\nШаг 1. Чтение и проверка входных данных")
    try:
        graph = Graph.from_weight_matrix_file(filename)
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Программа завершена из-за некорректных данных.")
        return

    print("Матрица смежности (0/1), полученная из матрицы весов:\n")
    print_matrix(graph.adj)

    print("\nШаг 2. Раскраска графа")
    chromatic, colors = graph.chromatic_number()

    print(f"\nХроматическое число графа: {chromatic}\n")

    print("Вектор цветов (вершина: цвет):")
    for i, c in enumerate(colors, start=1):
        print(f"  v{i}: {c}")


if __name__ == "__main__":
    main()
