from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton
from view import SudokuWindow


BASE_CELL_COLOR = 'rgb(30, 144, 255)'
INPUT_CELL_COLOR = 'rgb(176, 226, 255)'
WRONG_CELL_COLOR = 'red'
CORRECT_CELL_COLOR = 'lightgreen'


class SudokuCell(QPushButton):
    def __init__(self, value: str, is_base_item: bool, parent: SudokuWindow, grid_x: int = 0, grid_y: int = 0):
        super().__init__(value)
        self.value = value
        self.base_item = is_base_item
        self.parent = parent
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.set_value(value)
        self.setCheckable(not self.base_item)
        self.setFont(QFont('Arial', parent.get_cell_size() / 3))
        self.clicked.connect(lambda: self.parent.cell_pressed(self.grid_x, self.grid_y))
        self.init_style_sheet()

    def init_style_sheet(self):
        if self.is_base_item():
            self.setStyleSheet('background-color: %s' % BASE_CELL_COLOR)
        else:
            self.setStyleSheet('background-color: %s' % INPUT_CELL_COLOR)

    def get_value(self) -> str:
        return self.value

    def set_value(self, value: str):
        self.value = value
        self.setText(value if self.parent.sudoku_matrix.empty_value != value else '')

    def is_base_item(self) -> bool:
        return self.base_item

    def set_base_item(self, value: bool):
        self.base_item = value
        self.setCheckable(not value)

    def get_grid_x(self) -> int:
        return self.grid_x

    def set_grid_x(self, x: int):
        self.grid_x = x

    def get_grid_y(self) -> int:
        return self.grid_y

    def set_grid_y(self, y: int):
        self.grid_y = y
