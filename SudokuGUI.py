from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout
from SudokuMatrix import SudokuMatrix


class SudokuGUI(QMainWindow):
    def __init__(self, sudoku: SudokuMatrix):
        super().__init__()
        self.cell_size = 70
        self.offset_x = 100
        self.offset_y = 100

        self.sudoku = sudoku
        self.sudoku_solutions = sudoku.solve()

        self.sudoku_cells = [[] for i in range(self.sudoku.get_rows_count())]
        self.selected_cell = None
        self.sudoku_controls = self.create_sudoku_controls()
        self.sudoku_grid = self.create_sudoku_grid()
        self.root_layout = self.create_root_layout()

        self.window_width = self.sudoku.get_columns_count() * self.cell_size + 2 * self.offset_x
        self.window_height = self.sudoku.get_rows_count() * self.cell_size + 2 * self.offset_y
        self.setWindowTitle('SudokuPy')
        self.setFixedSize(self.window_width, self.window_height)
        self.setLayout(self.root_layout)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if self.selected_cell:
            value = event.text()
            if key == Qt.Key_Escape:
                self.selected_cell.setChecked(False)
                self.selected_cell = None
                return
            if value in self.sudoku.get_input_values():
                if self.sudoku.insert(self.selected_cell.get_grid_x(), self.selected_cell.get_grid_y(), value):
                    self.selected_cell.set_value(value)
                self.selected_cell.setChecked(False)
                self.selected_cell = None
                return

    def create_sudoku_controls(self) -> QHBoxLayout:
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        button_solve = QPushButton('Solve', self)
        button_solve.clicked.connect(self.solve_sudoku)
        layout.addWidget(button_solve)
        return layout

    def create_sudoku_grid(self) -> QGridLayout:
        grid = QGridLayout(self)
        grid.setAlignment(Qt.AlignCenter)
        for y in range(self.sudoku.get_rows_count()):
            for x in range(self.sudoku.get_columns_count()):
                item = self.sudoku.get_item(x, y)
                is_base_value = item != self.sudoku.get_empty_value()
                cell = SudokuCell(item, is_base_value, self, x, y)
                grid.addWidget(cell, x, y)
                self.sudoku_cells[y].append(cell)
        return grid

    def cell_pressed(self, x: int, y: int):
        cell = self.sudoku_cells[y][x]
        if not cell.isCheckable() or cell == self.selected_cell:
            return
        if self.selected_cell is not None:
            self.selected_cell.setChecked(False)
        self.selected_cell = cell

    def create_root_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        layout.addItem(self.sudoku_controls)
        layout.addItem(self.sudoku_grid)
        return layout

    def solve_sudoku(self):
        if self.sudoku.is_solved():
            return
        solution_for_current_grid = self.sudoku_solutions[0]
        self.sudoku = solution_for_current_grid
        for y in range(self.sudoku.get_rows_count()):
            for x in range(self.sudoku.get_columns_count()):
                current_cell = self.sudoku_cells[y][x]
                if current_cell.is_base_item():
                    continue
                current_cell.setCheckable(False)
                current_cell.setStyleSheet('background-color: lightgreen')
                current_cell.setText(solution_for_current_grid[y][x])

    def get_cell_size(self) -> int:
        return self.cell_size

    def get_offset_x(self) -> int:
        return self.offset_x

    def get_offset_y(self) -> int:
        return self.offset_y


class SudokuCell(QPushButton):
    def __init__(self, value: str, is_base_item: bool, parent: SudokuGUI, grid_x: int = 0, grid_y: int = 0):
        super().__init__(value, parent)
        self.value = value
        self.base_item = is_base_item
        self.parent = parent
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.set_value(value)
        self.setCheckable(not self.base_item)
        self.setFont(QFont('Tahoma', parent.get_cell_size() / 3))
        self.clicked.connect(lambda: self.parent.cell_pressed(self.grid_x, self.grid_y))
        self.init_style_sheet()
        self.update_geometry()

    def init_style_sheet(self):
        if self.is_base_item():
            self.setStyleSheet('background-color: gray')
        else:
            self.setStyleSheet('background-color: lightgray')

    def update_geometry(self):
        self.setGeometry(self.grid_x * self.parent.get_cell_size() + self.parent.get_offset_x(),
                         self.grid_y * self.parent.get_cell_size() + self.parent.get_offset_y(),
                         self.parent.get_cell_size(), self.parent.get_cell_size())

    def get_value(self) -> str:
        return self.value

    def set_value(self, value: str):
        self.value = value
        self.setText(value if self.parent.sudoku.empty_value != value else '')

    def is_base_item(self) -> bool:
        return self.base_item

    def set_base_item(self, value: bool):
        self.base_item = value
        self.setCheckable(not value)

    def get_grid_x(self) -> int:
        return self.grid_x

    def set_grid_x(self, x: int):
        self.grid_x = x
        self.update_geometry()

    def get_grid_y(self) -> int:
        return self.grid_y

    def set_grid_y(self, y: int):
        self.grid_y = y
        self.update_geometry()
