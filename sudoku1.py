import sys

from clingo.application import Application, clingo_main


class ClingoApp(Application):
    def print_model(self, model, printer):
        symbols = sorted(model.symbols(shown=True))
        print(" ".join(str(s) for s in symbols))
        sys.stdout.flush()

    def main(self, ctl, files):
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

        for f in files:
            ctl.load(f)

        if not files:
            ctl.load("-")

        ctl.ground([("base", [])])
        ctl.solve()


if __name__ == "__main__":
    clingo_main(ClingoApp())
