import re
import time
from tkinter import Tk, filedialog

from sudoku_generator import *
from board import Board


def require_choice_number(possible_values):
    while True:
        choice_number_str = input()

        if choice_number_str.strip() == '':
            print('Entering a choice number is required: ')
            continue

        if int(choice_number_str) not in possible_values:
            print('Unrecognized choice! Please try again: ')
        else:
            break

    choice_number = int(choice_number_str)
    return choice_number


def require_dimension():
    for pair in DIMENSIONS:
        print(pair[0], ': ', pair[1])

    print('Enter the number of the puzzle dimension: ')
    return require_choice_number([pair[0] for pair in DIMENSIONS])


def require_mode():
    for pair in MODES:
        print(pair[0], ': ', pair[1])

    print('Enter the number of the puzzle mode: ')
    return require_choice_number([pair[0] for pair in MODES])


def require_difficulty():
    for pair in DIFFICULTIES:
        print(pair[0], ': ', pair[1])

    print('Enter the number of the puzzle difficulty: ')
    return require_choice_number([pair[0] for pair in DIFFICULTIES])


def start_game(dimension, mode, empty_cells):
    possible_values = SUDOKU_VALUES[:dimension].copy()
    sudoku_generator = SudokuGenerator(dimension, mode, empty_cells, possible_values)
    sudoku, solved_sudoku, args = sudoku_generator.generate()

    play(dimension, mode, sudoku, solved_sudoku, **args)


def upload_puzzle():
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    filename = filedialog.askopenfilename()

    lines = []
    with open(filename) as file:
        lines = [line.strip() for line in file]

    try:
        dimension = int(lines[0])
        mode = lines[1]

        if dimension not in [pair[2] for pair in DIMENSIONS]:
            print('Incorrect dimension!')
            return

        if mode not in [pair[1] for pair in MODES]:
            print('Incorrect mode!')
            return

        args = {}
        sudoku = []

        counter = 2
        while counter < dimension + 2:
            row = [symbol for symbol in re.split('\s+|\|', lines[counter]) if symbol and symbol.isspace() is False]
            sudoku.append(row)
            counter += 1

        even_positions = []
        if mode == 'Odd-Even Sudoku':
            while counter < len(lines):
                matches = re.findall("\((.*?)\)", lines[counter])

                for match in matches:
                    coordinates = tuple([COORDINATES_DICT[coord] - 1 for coord in re.split('\s+|,', match) if coord and coord.isspace() is False])
                    even_positions.append(coordinates)

                counter += 1

            args = {'even_positions': copy.deepcopy(even_positions)}

        solved_sudoku = SudokuPuzzle.solve_puzzle(sudoku, mode, **args)

        play(dimension, mode, sudoku, solved_sudoku, **args)
    except:
        print('Invalid file content! Dimension, mode, puzzle, and even positions (depending on the mode) must be entered sequentially on new lines.')


def require_coordinate(axis):
    print("Enter " + axis + ": ")

    while True:
        choice = input()

        if choice.strip() == '':
            print('Entering a ' + axis + ' is required: ')
            continue

        if choice not in SUDOKU_VALUES:
            print('Unrecognized choice! Please try again: ')
        else:
            break

    return choice


def require_position():
    row = require_coordinate("row")
    col = require_coordinate("column")

    return row, col


def require_sudoku_value():
    print("Enter value: ")

    while True:
        value = input()

        if value.strip() == '':
            print('Entering a cell value is required: ')
            continue

        if value != '0' and value not in SUDOKU_VALUES:
            print('Unrecognized choice! Please try again: ')
        else:
            break

    return value


def clear_board():
    count = 3
    while count != 0:
        print("\rClearing the board.", end='')
        time.sleep(0.33)
        print("\rClearing the board..", end='')
        time.sleep(0.33)
        print("\rClearing the board...", end='')
        time.sleep(0.34)

        count -= 1

    print('\r\n', end='\n')


def play(dimension, mode, sudoku, solved_sudoku, **args):
    possible_values = SUDOKU_VALUES[:dimension].copy()
    board = Board(dimension, mode, possible_values, sudoku, solved_sudoku, **args)

    print(board, '\n')

    while True:
        for key in COMMAND_DICT:
            print(key, ': ', COMMAND_DICT[key])
        print('Enter the number of the command you want to execute: ')

        command_number = require_choice_number(COMMAND_DICT.keys())

        if COMMAND_DICT[command_number] == 'Update cell':
            position = require_position()
            value = require_sudoku_value()

            board.update_cell(position, value)

        elif COMMAND_DICT[command_number] == 'Undo':
            board.undo()

        elif COMMAND_DICT[command_number] == 'Redo':
            board.redo()

        elif COMMAND_DICT[command_number] == 'Hint':
            position = require_position()
            value = "Hint"

            board.update_cell(position, value)

        elif COMMAND_DICT[command_number] == 'Start':
            pass

        elif COMMAND_DICT[command_number] == 'Stop':
            pass

        elif COMMAND_DICT[command_number] == 'Check Puzzle':
            status_code = board.check_puzzle()
            status_tuple = [item for item in STATUSES if item[0] == status_code][0]

            status = status_tuple[1]
            message = status_tuple[2]

            print(message)

            if status == 'SOLVED':
                clear_board()
                break

        elif COMMAND_DICT[command_number] == 'Restart Puzzle':
            board.restart()

        elif COMMAND_DICT[command_number] == 'Solve Puzzle':
            board.solve()
            print(board, '\n')

            clear_board()
            break

        elif COMMAND_DICT[command_number] == 'Main Menu':
            break

        print(board, '\n')
