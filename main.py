from menu import *


dimension_index, mode_index, difficulty_index = None, None, None

while True:
    for key in MENU_DICT:
        print(key, ': ', MENU_DICT[key])
    print('Enter the number of the command you want to execute: ')

    command_number = require_choice_number(MENU_DICT.keys())

    if MENU_DICT[command_number] == 'Dimension':
        dimension_index = require_dimension() - 1

    elif MENU_DICT[command_number] == 'Mode':
        mode_index = require_mode() - 1

    elif MENU_DICT[command_number] == 'Difficulty':
        difficulty_index = require_difficulty() - 1

    elif MENU_DICT[command_number] == 'Start Game':
        dimension_index = dimension_index if dimension_index is not None else DEFAULT_DIMENSION_INDEX
        mode_index = mode_index if mode_index is not None else DEFAULT_MODE_INDEX
        difficulty_index = difficulty_index if difficulty_index is not None else DEFAULT_DIFFICULTY_INDEX

        dimension = int(DIMENSIONS[dimension_index][2])
        mode = MODES[mode_index][1]
        difficulty = DIFFICULTIES[difficulty_index][1]

        empty_cells = EMPTY_CELLS_DICT[(dimension, difficulty)]

        start_game(dimension, mode, empty_cells)

        dimension_index, mode_index, difficulty_index = None, None, None

    elif MENU_DICT[command_number] == 'Upload Puzzle':
        upload_puzzle()

    elif MENU_DICT[command_number] == 'Quit':
        break
