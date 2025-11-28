from typing import List, Tuple, Optional


class WeightedGraph:
    """Класс для работы с неориентированным графом, заданным матрицей весов."""

    def __init__(self, weight_matrix: List[List[int]]):
        self.w = weight_matrix
        self.n = len(weight_matrix)

    @classmethod
    def from_file(cls, filename: str):
        """
        Создаёт граф, читая и проверяя матрицу весов из файла.
        0 вне диагонали — отсутствие ребра, >0 — вес ребра.
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

        if not matrix:
            raise ValueError("Файл пуст или не содержит матрицу.")

        n = len(matrix)

        # Проверка квадратности
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица весов должна быть квадратной.")

        # Проверка значений и диагонали
        for i in range(n):
            for j in range(n):
                val = matrix[i][j]
                if val < 0:
                    raise ValueError("Матрица весов не должна содержать отрицательные числа.")
                if i == j and val != 0:
                    raise ValueError("На диагонали матрицы веса должны быть равны 0 (нет петель).")

        # Проверка симметричности (граф неориентированный)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != matrix[j][i]:
                    raise ValueError("Матрица весов должна быть симметричной (неориентированный граф).")

        return cls(matrix)

    def prim_mst(self) -> Tuple[Optional[List[Tuple[int, int, int]]], Optional[int]]:
        """
        Реализует алгоритм Прима.
        Возвращает (список рёбер остова, суммарный вес) или (None, None), если MST не существует.
        Рёбра задаются кортежем (u, v, w), вершины нумеруются с 0.
        """
        n = self.n
        if n == 0:
            return None, None
        if n == 1:
            # Один узел, пустой остов
            return [], 0

        in_mst = [False] * n  # входит ли вершина в остов
        min_edge = [float('inf')] * n  # минимальный вес ребра до остова
        parent = [-1] * n  # от какой вершины пришли

        # Начнём с вершины 0
        min_edge[0] = 0

        for _ in range(n):
            # Выбираем вершину u, еще не в остове, с минимальным min_edge[u]
            u = -1
            best = float('inf')
            for v in range(n):
                if not in_mst[v] and min_edge[v] < best:
                    best = min_edge[v]
                    u = v

            if u == -1:
                # Остались вершины, до которых нельзя добраться → граф несвязный
                return None, None

            in_mst[u] = True

            # Обновляем веса рёбер до соседних вершин
            for v in range(n):
                w = self.w[u][v]
                if w > 0 and not in_mst[v] and w < min_edge[v]:
                    min_edge[v] = w
                    parent[v] = u

        # Проверим, что все вершины вошли в остов
        if not all(in_mst):
            return None, None

        # Формируем список рёбер
        edges: List[Tuple[int, int, int]] = []
        total_weight = 0
        for v in range(1, n):
            u = parent[v]
            if u == -1:
                # На всякий случай, не должно случиться
                return None, None
            w = self.w[u][v]
            edges.append((u, v, w))
            total_weight += w

        return edges, total_weight


def print_matrix(matrix: List[List[int]]) -> None:
    """Печатает матрицу в удобочитаемом виде."""
    if not matrix:
        print("(пустая матрица)")
        return
    for row in matrix:
        print(" ".join(f"{x:3d}" for x in row))


def main() -> None:
    """
    Главная функция:
    - считывает имя файла с матрицей весов;
    - находит минимальный остов по алгоритму Прима;
    - выводит рёбра остова и сумму их длин,
      либо сообщение, что остов не существует.
    """
    filename = input("Введите имя файла с матрицей весов: ").strip()

    print("\nШаг 1. Чтение и проверка матрицы весов")
    try:
        graph = WeightedGraph.from_file(filename)
    except Exception as e:
        print(f"Ошибка: {e}")
        print("\nНевозможно построить минимальный остов из-за ошибок во входных данных.")
        return

    print("Матрица весов успешно загружена.\n")
    print("Исходная матрица весов:")
    print_matrix(graph.w)

    print("\nШаг 2. Алгоритм Прима: поиск минимального остова")
    edges, total_weight = graph.prim_mst()

    if edges is None:
        print("Граф несвязный. Минимальный покрывающий остов не существует.")
        return

    print("\nМножество рёбер минимального остова:")
    for (u, v, w) in edges:
        # +1, чтобы вывести вершины в привычной нумерации с 1
        print(f"  ({u + 1}, {v + 1}) вес = {w}")

    print(f"\nСуммарная длина (вес) остова: {total_weight}")
    print("\nРабота программы завершена успешно.")


if __name__ == "__main__":
    main()
