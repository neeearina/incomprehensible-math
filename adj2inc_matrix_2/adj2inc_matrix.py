from typing import List, Tuple


class Graph:
    """Класс для работы с графом, заданным матрицей смежности."""

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

        # Проверка, что матрица не пустая
        if not matrix:
            raise ValueError("Файл пуст или не содержит матрицу.")

        # Проверка, что матрица квадратная
        n = len(matrix)
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица должна быть квадратной.")

        # Проверка, что элементы — только 0 или 1
        for row in matrix:
            for x in row:
                if x not in (0, 1):
                    raise ValueError("Матрица должна содержать только 0 и 1.")

        # Проверка отсутствия петель (единиц на диагонали)
        for i in range(n):
            if matrix[i][i] == 1:
                raise ValueError(
                    "Матрица содержит петли (единицы на диагонали). "
                    "В данной версии программы петли не поддерживаются."
                )

        return cls(matrix)

    def edges(self) -> List[Tuple[str, int, int]]:
        """
        Строит список рёбер.
        Возвращает список кортежей (тип, u, v):
        тип: 'undirected' или 'directed', для направленных u -> v.
        """
        edges_list: List[Tuple[str, int, int]] = []

        for i in range(self.n):
            for j in range(self.n):
                if self.adj[i][j] == 1:
                    if i == j:
                        continue
                    if self.adj[j][i] == 1:
                        if j > i:
                            edges_list.append(("undirected", i, j))
                    else:
                        edges_list.append(("directed", i, j))

        return edges_list

    def incidence_matrix(self) -> Tuple[List[List[int]], List[Tuple[str, int, int]]]:
        """
        Строит матрицу инцидентности.
        Возвращает (матрица, список рёбер).
        """
        edges_list = self.edges()
        m = len(edges_list)

        # Матрица n x m, изначально заполнена нулями
        inc = [[0 for _ in range(m)] for _ in range(self.n)]

        for k, (edge_type, u, v) in enumerate(edges_list):
            if edge_type == "undirected":
                # Неориентированное ребро: 1 у обеих вершин
                inc[u][k] = 1
                inc[v][k] = 1
            else:
                # Ориентированное ребро: -1 у начала, +1 у конца
                inc[u][k] = -1
                inc[v][k] = 1

        return inc, edges_list


def print_matrix(matrix: List[List[int]], row_prefix: str = "v") -> None:
    """Печатает матрицу в удобочитаемом виде."""
    if not matrix:
        print("(пустая матрица)")
        return

    for row in matrix:
        print(" ".join(f"{x:3d}" for x in row))


def print_incidence_matrix(matrix: List[List[int]], edges: List[Tuple[str, int, int]]) -> None:
    """Печатает матрицу инцидентности с небольшими пояснениями."""
    if not matrix:
        print("(матрица инцидентности пуста)")
        return

    m = len(edges)

    header = ["   "] + [f"e{k + 1:02d}" for k in range(m)]
    print(" ".join(f"{h:>4s}" for h in header))

    for i, row in enumerate(matrix):
        line = [f"v{i + 1:02d}"] + [f"{x:4d}" for x in row]
        print(" ".join(line))

    print("\nОбозначения рёбер:")
    for k, (edge_type, u, v) in enumerate(edges, start=1):
        if edge_type == "undirected":
            print(f"  e{k:02d}: неориентированное ребро между v{u + 1} и v{v + 1}")
        else:
            print(f"  e{k:02d}: ориентированное ребро v{u + 1} → v{v + 1}")


def main() -> None:
    """Точка входа."""
    filename = input("Введите имя файла с матрицей смежности: ").strip()

    print("\nШаг 1. Чтение и проверка входных данных")
    try:
        graph = Graph.from_file(filename)
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Программа завершена из-за некорректных данных.")
        return

    print("Входная матрица смежности успешно загружена.\n")

    print("Матрица смежности:")
    print_matrix(graph.adj)

    print("\nШаг 2. Построение матрицы инцидентности")
    inc_matrix, edges = graph.incidence_matrix()

    if not edges:
        print("В графе нет рёбер. Матрица инцидентности пуста.")
        return

    print("\nМатрица инцидентности:")
    print_incidence_matrix(inc_matrix, edges)


if __name__ == "__main__":
    main()
