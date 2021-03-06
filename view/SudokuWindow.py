from PyQt5.QtCore import Qt, QEventLoop, QTimer
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from view.widgets.SudokuCell import SudokuCell, BASE_CELL_COLOR, INPUT_CELL_COLOR, WRONG_CELL_COLOR
from SudokuMatrix import SudokuMatrix
from view.widgets.SudokuCellBox import SudokuCellBox


class SudokuWindow(QMainWindow):
    def __init__(self, matrix: SudokuMatrix, controller):
        super().__init__()
        self.sudoku_matrix = matrix
        self.sudoku_controller = controller
        self.cell_size = 80
        self.selected_cell = None
        self.cells = {}
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

    def update_cells(self, collision_positions: iter = ()):
        for y in range(self.sudoku_matrix.get_rows_count()):
            for x in range(self.sudoku_matrix.get_columns_count()):
                current_cell = self.get_cell(x, y)
                if current_cell == self.sudoku_matrix.get_empty_value():
                    current_cell.set_color(INPUT_CELL_COLOR)
                elif (x, y) in collision_positions:
                    current_cell.set_color(WRONG_CELL_COLOR)
                elif current_cell.is_base_item():
                    current_cell.set_color(BASE_CELL_COLOR)
                else:
                    current_cell.set_color(INPUT_CELL_COLOR)

    def _init_window(self, style_sheet_path: str = 'view/stylesheets/style_default.css'):
        self.setWindowTitle('SudokuPy')
        try:
            with open(style_sheet_path) as stylesheet_file:
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
        grid.setSpacing(10)
        grid.setAlignment(Qt.AlignCenter)
        box_size = self.sudoku_matrix.get_box_size()

        for g_y in range(box_size):
            for g_x in range(box_size):
                box = SudokuCellBox(width=box_size, height=box_size)
                for c_y in range(self.sudoku_matrix.get_box_size()):
                    for c_x in range(self.sudoku_matrix.get_box_size()):
                        item = self.sudoku_matrix.get_item(g_x * box_size + c_x, g_y * box_size + c_y)
                        is_base_value = item != self.sudoku_matrix.get_empty_value()
                        cell = SudokuCell(item, is_base_value, self, g_x * box_size + c_x, g_y * box_size + c_y)
                        cell.setFixedSize(self.cell_size, self.cell_size)
                        box.get_grid().addWidget(cell, c_y, c_x)
                        self.cells[(g_x * box_size + c_x, g_y * box_size + c_y)] = cell
                grid.addWidget(box, g_y, g_x)
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
        self.sudoku_controller.on_cell_pressed(x, y)

    def get_cell(self, x: int, y: int):
        return self.cells.get((x, y))

    def get_cell_size(self) -> int:
        return self.cell_size

    def get_selected_cell(self):
        return self.selected_cell

    def set_selected_cell(self, x: int, y: int):
        if self.selected_cell:
            self.selected_cell.setChecked(False)
        self.selected_cell = self.get_cell(x, y)
        self.selected_cell.setChecked(True)

    def unselect_current_cell(self):
        if not self.selected_cell:
            return
        self.selected_cell.setChecked(False)
        self.selected_cell = None

    def get_matrix(self):
        return self.sudoku_matrix
