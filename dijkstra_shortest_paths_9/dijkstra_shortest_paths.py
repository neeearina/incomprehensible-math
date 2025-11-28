import math
import heapq
from typing import List, Tuple, Optional


class WeightedGraph:
    """Класс для работы с графом, заданным матрицей весов."""

    def __init__(self, weight_matrix: List[List[int]]):
        """Сохраняет матрицу весов и строит список смежности."""
        self.w = weight_matrix
        self.n = len(weight_matrix)
        self.adj_list = self._build_adjacency_list()

    @classmethod
    def from_file(cls, filename: str) -> "WeightedGraph":
        """Создаёт граф, читая и проверяя матрицу весов из файла."""
        matrix: List[List[int]] = []

        # Чтение матрицы из файла
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

        # Проверка, что матрица не пустая
        if not matrix:
            raise ValueError("Файл пуст или не содержит матрицу.")

        n = len(matrix)

        # Проверка, что матрица квадратная
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица весов должна быть квадратной.")

        # Проверка значений
        for i in range(n):
            for j in range(n):
                val = matrix[i][j]
                if val < 0:
                    raise ValueError("Алгоритм Дейкстры не работает с отрицательными весами.")
                if i == j and val != 0:
                    raise ValueError("Матрица содержит петли (ненулевая диагональ).")

        # Не требуем симметричности — граф может быть ориентированным
        return cls(matrix)

    def _build_adjacency_list(self) -> List[List[Tuple[int, int]]]:
        """Строит список смежности (с весами) из матрицы весов."""
        adj: List[List[Tuple[int, int]]] = [[] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if self.w[i][j] > 0:
                    adj[i].append((j, self.w[i][j]))
        return adj

    def dijkstra(self, start: int) -> Tuple[List[float], List[Optional[int]]]:
        """
        Реализует алгоритм Дейкстры.
        Возвращает (список расстояний, список предков).
        """
        dist = [math.inf] * self.n
        prev: List[Optional[int]] = [None] * self.n
        dist[start] = 0

        # Очередь с приоритетом: (расстояние, вершина)
        heap: List[Tuple[float, int]] = [(0, start)]

        while heap:
            cur_dist, v = heapq.heappop(heap)

            if cur_dist > dist[v]:
                continue  # устаревшая запись

            for u, weight in self.adj_list[v]:
                new_dist = dist[v] + weight
                if new_dist < dist[u]:
                    dist[u] = new_dist
                    prev[u] = v
                    heapq.heappush(heap, (new_dist, u))

        return dist, prev

    def reconstruct_path(self, prev: List[Optional[int]], start: int, end: int) -> List[int]:
        """Восстанавливает путь от start до end по массиву предков."""
        path: List[int] = []
        cur = end
        while cur is not None:
            path.append(cur)
            if cur == start:
                break
            cur = prev[cur]

        path.reverse()
        if not path or path[0] != start:
            return []  # пути нет
        return path


def print_matrix(matrix: List[List[int]]) -> None:
    """Печатает матрицу в удобном виде."""
    for row in matrix:
        print(" ".join(f"{x:3d}" for x in row))


def print_distances(dist: List[float], start: int) -> None:
    """Печатает вектор длин кратчайших путей."""
    print(f"Вектор длин кратчайших путей от вершины v{start + 1}:")
    for i, d in enumerate(dist):
        if math.isinf(d):
            print(f"  до v{i + 1}: недостижима")
        else:
            print(f"  до v{i + 1}: {d}")


def print_paths_for_all(prev: List[Optional[int]], start: int) -> None:
    """Печатает кратчайшие пути от start до всех вершин."""
    print(f"\nВектор кратчайших путей от вершины v{start + 1}:")
    n = len(prev)
    for end in range(n):
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            if cur == start:
                break
            cur = prev[cur]
        path.reverse()
        if not path or path[0] != start:
            print(f"  до v{end + 1}: пути нет")
        else:
            human_path = " -> ".join(f"v{x + 1}" for x in path)
            print(f"  до v{end + 1}: {human_path}")


def main() -> None:
    """
    Главная функция:
    - считывает матрицу весов из файла;
    - запрашивает пару вершин (источник и цель);
    - выполняет алгоритм Дейкстры;
    - выводит вектор расстояний и вектор кратчайших путей,
      а также отдельно путь между указанной парой.
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

    n = graph.n
    print(f"\nВ графе {n} вершин (нумерация: v1 .. v{n}).")

    print("\nШаг 2. Ввод пары вершин")
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

    print(f"\nНачальная вершина: v{s}, конечная вершина: v{t}.")

    print("\nШаг 3. Алгоритм Дейкстры")
    dist, prev = graph.dijkstra(start)

    print("\nРезультаты алгоритма Дейкстры:")
    print_distances(dist, start)
    print_paths_for_all(prev, start)

    print(f"\nШаг 4. Кратчайший путь между v{s} и v{t}")
    path = graph.reconstruct_path(prev, start, end)
    if not path or math.isinf(dist[end]):
        print(f"Между v{s} и v{t} нет пути.")
    else:
        human_path = " -> ".join(f"v{x + 1}" for x in path)
        print(f"Длина кратчайшего пути: {dist[end]}")
        print(f"Кратчайший путь: {human_path}")


if __name__ == "__main__":
    main()
