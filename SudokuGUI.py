from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout
from SudokuMatrix import SudokuMatrix


class SudokuGUI(QMainWindow):
    def __init__(self, sudoku: SudokuMatrix):
        super().__init__()
        self.sudoku = sudoku
        self.sudoku_solutions = sudoku.solve()

        self.sudoku_cells = [[] for i in range(self.sudoku.get_rows_count())]
        self.selected_cell = None
        self.sudoku_controls = self.create_sudoku_controls()
        self.sudoku_grid = self.create_sudoku_grid()
        self.root_layout = self.create_root_layout()

        self.setWindowTitle('SudokuPy')
        self.setGeometry(460, 100, 1000, 800)
        self.setLayout(self.root_layout)

    def create_sudoku_controls(self) -> QHBoxLayout:
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        button_solve = QPushButton('Solve', self)
        button_solve.clicked.connect(lambda: print('xd'))

        layout.addWidget(button_solve)
        return layout

    def create_sudoku_grid(self) -> QGridLayout:
        cell_size = 60
        offset_x = 100
        offset_y = 100

        grid = QGridLayout(self)
        grid.setAlignment(Qt.AlignCenter)
        for y in range(self.sudoku.get_rows_count()):
            for x in range(self.sudoku.get_columns_count()):
                item = self.sudoku.get_item(x, y)
                is_base_item = item != self.sudoku.get_empty_value()
                button = QPushButton(item if is_base_item else '', self)
                button.clicked.connect(lambda: self.cell_pressed(button))
                button.setCheckable(not is_base_item)
                button.setGeometry(x * cell_size + offset_x, y * cell_size + offset_y, cell_size, cell_size)
                grid.addWidget(button, x, y)
                self.sudoku_cells[y].append(button)
        print(len(self.sudoku_cells[0]))
        return grid

    def cell_pressed(self, cell):
        if self.selected_cell is not None:
            self.selected_cell.setChecked(False)
        self.selected_cell = cell
        # print('= None')
        # self.selected_cell = None

    def create_root_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        layout.addItem(self.sudoku_controls)
        layout.addItem(self.sudoku_grid)
        return layout

    def solve_sudoku(self):
        for y in range(self.sudoku.get_rows_count()):
            for x in range(self.sudoku.get_columns_count()):
                self.sudoku_grid.get
