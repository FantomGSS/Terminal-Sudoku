import copy
import math

from sudoku_puzzle import SudokuPuzzle
from action import Action
from settings import *


class Board:
    def __init__(self, dimension, mode, possible_values, sudoku, solved_sudoku, **args) -> None:
        self.dimension = dimension
        self.mode = mode
        self.possible_values = possible_values.copy()

        self.initial_board = copy.deepcopy(sudoku)
        self.solved_board = copy.deepcopy(solved_sudoku)
        self.board = copy.deepcopy(sudoku)

        self.fixed_positions = []
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.board[i][j] != '0':
                    self.fixed_positions.append((i, j))

        self.wrong_positions = []

        self.actions = []
        self.actionPosition = -1

        self.is_enabled_undo = False
        self.is_enabled_redo = False

        self.even_positions = []
        if self.mode == 'Odd-Even Sudoku' and 'even_positions' in args:
            self.even_positions = copy.deepcopy(args['even_positions'])

    def __str__(self) -> str:
        def get_key_by_value(coordinate):
            for key, value in COORDINATES_DICT.items():
                if coordinate == value:
                    return key

        board_string = '  '

        numbering = [i + 1 for i in range(self.dimension)]
        for i in numbering:
            if i != self.dimension:
                board_string += '\033[94m' + get_key_by_value(i) + '\033[0m' + ' '

                if i % int(math.sqrt(self.dimension)) == 0:
                    board_string += '  '
            else:
                board_string += '\033[94m' + get_key_by_value(i) + '\033[0m'

        for i in range(self.dimension):
            board_string += '\n' + '\033[94m' + get_key_by_value(i + 1) + '\033[0m' + ' '

            for j in range(self.dimension):
                if (i, j) in self.fixed_positions:
                    if (i, j) in self.even_positions:
                        board_string += '\033[4;100m' + str(self.board[i][j]) + '\033[0m' + ' '
                    else:
                        board_string += '\033[4m' + str(self.board[i][j]) + '\033[0m' + ' '
                else:
                    if self.board[i][j] == '0':
                        if (i, j) in self.even_positions:
                            board_string += '\033[100m' + str(self.board[i][j]) + '\033[0m' + ' '
                        else:
                            board_string += str(self.board[i][j]) + ' '
                    else:
                        if (i, j) in self.even_positions:
                            if (i, j) in self.wrong_positions:
                                board_string += '\033[91;100m' + str(self.board[i][j]) + '\033[0m' + ' '
                            else:
                                board_string += '\033[92;100m' + str(self.board[i][j]) + '\033[0m' + ' '
                        else:
                            if (i, j) in self.wrong_positions:
                                board_string += '\033[91m' + str(self.board[i][j]) + '\033[0m' + ' '
                            else:
                                board_string += '\033[92m' + str(self.board[i][j]) + '\033[0m' + ' '

                if (j + 1) % int(math.sqrt(self.dimension)) == 0:
                    board_string += '  '

                if j == self.dimension - 1:
                    board_string = board_string[:-3]

            if i + 1 != self.dimension and (i + 1) % int(math.sqrt(self.dimension)) == 0:
                board_string += '\n'

        return board_string

    def update_cell(self, position, value) -> None:
        coordinates = COORDINATES_DICT[position[0]] - 1, COORDINATES_DICT[position[1]] - 1
        symbol = None

        if value == "Hint":
            symbol = self.solved_board[coordinates[0]][coordinates[1]]
        else:
            symbol = value

        if symbol == self.board[coordinates[0]][coordinates[1]]:
            print("The value is the same as the one already placed in cell!")
            return

        if coordinates in self.fixed_positions:
            print("You cannot set a value to a fixed cell!")
            return

        if coordinates in self.wrong_positions:
            self.wrong_positions.remove(coordinates)

        is_valid_note = SudokuPuzzle.is_valid_note(self.board, self.mode, coordinates[0], coordinates[1], symbol, even_positions=self.even_positions)

        action = Action(coordinates[0], coordinates[1], self.board[coordinates[0]][coordinates[1]], symbol)

        if self.actionPosition < len(self.actions) - 1:
            self.actions = copy.deepcopy(self.actions[:self.actionPosition + 1])
            self.is_enabled_redo = False

        self.actions.append(action)
        self.actionPosition = len(self.actions) - 1
        self.is_enabled_undo = True

        if not is_valid_note:
            self.wrong_positions.append(coordinates)

        self.board[coordinates[0]][coordinates[1]] = symbol

    def undo(self) -> None:
        if self.is_enabled_undo:
            action = self.actions[self.actionPosition]
            self.actionPosition -= 1

            if self.actionPosition == -1:
                self.is_enabled_undo = False

            row = action.get_row()
            col = action.get_col()
            symbol = action.get_old_symbol()

            if (row, col) in self.wrong_positions:
                self.wrong_positions.remove((row, col))

            is_valid_note = SudokuPuzzle.is_valid_note(self.board, self.mode, row, col, symbol, even_positions=self.even_positions)
            if not is_valid_note:
                self.wrong_positions.append((row, col))

            self.is_enabled_redo = True
            self.board[row][col] = symbol
        else:
            return

    def redo(self) -> None:
        if self.is_enabled_redo:
            self.actionPosition += 1

            if self.actionPosition == len(self.actions) - 1:
                self.is_enabled_redo = False

            action = self.actions[self.actionPosition]
            row = action.get_row()
            col = action.get_col()
            symbol = action.get_new_symbol()

            if (row, col) in self.wrong_positions:
                self.wrong_positions.remove((row, col))

            is_valid_note = SudokuPuzzle.is_valid_note(self.board, self.mode, row, col, symbol, even_positions=self.even_positions)
            if not is_valid_note:
                self.wrong_positions.append((row, col))

            self.is_enabled_undo = True
            self.board[row][col] = symbol
        else:
            return

    def check_puzzle(self) -> int:
        if SudokuPuzzle.check_puzzle(self.board, self.mode, even_positions=self.even_positions):
            if SudokuPuzzle.puzzle_is_complete(self.board):
                return 1
            else:
                return 2
        else:
            return 3

    def restart(self):
        self.board = copy.deepcopy(self.initial_board)
        self.wrong_positions = []

        self.actions = []
        self.actionPosition = -1

        self.is_enabled_undo = False
        self.is_enabled_redo = False

    def solve(self):
        self.board = copy.deepcopy(self.solved_board)
