import math
from typing import List, Optional, Tuple


INF = math.inf


class WeightedGraph:
    """Класс для работы с графом, заданным матрицей весов."""

    def __init__(self, weight_matrix: List[List[int]]):
        self.w = weight_matrix
        self.n = len(weight_matrix)

    @classmethod
    def from_file(cls, filename: str) -> "WeightedGraph":
        """
        Создаёт граф, читая и проверяя матрицу весов из файла.

        Формат:
        - матрица n x n;
        - 0 на диагонали;
        - 0 вне диагонали означает отсутствие ребра;
        - любое целое число (в т.ч. отрицательное) вне диагонали — вес ребра.
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

        # Проверка: матрица не пустая
        if not matrix:
            raise ValueError("Файл пуст или не содержит матрицу.")

        n = len(matrix)

        # Проверка: квадратная
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица весов должна быть квадратной.")

        # Проверка диагонали
        for i in range(n):
            if matrix[i][i] != 0:
                raise ValueError("Диагональные элементы матрицы должны быть равны 0 (нет петель).")

        # Алгоритм Флойда–Уоршелла допускает отрицательные веса,
        # но не допускает отрицательные циклы — их проверим после алгоритма.
        return cls(matrix)

    def floyd_warshall(self) -> Tuple[List[List[float]], List[List[Optional[int]]]]:
        """
        Реализует алгоритм Флойда–Уоршелла.

        Возвращает:
        - dist[i][j] — длина кратчайшего пути от i до j;
        - nxt[i][j]  — следующая вершина после i на кратчайшем пути к j
                       (None, если пути нет).
        """
        n = self.n
        dist: List[List[float]] = [[INF] * n for _ in range(n)]
        nxt: List[List[Optional[int]]] = [[None] * n for _ in range(n)]

        # Инициализация
        for i in range(n):
            for j in range(n):
                if i == j:
                    dist[i][j] = 0
                elif self.w[i][j] != 0:
                    dist[i][j] = self.w[i][j]
                    nxt[i][j] = j

        # Основной тройной цикл
        for k in range(n):
            for i in range(n):
                if dist[i][k] is INF:
                    continue
                for j in range(n):
                    if dist[k][j] is INF:
                        continue
                    new_dist = dist[i][k] + dist[k][j]
                    if new_dist < dist[i][j]:
                        dist[i][j] = new_dist
                        nxt[i][j] = nxt[i][k]

        # Проверка на наличие отрицательных циклов
        for i in range(n):
            if dist[i][i] < 0:
                raise ValueError(
                    "В графе обнаружен отрицательный цикл. "
                    "Кратчайшие пути не определены."
                )

        return dist, nxt

    def reconstruct_path(
        self,
        nxt: List[List[Optional[int]]],
        start: int,
        end: int
    ) -> List[int]:
        """
        Восстанавливает один кратчайший путь от start до end по матрице nxt.
        Возвращает список индексов вершин (0..n-1). Пустой список, если пути нет.
        """
        if nxt[start][end] is None and start != end:
            return []
        path = [start]
        cur = start
        while cur != end:
            cur = nxt[cur][end]
            if cur is None:  # на всякий случай
                return []
            path.append(cur)
        return path


def print_weight_matrix(matrix: List[List[int]]) -> None:
    """Печатает исходную матрицу весов."""
    for row in matrix:
        print(" ".join(f"{x:4d}" for x in row))


def print_dist_matrix(dist: List[List[float]]) -> None:
    """Печатает матрицу кратчайших расстояний."""
    for row in dist:
        out_row = []
        for x in row:
            if math.isinf(x):
                out_row.append("  ∞ ")
            else:
                out_row.append(f"{int(x):4d}")
        print(" ".join(out_row))


def print_next_matrix(nxt: List[List[Optional[int]]]) -> None:
    """Печатает матрицу 'следующих' вершин."""
    n = len(nxt)
    for i in range(n):
        row_str = []
        for j in range(n):
            if nxt[i][j] is None:
                row_str.append("  - ")
            else:
                # +1, чтобы вершины были 1..n
                row_str.append(f"{nxt[i][j] + 1:4d}")
        print(" ".join(row_str))


def main() -> None:
    """
    Главная функция:
    - считывает матрицу весов из файла;
    - строит матрицу кратчайших расстояний и матрицу путей (Флойд–Уоршелл);
    - запрашивает две вершины и восстанавливает кратчайший путь между ними.
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
    print_weight_matrix(graph.w)

    print("\nШаг 2. Алгоритм Флойда–Уоршелла")
    try:
        dist, nxt = graph.floyd_warshall()
    except Exception as e:
        print(f"Ошибка при выполнении алгоритма: {e}")
        return

    print("\nМатрица длин кратчайших путей:")
    print_dist_matrix(dist)

    print("\nМатрица 'следующих вершин' для кратчайших путей (next[i][j]):")
    print_next_matrix(nxt)

    n = graph.n
    print(f"\nВ графе {n} вершин, нумерация v1..v{n}.")

    print("\nШаг 3. Ввод пары вершин для восстановления пути")
    try:
        s_str = input("Введите номер начальной вершины (1..n): ").strip()
        t_str = input("Введите номер конечной вершины (1..n): ").strip()
        s = int(s_str)
        t = int(t_str)
        if not (1 <= s <= n and 1 <= t <= n):
            raise ValueError
    except ValueError:
        print("Некорректный ввод номеров вершин.")
        print("Программа завершена.")
        return

    start = s - 1
    end = t - 1

    print(f"\nВосстановление кратчайшего пути между v{s} и v{t}:")

    if math.isinf(dist[start][end]):
        print("Между выбранными вершинами нет пути.")
    else:
        path = graph.reconstruct_path(nxt, start, end)
        human_path = " -> ".join(f"v{v+1}" for v in path)
        print(f"Длина кратчайшего пути: {int(dist[start][end])}")
        print(f"Кратчайший путь: {human_path}")


if __name__ == "__main__":
    main()
