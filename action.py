class Action:
    def __init__(self, row, col, old_symbol, new_symbol) -> None:
        self.row = row
        self.col = col
        self.old_symbol = old_symbol
        self.new_symbol = new_symbol

    def get_row(self) -> int:
        return self.row

    def get_col(self) -> int:
        return self.col

    def get_old_symbol(self) -> str:
        return self.old_symbol

    def get_new_symbol(self) -> str:
        return self.new_symbol
