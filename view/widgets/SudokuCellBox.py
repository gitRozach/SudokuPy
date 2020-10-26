from PyQt5.QtWidgets import QWidget, QGridLayout


class SudokuCellBox(QWidget):
    def __init__(self, width: int, height: int, parent=None):
        super().__init__(parent=parent)
        self._box_width = width
        self._box_height = height
        self._grid = QGridLayout(self)
        self._grid.setSpacing(3)
        self.setLayout(self._grid)

    def get_box_width(self):
        return self._box_width

    def get_box_height(self):
        return self._box_height

    def get_grid(self):
        return self._grid
