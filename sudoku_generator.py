import random

from sudoku_puzzle import *


class SudokuGenerator:
    def __init__(self, dimension, mode, empty_cells, possible_values) -> None:
        self.dimension = dimension
        self.sub_dimension = int(math.sqrt(dimension))
        self.mode = mode
        self.empty_cells = empty_cells
        self.possible_values = possible_values.copy()
        self.grid = []

        row = ['0' for i in range(dimension)]
        for i in range(dimension):
            self.grid.append(row.copy())

    def __check_symbol_in_square(self, upper_left_corner_row, upper_left_corner_col, symbol) -> bool:
        for i in range(self.sub_dimension):
            for j in range(self.sub_dimension):
                if self.grid[upper_left_corner_row + i][upper_left_corner_col + j] == symbol:
                    return False

        return True

    def __fill_square(self, upper_left_corner_row, upper_left_corner_col) -> None:
        symbol = random.choice(self.possible_values)

        for i in range(self.sub_dimension):
            for j in range(self.sub_dimension):
                while self.__check_symbol_in_square(upper_left_corner_row, upper_left_corner_col, symbol) is False:
                    symbol = random.choice(self.possible_values)

                self.grid[upper_left_corner_row + i][upper_left_corner_col + j] = symbol

    def __fill_board_main_diagonal_squares(self) -> None:
        for i in range(0, self.dimension, self.sub_dimension):
            self.__fill_square(i, i)

    def __get_board_main_diagonal_values(self) -> list:
        diagonal_values = []
        for i in range(self.dimension):
            diagonal_values.append(self.grid[i][i])

        return diagonal_values

    def __create_empty_cells(self):
        while self.empty_cells != 0:
            index_of_grid_cell = random.choice(range(self.dimension * self.dimension))

            row = int(index_of_grid_cell / self.dimension)
            col = index_of_grid_cell % self.dimension

            if self.grid[row][col] != '0':
                self.grid[row][col] = '0'
                self.empty_cells -= 1

    def generate(self) -> tuple:
        if self.mode == 'Diagonal Sudoku':
            while len(set(self.__get_board_main_diagonal_values())) != self.dimension:
                self.grid = []

                row = ['0' for i in range(self.dimension)]
                for i in range(self.dimension):
                    self.grid.append(row.copy())

                self.__fill_board_main_diagonal_squares()
        else:
            self.__fill_board_main_diagonal_squares()

        if self.mode == 'Odd-Even Sudoku':
            self.grid = SudokuPuzzle.solve_puzzle(self.grid, 'Sudoku')
        else:
            self.grid = SudokuPuzzle.solve_puzzle(self.grid, self.mode)

        args = {}
        if self.mode == 'Odd-Even Sudoku':
            even_positions = []

            for i in range(self.dimension):
                for j in range(self.dimension):
                    if COORDINATES_DICT[self.grid[i][j]] % 2 == 0:
                        even_positions.append((i, j))

            args['even_positions'] = even_positions

        solved_sudoku = copy.deepcopy(self.grid)

        self.__create_empty_cells()

        return copy.deepcopy(self.grid), solved_sudoku, args
