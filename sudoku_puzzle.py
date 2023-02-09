import copy
import math

from settings import *


class SudokuPuzzle:
    @staticmethod
    def __get_main_diagonal_data(puzzle) -> tuple:
        dimension = len(puzzle)

        main_diagonal = [puzzle[i][i] for i in range(0, dimension)]
        main_diagonal_coords = [(i, i) for i in range(0, dimension)]

        return main_diagonal, main_diagonal_coords

    @staticmethod
    def __get_minor_diagonal_data(puzzle) -> tuple:
        dimension = len(puzzle)

        minor_diagonal = [puzzle[dimension - 1 - i][i] for i in range(0, dimension)]
        minor_diagonal_coords = [(dimension - 1 - i, i) for i in range(0, dimension)]

        return minor_diagonal, minor_diagonal_coords

    @staticmethod
    def puzzle_is_complete(puzzle) -> bool:
        dimension = len(puzzle)

        for i in range(dimension):
            for j in range(dimension):
                if puzzle[i][j] == '0':
                    return False

        return True

    @staticmethod
    def check_puzzle(puzzle, mode, **args) -> bool:
        dimension = len(puzzle)
        sub_dimension = int(math.sqrt(dimension))

        for i in range(dimension):
            row_without_empty_cells = [cell for cell in puzzle[i] if cell != '0']

            col = []
            for j in range(dimension):
                col.append(puzzle[j][i])

            col_without_empty_cells = [cell for cell in col if cell != '0']

            if (len(row_without_empty_cells) != len(set(row_without_empty_cells))) or (len(col_without_empty_cells) != len(set(col_without_empty_cells))):
                return False

        for row in range(0, dimension, sub_dimension):
            for col in range(0, dimension, sub_dimension):
                square = []

                for i in range(row, row + sub_dimension):
                    for j in range(col, col + sub_dimension):
                        if puzzle[i][j] != '0':
                            square.append(puzzle[i][j])

                if len(square) != len(set(square)):
                    return False

        if mode == 'Diagonal Sudoku':
            main_diagonal, main_diagonal_coords = SudokuPuzzle.__get_main_diagonal_data(puzzle)
            main_diagonal_without_empty_cells = [cell for cell in main_diagonal if cell != '0']

            if len(set(main_diagonal_without_empty_cells)) != len(main_diagonal_without_empty_cells):
                return False

            minor_diagonal, minor_diagonal_coords = SudokuPuzzle.__get_minor_diagonal_data(puzzle)
            minor_diagonal_without_empty_cells = [cell for cell in minor_diagonal if cell != '0']

            if len(set(minor_diagonal_without_empty_cells)) != len(minor_diagonal_without_empty_cells):
                return False

        if mode == 'Odd-Even Sudoku':
            even_positions = args['even_positions']

            for pair in even_positions:
                row = pair[0]
                col = pair[1]

                symbol = puzzle[row][col]

                if symbol != '0' and COORDINATES_DICT[symbol] % 2 != 0:
                    return False

        return True

    @staticmethod
    def is_valid_note(puzzle, mode, row, col, symbol, **args) -> bool:
        dimension = len(puzzle)
        sub_dimension = int(math.sqrt(dimension))

        for i in range(dimension):
            if puzzle[i][col] == symbol and puzzle[i][col] != '0':
                return False

            if puzzle[row][i] == symbol and puzzle[row][i] != '0':
                return False

            if puzzle[sub_dimension * int(row / sub_dimension) + int(i / sub_dimension)][sub_dimension * int(col / sub_dimension) + i % sub_dimension] != '0' \
                    and puzzle[sub_dimension * int(row / sub_dimension) + int(i / sub_dimension)][sub_dimension * int(col / sub_dimension) + i % sub_dimension] == symbol:
                return False

        if symbol != '0':
            if mode == 'Diagonal Sudoku':
                puzzle[row][col] = symbol

                main_diagonal, main_diagonal_coords = SudokuPuzzle.__get_main_diagonal_data(puzzle)
                if (row, col) in main_diagonal_coords:
                    main_diagonal_without_empty_cells = [cell for cell in main_diagonal if cell != '0']

                    if len(set(main_diagonal_without_empty_cells)) != len(main_diagonal_without_empty_cells):
                        return False

                minor_diagonal, minor_diagonal_coords = SudokuPuzzle.__get_minor_diagonal_data(puzzle)
                if (row, col) in minor_diagonal_coords:
                    minor_diagonal_without_empty_cells = [cell for cell in minor_diagonal if cell != '0']

                    if len(set(minor_diagonal_without_empty_cells)) != len(minor_diagonal_without_empty_cells):
                        return False

            if mode == 'Odd-Even Sudoku':
                even_positions = args['even_positions']

                if ((row, col) in even_positions) ^ (COORDINATES_DICT[symbol] % 2 == 0):
                    return False

        return True

    @staticmethod
    def solve_puzzle_helper(puzzle, mode, **args) -> bool:
        dimension = len(puzzle)
        possible_values = SUDOKU_VALUES[:dimension].copy()

        for i in range(dimension):
            for j in range(dimension):
                if puzzle[i][j] == '0':
                    for symbol in possible_values:
                        if SudokuPuzzle.is_valid_note(puzzle, mode, i, j, symbol, **args):
                            puzzle[i][j] = symbol

                            if SudokuPuzzle.solve_puzzle_helper(puzzle, mode, **args):
                                return True

                            puzzle[i][j] = '0'

                    return False

        return True

    @staticmethod
    def solve_puzzle(puzzle, mode, **args) -> list:
        puzzle = copy.deepcopy(puzzle)
        SudokuPuzzle.solve_puzzle_helper(puzzle, mode, **args)

        return puzzle
