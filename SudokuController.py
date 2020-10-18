from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

from SudokuMatrix import SudokuMatrix
from view.SudokuWindow import SudokuWindow
from PyQt5.QtWidgets import QApplication
import sys


grid1 = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
         [6, 8, 0, 0, 7, 0, 0, 9, 0],
         [1, 9, 0, 0, 0, 4, 5, 0, 0],
         [8, 2, 0, 1, 0, 0, 0, 4, 0],
         [0, 0, 4, 6, 0, 2, 9, 0, 0],
         [0, 5, 0, 0, 0, 3, 0, 2, 8],
         [0, 0, 9, 3, 0, 0, 0, 7, 4],
         [0, 4, 0, 0, 5, 0, 0, 3, 6],
         [7, 0, 3, 0, 1, 8, 0, 0, 0]]

grid2 = [[9, 0, 6, 0, 7, 0, 4, 0, 3],
         [0, 0, 0, 4, 0, 0, 2, 0, 0],
         [0, 7, 0, 0, 2, 3, 0, 1, 0],
         [5, 0, 0, 0, 0, 0, 1, 0, 0],
         [0, 4, 0, 2, 0, 8, 0, 6, 0],
         [0, 0, 3, 0, 0, 0, 0, 0, 5],
         [0, 3, 0, 7, 0, 0, 0, 5, 0],
         [0, 0, 7, 0, 0, 5, 0, 0, 0],
         [4, 0, 5, 0, 1, 0, 7, 0, 8]]

grid3 = [[8, 4, 3, 5, 6, 7, 2, 1, 9],
         [0, 0, 0, 0, 0, 0, 0, 0, 6],
         [0, 0, 0, 0, 0, 0, 0, 0, 5],
         [3, 8, 4, 6, 7, 2, 0, 0, 1],
         [0, 0, 0, 1, 5, 9, 0, 0, 3],
         [0, 0, 0, 8, 3, 4, 0, 0, 7],
         [0, 0, 0, 0, 0, 0, 0, 0, 4],
         [0, 0, 0, 0, 0, 0, 0, 0, 8],
         [1, 9, 8, 3, 4, 5, 7, 6, 2]]

grid4 = [['E', -1, -1, 6, 4, 'D', -1, 5, -1, 8, -1, -1, -1, 'C', -1, 7],
         [-1, 7, 5, 4, -1, -1, 'C', 'F', 'A', 'E', -1, -1, -1, 0, -1, -1],
         [-1, -1, -1, 3, -1, -1, 0, 'A', -1, 'F', -1, -1, 4, -1, -1, -1],
         [-1, 'A', -1, -1, -1, -1, -1, 8, -1, 0, -1, 6, -1, -1, 2, -1],
         [-1, -1, -1, -1, 'A', -1, -1, -1, -1, -1, 7, -1, -1, 'F', -1, -1],
         [-1, -1, 1, -1, -1, 0, -1, -1, 4, 6, -1, -1, 'A', -1, -1, -1],
         [-1, 3, 9, 'A', -1, 1, -1, -1, 'E', 'B', -1, -1, 5, -1, 0, 4],
         ['D', 'C', 2, -1, -1, 4, -1, 6, -1, -1, -1, 3, -1, -1, -1, -1],
         ['C', -1, -1, -1, -1, 'A', -1, 4, -1, -1, -1, 9, -1, -1, 8, 'B'],
         [-1, -1, 8, -1, -1, 'B', -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
         ['A', 'E', -1, -1, 3, 2, -1, -1, -1, 7, 8, -1, -1, 5, -1, -1],
         [-1, -1, -1, -1, -1, -1, -1, 0, -1, 4, 6, -1, -1, 'D', -1, -1],
         [-1, -1, 0, -1, 9, -1, 'D', -1, -1, -1, -1, -1, -1, -1, 'B', -1],
         [5, 2, -1, 'E', 1, -1, 6, -1, -1, -1, -1, 4, -1, 3, -1, 'C'],
         [-1, -1, -1, -1, -1, 8, -1, 7, -1, 'C', 9, -1, -1, -1, -1, 'D'],
         [6, 'B', 7, -1, 'E', -1, -1, -1, 2, 'D', 3, -1, 'F', -1, -1, -1]]


class SudokuController:
    def __init__(self):
        self.sudoku_matrix = SudokuMatrix(grid2)
        self.sudoku_window = SudokuWindow(self.sudoku_matrix, self)

    def on_key_pressed(self, key_event: QKeyEvent):
        key = key_event.key()
        if self.sudoku_window.selected_cell:
            value = key_event.text()
            if key == Qt.Key_Escape:
                self.sudoku_window.selected_cell.setChecked(False)
                self.sudoku_window.selected_cell = None
                return
            if value in self.sudoku_matrix.get_input_values():
                grid_x = self.sudoku_window.selected_cell.get_grid_x()
                grid_y = self.sudoku_window.selected_cell.get_grid_y()
                if self.sudoku_matrix.insert(grid_x, grid_y, value):
                    self.sudoku_window.selected_cell.set_value(value)
                for c_x, c_y in self.sudoku_matrix.get_collisions_at(grid_x, grid_y):
                    self.sudoku_window.sudoku_cells[c_y][c_x].setStyleSheet('background-color: red')
                self.sudoku_window.selected_cell.setChecked(False)
                self.sudoku_window.selected_cell = None
                return

    def on_check_button_pressed(self):
        self.sudoku_window.check_sudoku()

    def on_solve_button_pressed(self):
        self.sudoku_window.solve_sudoku()

    def on_hint_button_pressed(self):
        self.sudoku_window.check_sudoku()

    def get_matrix(self) -> SudokuMatrix:
        return self.sudoku_matrix

    def get_window(self) -> SudokuWindow:
        return self.sudoku_window


def main():
    app = QApplication(sys.argv)
    controller = SudokuController()
    controller.get_window().show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
