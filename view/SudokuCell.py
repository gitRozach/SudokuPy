from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton
from view import SudokuWindow


class SudokuCell(QPushButton):
    def __init__(self, value: str, is_base_item: bool, parent: SudokuWindow, grid_x: int = 0, grid_y: int = 0):
        super().__init__(value, parent)
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
        self.update_geometry()

    def init_style_sheet(self):
        if self.is_base_item():
            self.setStyleSheet('background-color: rgb(30, 144, 255)')
        else:
            self.setStyleSheet('background-color: rgb(176, 226, 255)')

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
