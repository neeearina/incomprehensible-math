from typing import List, Optional, Tuple
import itertools


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
                        raise ValueError(
                            f"Файл '{filename}': матрица содержит нечисловые значения."
                        )
                    matrix.append(row)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{filename}' не найден.")

        # Проверка: матрица не пустая
        if not matrix:
            raise ValueError(f"Файл '{filename}' пуст или не содержит матрицу.")

        # Проверка: квадратная матрица
        n = len(matrix)
        if any(len(row) != n for row in matrix):
            raise ValueError(
                f"Файл '{filename}': матрица смежности должна быть квадратной."
            )

        # Проверка: элементы только 0 или 1
        for row in matrix:
            for x in row:
                if x not in (0, 1):
                    raise ValueError(
                        f"Файл '{filename}': матрица смежности должна содержать только 0 и 1."
                    )

        # Проверка отсутствия петель (простые графы)
        for i in range(n):
            if matrix[i][i] != 0:
                raise ValueError(
                    f"Файл '{filename}': матрица содержит петли (единицы на диагонали)."
                )

        return cls(matrix)

    def degree_sequence(self) -> List[int]:
        """Возвращает список степеней вершин."""
        return [sum(row) for row in self.adj]

    def is_isomorphic_to(self, other: "Graph") -> Tuple[bool, Optional[List[int]]]:
        """
        Проверяет, изоморфен ли данный граф графу other.
        Возвращает (True, перестановка) или (False, None).
        Перестановка p такая, что вершина i этого графа соответствует вершине p[i] другого.
        """
        # 1. Размеры должны совпадать
        if self.n != other.n:
            return False, None

        n = self.n

        # 2. Степенные последовательности должны совпадать (как мультимножества)
        deg_self = self.degree_sequence()
        deg_other = other.degree_sequence()
        if sorted(deg_self) != sorted(deg_other):
            return False, None

        # 3. Полный перебор перестановок вершин (подходит для небольших графов)
        vertices = list(range(n))

        for perm in itertools.permutations(vertices):
            # Быстрая проверка: степени должны совпадать по соответствию
            ok_degrees = True
            for i in range(n):
                if deg_self[i] != deg_other[perm[i]]:
                    ok_degrees = False
                    break
            if not ok_degrees:
                continue

            # Проверка соответствия матриц смежности
            is_iso = True
            for i in range(n):
                for j in range(n):
                    if self.adj[i][j] != other.adj[perm[i]][perm[j]]:
                        is_iso = False
                        break
                if not is_iso:
                    break

            if is_iso:
                return True, list(perm)

        return False, None


def print_matrix(matrix: List[List[int]], title: str = "") -> None:
    """Печатает матрицу с необязательным заголовком."""
    if title:
        print(title)
    if not matrix:
        print("(пустая матрица)")
        return
    for row in matrix:
        print(" ".join(f"{x:2d}" for x in row))
    print()


def print_isomorphism_mapping(mapping: List[int]) -> None:
    """Печатает соответствие вершин двух графов по найденному изоморфизму."""
    print("Найдено соответствие вершин (биекция):")
    for i, j in enumerate(mapping):
        print(f"  вершина G1: v{i + 1}  →  вершина G2: v{j + 1}")


def main() -> None:
    """Главная функция: чтение двух файлов, вывод и проверка изоморфизма."""
    filename1 = input("Введите имя файла с матрицей смежности первого графа: ").strip()
    filename2 = input("Введите имя файла с матрицей смежности второго графа: ").strip()

    print("\nШаг 1. Чтение и проверка входных данных ===")
    try:
        g1 = Graph.from_file(filename1)
        g2 = Graph.from_file(filename2)
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Программа завершена из-за некорректных данных.")
        return

    print("Обе матрицы успешно загружены и проверены.\n")

    print_matrix(g1.adj, "Матрица смежности первого графа (G1):")
    print_matrix(g2.adj, "Матрица смежности второго графа (G2):")

    print("Шаг 2. Проверка графов на изоморфизм ===")
    are_iso, mapping = g1.is_isomorphic_to(g2)

    if are_iso:
        print("\nРезультат: графы ИЗОМОРФНЫ.")
        if mapping is not None:
            print()
            print_isomorphism_mapping(mapping)
    else:
        print("\nРезультат: графы НЕ изоморфны.")


if __name__ == "__main__":
    main()
