from PyQt5.QtCore import Qt, QEventLoop, QTimer
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from view.SudokuCell import SudokuCell
from SudokuMatrix import SudokuMatrix


class SudokuWindow(QMainWindow):
    def __init__(self, matrix: SudokuMatrix, controller):
        super().__init__()
        self.cell_size = 100
        self.selected_cell = None

        self.sudoku_matrix = matrix
        self.sudoku_controller = controller
        self.sudoku_cells = []
        # Placeholder Root Widget
        self.root = QWidget()
        self.setCentralWidget(self.root)
        # Init Controls
        self.button_check = QPushButton('Check')
        self.button_solve = QPushButton('Solve')
        self.button_hint = QPushButton('Hint')
        # Init Layouts
        self.sudoku_controls = self.create_controls_layout()
        self.sudoku_grid = self.create_grid_layout()
        self.root_layout = self.create_root_layout()
        # Init QMainWindow properties and button slots
        self._init_window()
        self._init_button_slots()

    def _init_window(self):
        self.setWindowTitle('SudokuPy')
        try:
            with open('view/Stylesheet_Default.css') as stylesheet_file:
                stylesheet_str = stylesheet_file.read()
                self.setStyleSheet(stylesheet_str)
        except FileNotFoundError:
            pass

    def _init_button_slots(self):
        self.button_check.clicked.connect(self.sudoku_controller.on_check_button_pressed)
        self.button_solve.clicked.connect(self.sudoku_controller.on_solve_button_pressed)
        self.button_hint.clicked.connect(self.sudoku_controller.on_hint_button_pressed)

    def create_controls_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.button_check)
        layout.addWidget(self.button_solve)
        layout.addWidget(self.button_hint)
        return layout

    def create_grid_layout(self) -> QGridLayout:
        grid = QGridLayout()
        grid.setSpacing(1)
        grid.setAlignment(Qt.AlignCenter)
        for y in range(self.sudoku_matrix.get_rows_count()):
            for x in range(self.sudoku_matrix.get_columns_count()):
                item = self.sudoku_matrix.get_item(x, y)
                is_base_value = item != self.sudoku_matrix.get_empty_value()
                cell = SudokuCell(item, is_base_value, self, x, y)
                cell.setFixedSize(self.cell_size, self.cell_size)
                grid.addWidget(cell, y, x)
                self.sudoku_cells.append(cell)
        return grid

    def create_root_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout(self.root)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.addLayout(self.sudoku_controls)
        layout.addLayout(self.sudoku_grid)
        return layout

    @staticmethod
    def qt_sleep(millis: int):
        loop = QEventLoop()
        QTimer.singleShot(millis, loop.quit)
        loop.exec_()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.sudoku_controller.on_key_pressed(event)

    def cell_pressed(self, x: int, y: int):
        cell = self.sudoku_cells[y][x]
        if not cell.isCheckable() or cell == self.selected_cell:
            return
        if self.selected_cell is not None:
            self.selected_cell.setChecked(False)
        self.selected_cell = cell

    def get_cell(self, x: int, y: int):
        return self.sudoku_cells[y * self.sudoku_matrix.get_columns_count() + x]

    def get_cell_size(self) -> int:
        return self.cell_size
