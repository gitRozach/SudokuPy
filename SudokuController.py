from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtCore import Qt

from SudokuMatrix import SudokuMatrix
from view.SudokuWindow import SudokuWindow
from PyQt5.QtWidgets import QApplication, QStyle
import sys

from view.widgets.SudokuCell import CORRECT_CELL_COLOR, WRONG_CELL_COLOR, BASE_CELL_COLOR

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


class SudokuController:
    def __init__(self):
        self.matrix = SudokuMatrix(grid1)
        self.window = SudokuWindow(self.matrix, self)

    def on_key_pressed(self, key_event: QKeyEvent):
        key = key_event.key()
        if c := self.window.get_selected_cell():
            value = key_event.text()
            if key == Qt.Key_Escape:
                self.window.unselect_current_cell()
            elif key == Qt.Key_Delete or value in self.matrix.get_input_values():
                delete = key == Qt.Key_Delete
                empty_val = self.matrix.get_empty_value()
                collisions = self.matrix.insert(c.get_grid_x(), c.get_grid_y(), empty_val if delete else value)
                c.set_value('0' if delete else value)
                self.window.unselect_current_cell()
                self.window.update_cells(collision_positions=collisions)
            elif key == Qt.Key_W:
                next_item = self.matrix.get_next_input_for(c.get_grid_x(), c.get_grid_y())
                collisions = self.matrix.insert(c.get_grid_x(), c.get_grid_y(), next_item)
                c.set_value(next_item)
                self.window.update_cells(collision_positions=collisions)
            elif key == Qt.Key_S:
                previous_item = self.matrix.get_previous_input_for(c.get_grid_x(), c.get_grid_y())
                collisions = self.matrix.insert(c.get_grid_x(), c.get_grid_y(), previous_item)
                c.set_value(previous_item)
                self.window.update_cells(collision_positions=collisions)

    def on_mouse_event(self, mouse_event: QMouseEvent):
        key = mouse_event.button()
        if c := self.window.get_selected_cell():
            pass

    def on_check_button_pressed(self):
        if self.matrix.is_solved():
            return
        # TODO Choose a solution according to the current input
        chosen_solution = self.matrix.get_solutions()[0]
        self.window.unselect_current_cell()
        for y in range(self.matrix.get_rows_count()):
            for x in range(self.matrix.get_columns_count()):
                correct_input = chosen_solution[y][x] == self.matrix[y][x]
                self.window.get_cell(x, y).set_color(CORRECT_CELL_COLOR if correct_input else WRONG_CELL_COLOR)
                self.window.qt_sleep(20)

    def on_solve_button_pressed(self):
        if self.matrix.is_solved():
            return
        # TODO Choose a solution according to the current input
        chosen_solution = self.matrix.get_solutions()[0]
        self.matrix = chosen_solution  # Prevents changes during solving process
        self.window.unselect_current_cell()

        for y in range(self.matrix.get_rows_count()):
            for x in range(self.matrix.get_columns_count()):
                current_cell = self.window.get_cell(x, y)
                if current_cell.is_base_item():
                    current_cell.set_color(BASE_CELL_COLOR)
                    continue
                current_cell.setCheckable(False)
                current_cell.set_color(CORRECT_CELL_COLOR)
                current_cell.setText(chosen_solution[y][x])
                self.window.qt_sleep(15)

    def on_hint_button_pressed(self):
        # TODO
        pass

    def on_cell_pressed(self, x: int, y: int):
        cell = self.window.get_cell(x, y)
        if not cell.isCheckable() or cell == self.window.get_selected_cell():
            return
        self.window.set_selected_cell(x, y)

    def get_matrix(self) -> SudokuMatrix:
        return self.matrix

    def get_window(self) -> SudokuWindow:
        return self.window


def main():
    app = QApplication(sys.argv)
    controller = SudokuController()
    controller.get_window().show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
