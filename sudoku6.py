import sys

import clingo
from clingo.application import Application, clingo_main

from sudoku_board import Sudoku 

class Context:

    def __init__(self, board: Sudoku):
        self.board = board
        
    def initial(self) -> list[clingo.symbol.Symbol]:
        return [
            clingo.Function(
                "",
                [clingo.Number(row), clingo.Number(col), clingo.Number(value)],
                True,
            )
            for (row, col), value in self.board.sudoku.items()
        ]


class ClingoApp(Application):

    def print_model(self, model, printer):
        symbols = sorted(model.symbols(shown=True))
        print(Sudoku.from_model(model))
        sys.stdout.flush()

    def main(self, ctl, files):
        if files:
            with open(files[0], encoding="utf-8") as puzzle_file:
                board = Sudoku.from_str(puzzle_file.read())
        else:
            board = Sudoku.from_str(sys.stdin.read())

        ctl.add(
            "base",
            [],
            """
            1 { sudoku(X,Y,N) : N=1..9 } 1 :- X=1..9, Y=1..9.

            subgrid(X,Y,G) :- X=1..9, Y=1..9, G=1+(((X-1)/3)*3+(Y-1)/3).

            :- initial(X,Y,N), not sudoku(X,Y,N).

            :- sudoku(X,Y1,N), sudoku(X,Y2,N), Y1 < Y2. 
            :- sudoku(X1,Y,N), sudoku(X2,Y,N), X1 < X2.
            :- sudoku(X1,Y1,N), sudoku(X2,Y2,N),
               subgrid(X1,Y1,G), subgrid(X2,Y2,G), X1 < X2.

            #show sudoku/3.
            """,
        )

        ctl.load("sudoku_py.lp")

        ctl.ground([("base", [])], context=Context(board))
        ctl.solve()


if __name__ == "__main__":
    clingo_main(ClingoApp())
