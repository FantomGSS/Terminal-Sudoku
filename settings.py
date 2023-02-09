DIMENSIONS = [(1, '4x4', 4), (2, '9x9', 9), (3, '16x16', 16)]
MODES = [(1, 'Sudoku'), (2, 'Odd-Even Sudoku'), (3, 'Diagonal Sudoku')]
DIFFICULTIES = [(1, 'Easy'), (2, 'Medium'), (3, 'Hard')]

DEFAULT_DIMENSION_INDEX = 1
DEFAULT_MODE_INDEX = 0
DEFAULT_DIFFICULTY_INDEX = 0

SUDOKU_VALUES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G']

COORDINATES_DICT = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'A': 10,
    'B': 11,
    'C': 12,
    'D': 13,
    'E': 14,
    'F': 15,
    'G': 16
}

MENU_DICT = {
    1: 'Dimension',
    2: 'Mode',
    3: 'Difficulty',
    4: 'Start Game',
    5: 'Upload Puzzle',
    6: 'Quit'
}

COMMAND_DICT = {
    1: 'Update cell',
    2: 'Undo',
    3: 'Redo',
    4: 'Hint',
    5: 'Start',
    6: 'Stop',
    7: 'Check Puzzle',
    8: 'Restart Puzzle',
    9: 'Solve Puzzle',
    10: 'Main Menu'
}

EMPTY_CELLS_DICT = {
    (4, 'Easy'): 4,
    (4, 'Medium'): 7,
    (4, 'Hard'): 10,
    (9, 'Easy'): 30,
    (9, 'Medium'): 45,
    (9, 'Hard'): 60,
    (16, 'Easy'): 62,
    (16, 'Medium'): 133,
    (16, 'Hard'): 180
}

STATUSES = [(1, 'SOLVED', 'Congratulations! You have successfully solved the puzzle.'),
            (2, 'INCOMPLETE', 'At this point, the puzzle is correct, but there are still empty cells.'),
            (3, 'WRONG', 'Unfortunately, there are incorrectly filled values.')]
