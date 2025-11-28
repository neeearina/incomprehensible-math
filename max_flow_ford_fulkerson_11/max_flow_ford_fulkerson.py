from collections import deque
from typing import List, Optional, Tuple


class FlowNetwork:
    """Класс для работы с сетью потоков, заданной матрицей пропускных способностей."""

    def __init__(self, capacity_matrix: List[List[int]]):
        """Сохраняет матрицу пропускных способностей и строит список смежности."""
        self.cap = capacity_matrix
        self.n = len(capacity_matrix)
        self.adj = self._build_adj_list()

    @classmethod
    def from_file(cls, filename: str) -> "FlowNetwork":
        """
        Читает матрицу пропускных способностей из файла и проверяет корректность данных.

        Формат:
        - квадратная матрица n x n;
        - 0 на диагонали (нет петель);
        - 0 вне диагонали — ребра нет;
        - положительное число вне диагонали — пропускная способность ребра.
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

        # Проверка: квадратная матрица
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица должна быть квадратной.")

        # Проверка значений и диагонали
        for i in range(n):
            for j in range(n):
                val = matrix[i][j]
                if val < 0:
                    raise ValueError("Пропускные способности не могут быть отрицательными.")
                if i == j and val != 0:
                    raise ValueError("Диагональные элементы должны быть равны 0 (нет петель).")

        return cls(matrix)

    def _build_adj_list(self) -> List[List[int]]:
        """Строит список смежности по матрице пропускных способностей."""
        adj = [[] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if self.cap[i][j] > 0:
                    adj[i].append(j)
        return adj

    def _bfs_on_residual(
        self,
        residual: List[List[int]],
        s: int,
        t: int
    ) -> Tuple[bool, List[Optional[int]]]:
        """
        Поиск пути из s в t по остаточной сети с помощью BFS.
        Возвращает: (нашёлся_ли_путь, массив_предков).
        """
        parent: List[Optional[int]] = [None] * self.n
        visited = [False] * self.n
        queue = deque([s])
        visited[s] = True

        while queue:
            v = queue.popleft()
            for u in range(self.n):
                if not visited[u] and residual[v][u] > 0:
                    visited[u] = True
                    parent[u] = v
                    if u == t:
                        return True, parent
                    queue.append(u)

        return visited[t], parent

    def max_flow_ford_fulkerson(
        self,
        s: int,
        t: int
    ) -> Tuple[int, List[Tuple[List[int], int]]]:
        """
        Реализует метод Форда–Фалкерсона (через BFS по остаточной сети — вариант Эдмондса–Карпа).

        Возвращает:
        - величину максимального потока,
        - список пар (путь_как_список_вершин, величина_добавленного_потока) для всех найденных путей.
        """
        # Остаточная сеть сначала совпадает с исходной матрицей пропускных способностей
        residual = [row[:] for row in self.cap]
        max_flow = 0
        augmenting_paths: List[Tuple[List[int], int]] = []

        while True:
            found, parent = self._bfs_on_residual(residual, s, t)
            if not found:
                break  # больше нет увеличивающих путей

            # Восстановим путь s -> t по массиву предков
            path: List[int] = []
            v = t
            while v is not None:
                path.append(v)
                if v == s:
                    break
                v = parent[v]
            path.reverse()

            # Найдём минимальную пропускную способность вдоль этого пути (bottleneck)
            bottleneck = float("inf")
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                bottleneck = min(bottleneck, residual[u][v])

            if bottleneck == float("inf"):
                # На всякий случай, но вообще сюда попадать не должны
                break

            # Сохраним путь и его величину
            augmenting_paths.append((path, bottleneck))

            # Увеличим общий поток
            max_flow += bottleneck

            # Обновим остаточную сеть: уменьшаем прямые рёбра, увеличиваем обратные
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                residual[u][v] -= bottleneck
                residual[v][u] += bottleneck  # обратное ребро

        return max_flow, augmenting_paths


def print_matrix(matrix: List[List[int]]) -> None:
    """Печатает матрицу целых чисел."""
    for row in matrix:
        print(" ".join(f"{x:3d}" for x in row))


def print_paths(augmenting_paths: List[Tuple[List[int], int]]) -> None:
    """Печатает все найденные увеличивающие пути и их величины."""
    if not augmenting_paths:
        print("Увеличивающих путей не найдено.")
        return

    print("Найденные пути от источника к стоку в ходе работы алгоритма:")
    for idx, (path, flow) in enumerate(augmenting_paths, start=1):
        human_path = " -> ".join(f"v{v+1}" for v in path)
        print(f"  Путь {idx}: {human_path}, добавленный поток = {flow}")


def main() -> None:
    """
    Главная функция:
    - считывает матрицу пропускных способностей из файла;
    - запрашивает номера истока и стока;
    - выполняет алгоритм Форда–Фалкерсона;
    - выводит все найденные пути и величину максимального потока.
    """
    filename = input("Введите имя файла с матрицей пропускных способностей: ").strip()

    print("\nШаг 1. Чтение и проверка входных данных")
    try:
        network = FlowNetwork.from_file(filename)
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Программа завершена из-за некорректных данных.")
        return

    print("Матрица пропускных способностей успешно загружена.\n")
    print("Исходная матрица пропускных способностей:")
    print_matrix(network.cap)

    n = network.n
    print(f"\nВ сети {n} вершин (нумеруются v1..v{n}).")

    print("\nШаг 2. Ввод истока и стока")
    try:
        s_str = input("Введите номер истока (1..n): ").strip()
        t_str = input("Введите номер стока (1..n): ").strip()
        s = int(s_str)
        t = int(t_str)
        if not (1 <= s <= n and 1 <= t <= n) or s == t:
            raise ValueError
    except ValueError:
        print("Некорректные номера истока/стока (они должны быть в диапазоне 1..n и не совпадать).")
        print("Программа завершена.")
        return

    s_idx = s - 1
    t_idx = t - 1

    print(f"\nИсток: v{s}, сток: v{t}.")

    print("\nШаг 3. Алгоритм Форда–Фалкерсона")
    max_flow, augmenting_paths = network.max_flow_ford_fulkerson(s_idx, t_idx)

    print()
    print_paths(augmenting_paths)

    print(f"\nВеличина максимального потока из v{s} в v{t}: {max_flow}")
    print("\nРабота программы завершена.")


if __name__ == "__main__":
    main()
