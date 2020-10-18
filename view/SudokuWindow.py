from PyQt5.QtCore import Qt, QEventLoop, QTimer
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout

from view.SudokuCell import SudokuCell
from SudokuMatrix import SudokuMatrix


class SudokuWindow(QMainWindow):
    def __init__(self, matrix: SudokuMatrix, controller):
        super().__init__()
        self.cell_size = 70
        self.offset_x = 50
        self.offset_y = 50

        self.button_check = QPushButton('Check', self)
        self.button_check.setGeometry(self.offset_x, 0, 60, 30)
        self.button_solve = QPushButton('Solve', self)
        self.button_solve.setGeometry(self.offset_x + 60, 0, 60, 30)
        self.button_hint = QPushButton('Hint', self)
        self.button_hint.setGeometry(self.offset_x + 120, 0, 60, 30)

        self.sudoku = matrix
        self.sudoku_controller = controller
        self.sudoku_cells = []
        for i in range(self.sudoku.get_rows_count()):
            self.sudoku_cells.append([])
        self.selected_cell = None

        self.button_check.clicked.connect(self.sudoku_controller.on_check_button_pressed)
        self.button_solve.clicked.connect(self.sudoku_controller.on_solve_button_pressed)
        self.button_hint.clicked.connect(self.sudoku_controller.on_hint_button_pressed)

        self.sudoku_controls = self.create_sudoku_controls()
        self.sudoku_grid = self.create_sudoku_grid()
        self.root_layout = self.create_root_layout()

        self.window_width = self.sudoku.get_columns_count() * self.cell_size + 2 * self.offset_x
        self.window_height = self.sudoku.get_rows_count() * self.cell_size + 2 * self.offset_y
        self._initialize()

    def _initialize(self):
        self.setStyleSheet('background-color: rgb(176, 226, 255)')
        self.setWindowTitle('SudokuPy')
        self.setFixedSize(self.window_width, self.window_height)
        self.setLayout(self.root_layout)

    @staticmethod
    def _qt_sleep(millis: int):
        loop = QEventLoop()
        QTimer.singleShot(millis, loop.quit)
        loop.exec_()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.sudoku_controller.on_key_pressed(event)

    def create_sudoku_controls(self) -> QHBoxLayout:
        layout = QHBoxLayout(self)
        layout.addWidget(self.button_check)
        layout.addWidget(self.button_solve)
        layout.addWidget(self.button_hint)
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

    def check_sudoku(self):
        if not (solutions := self.sudoku.solve()):
            return
        chosen_solution = solutions[0]
        for y in range(self.sudoku.get_rows_count()):
            for x in range(self.sudoku.get_columns_count()):
                if chosen_solution[y][x] == self.sudoku[y][x]:
                    self.sudoku_cells[y][x].setStyleSheet('background-color: lightgreen')
                else:
                    self.sudoku_cells[y][x].setStyleSheet('background-color: red')
                self._qt_sleep(75)

    def solve_sudoku(self):
        if self.sudoku.is_solved():
            return
        if not (solutions := self.sudoku.solve()):
            return
        chosen_solution = solutions[0]
        self.sudoku = chosen_solution  # Prevents changes during solving process

        for y in range(self.sudoku.get_rows_count()):
            for x in range(self.sudoku.get_columns_count()):
                current_cell = self.sudoku_cells[y][x]
                if current_cell.is_base_item():
                    continue
                current_cell.setCheckable(False)
                current_cell.setStyleSheet('background-color: lightgreen')
                current_cell.setText(chosen_solution[y][x])
                self._qt_sleep(75)

    def get_cell_size(self) -> int:
        return self.cell_size

    def get_offset_x(self) -> int:
        return self.offset_x

    def get_offset_y(self) -> int:
        return self.offset_y