from typing import List, Tuple


class IncidenceGraph:
    """Класс для работы с графом, заданным матрицей инцидентности."""

    def __init__(self, incidence_matrix: List[List[int]]):
        self.inc = incidence_matrix
        self.n = len(incidence_matrix)  # число вершин
        self.m = len(incidence_matrix[0])  # число рёбер

    @classmethod
    def from_file(cls, filename: str):
        """Создаёт граф, читая и проверяя матрицу инцидентности из файла."""
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

        # Проверки
        if not matrix:
            raise ValueError("Файл пуст или не содержит матрицу.")

        num_cols = len(matrix[0])
        if any(len(row) != num_cols for row in matrix):
            raise ValueError("Все строки матрицы должны иметь одинаковое количество столбцов.")

        for row in matrix:
            for x in row:
                if x not in (-1, 0, 1):
                    raise ValueError("Матрица инцидентности должна содержать только значения -1, 0, 1.")

        n = len(matrix)
        m = num_cols
        for e in range(m):
            col = [matrix[v][e] for v in range(n)]
            num_pos = sum(1 for v in col if v == 1)
            num_neg = sum(1 for v in col if v == -1)

            # Возможные варианты:
            # 1) неориентированное ребро: ровно две вершины с +1, ни одной с -1
            # 2) ориентированное ребро: одна вершина с -1, одна с +1
            if (num_pos == 2 and num_neg == 0) or (num_pos == 1 and num_neg == 1):
                continue
            else:
                raise ValueError(
                    "Столбец матрицы инцидентности не соответствует ни ориентированному, "
                    "ни неориентированному ребру. Проверьте данные."
                )

        return cls(matrix)

    def edges(self) -> List[Tuple[str, int, int]]:
        """
        Возвращает список рёбер.
        Каждый элемент: (тип, u, v),
        тип: 'undirected' или 'directed', для ориентированных u -> v.
        """
        edges_list: List[Tuple[str, int, int]] = []

        for e in range(self.m):
            col = [self.inc[v][e] for v in range(self.n)]
            vertices_pos = [i for i, val in enumerate(col) if val == 1]
            vertices_neg = [i for i, val in enumerate(col) if val == -1]

            if len(vertices_pos) == 2 and len(vertices_neg) == 0:
                # Неориентированное ребро
                u, v = vertices_pos
                edges_list.append(("undirected", u, v))
            elif len(vertices_pos) == 1 and len(vertices_neg) == 1:
                # Ориентированное ребро: от -1 к +1
                u = vertices_neg[0]
                v = vertices_pos[0]
                edges_list.append(("directed", u, v))
            else:
                # Сюда не должны попасть, т.к. мы проверили в from_file
                raise ValueError("Обнаружен некорректный столбец матрицы инцидентности.")

        return edges_list

    def to_adjacency_matrix(self) -> List[List[int]]:
        """Строит и возвращает матрицу смежности по матрице инцидентности."""
        # Изначально матрица смежности из нулей
        adj = [[0 for _ in range(self.n)] for _ in range(self.n)]

        for edge_type, u, v in self.edges():
            if edge_type == "undirected":
                adj[u][v] = 1
                adj[v][u] = 1
            else:  # directed
                adj[u][v] = 1

        return adj


def print_matrix(matrix: List[List[int]]) -> None:
    """Печатает матрицу в удобном виде."""
    if not matrix:
        print("(пустая матрица)")
        return
    for row in matrix:
        print(" ".join(f"{x:3d}" for x in row))


def print_edges(edges: List[Tuple[str, int, int]]) -> None:
    """Печатает список рёбер с указанием типа."""
    if not edges:
        print("Рёбра отсутствуют.")
        return

    for idx, (edge_type, u, v) in enumerate(edges, start=1):
        if edge_type == "undirected":
            print(f"  e{idx:02d}: неориентированное ребро между v{u + 1} и v{v + 1}")
        else:
            print(f"  e{idx:02d}: ориентированное ребро v{u + 1} → v{v + 1}")


def main() -> None:
    """Главная функция: ввод имени файла, вывод исходных и результирующих данных."""
    filename = input("Введите имя файла с матрицей инцидентности: ").strip()

    print("\nШаг 1. Чтение и проверка матрицы инцидентности")
    try:
        graph = IncidenceGraph.from_file(filename)
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Программа завершена из-за некорректных данных.")
        return

    print("Матрица инцидентности успешно загружена.\n")
    print("Исходная матрица инцидентности:")
    print_matrix(graph.inc)

    print("\nШаг 2. Определение рёбер графа")
    edges = graph.edges()
    print_edges(edges)

    print("\nШаг 3. Построение матрицы смежности")
    adjacency = graph.to_adjacency_matrix()

    print("\nПолученная матрица смежности:")
    print_matrix(adjacency)


if __name__ == "__main__":
    main()
