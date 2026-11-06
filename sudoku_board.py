from typing import Tuple
import clingo


class Sudoku:
    def __init__(self, sudoku: dict[Tuple[int, int], int]):
        self.sudoku = sudoku

    def __str__(self) -> str:
        s = ""
        for x in range(1, 10):
            for y in range(1, 10):
                n = self.sudoku.get((x, y), 0)
                s += str(n)
                if y < 9:
                    if y % 3 == 0:
                        s += "  "
                    else:
                        s += " "
            s += "\n"
            if x % 3 == 0 and x != 9:
                s += "\n"
        return s

    @classmethod
    def from_str(cls, s: str) -> "Sudoku":
        sudoku = {}
        cells = s.split()
        if len(cells) != 81:
            raise ValueError(f"Expected 81 cells, got {len(cells)}")

        for index, cell in enumerate(cells):
            if cell != "-":
                row, col = divmod(index, 9)
                sudoku[(row + 1, col + 1)] = int(cell)

        return cls(sudoku)

    @classmethod
    def from_model(cls, model: clingo.solving.Model) -> "Sudoku":
        sudoku = {}
        for symbol in model.symbols(shown=True):
            if symbol.name == "sudoku" and len(symbol.arguments) == 3:
                x, y, n = symbol.arguments
                sudoku[(x.number, y.number)] = n.number
        return cls(sudoku)
