import numpy as np


class SudokuMatrix:
    def __init__(self, grid: iter, box_size: int = 3, empty_value: str = '0', input_values: list = None):
        self.grid = np.array([['%s' % i for i in y] for y in grid])
        self.grid_columns = len(grid[0])
        self.grid_rows = len(grid)
        self.box_size = box_size
        self.empty_value = empty_value
        self.input_values = input_values if input_values else ['%i' % i for i in range(1, 10)]
        self.base_positions = self.collect_value_positions()

    def __str__(self) -> str:
        return str(self.grid)

    def __getitem__(self, index) -> str:
        return self.grid[index]

    def __len__(self) -> int:
        return self.grid_rows * self.grid_columns

    def get_item(self, x: int, y: int) -> str:
        return self.grid[y][x]

    def insert(self, x: int, y: int, value: str) -> bool:
        if (x, y) in self.base_positions:
            return False
        self.grid[y][x] = value
        return True

    def replace(self, x: int, y: int, value: str):
        return self.insert(x, y, value)

    def remove(self, x: int, y: int) -> bool:
        return self.insert(x, y, self.empty_value)

    def check_value_at(self, x: int, y: int, value: str, ignore_empty_values: bool = True) -> bool:
        if value not in self.input_values:
            return True if value == self.empty_value and ignore_empty_values else False
        for y1 in range(self.grid_rows):  # Check all vertical values except the current position
            if (x, y1) != (x, y) and str(self.grid[y1][x]) == value:
                return False
        for x1 in range(self.grid_columns):  # Check all horizontal values except the current position
            if (x1, y) != (x, y) and str(self.grid[y][x1]) == value:
                return False
        y0 = int((y // self.box_size) * self.box_size)  # Y-cell index
        x0 = int((x // self.box_size) * self.box_size)  # X-cell index
        for m in range(self.box_size):  # Check current cell except the current position
            for n in range(self.box_size):
                if (x0 + n, y0 + m) != (x, y) and str(self.grid[y0 + m][x0 + n]) == value:
                    return False
        return True

    def check(self, ignore_empty_values: bool = False) -> bool:
        for y in range(self.grid_rows):
            for x in range(self.grid_columns):
                if not self.check_value_at(x, y, str(self.grid[y][x]), ignore_empty_values):
                    return False
        return True

    def is_solved(self):
        return self.check(ignore_empty_values=False)

    def solve(self, max_results: int = -1) -> list:
        results = []
        counter = [max_results]

        def solve_rec():
            if not counter[0]:
                return
            for y in range(self.grid_rows):
                for x in range(self.grid_columns):
                    if self.grid[y][x] == self.empty_value:
                        for n in self.input_values:
                            if self.check_value_at(x, y, n):
                                self.grid[y][x] = n
                                res = solve_rec()
                                if res is not None:
                                    results.append(SudokuMatrix(res.copy()))
                                    counter[0] -= 1
                                self.grid[y][x] = self.empty_value
                        return
            return self.grid
        solve_rec()
        return results

    def collect_value_positions(self) -> tuple:
        not_empty_positions = []
        for y in range(self.grid_rows):
            for x in range(self.grid_columns):
                if str(self.grid[y][x]) in self.input_values:
                    not_empty_positions.append((x, y))
        return tuple(not_empty_positions)

    def grid(self) -> np.array:
        return self.grid

    def get_columns_count(self) -> int:
        return self.grid_columns

    def get_rows_count(self) -> int:
        return self.grid_rows

    def get_box_size(self) -> int:
        return self.box_size

    def get_empty_value(self) -> str:
        return self.empty_value

    def get_input_values(self) -> list:
        return self.input_values

    def get_base_positions(self) -> tuple:
        return self.base_positions
