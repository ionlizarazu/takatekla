from tkinter import Game, Tk

from game import Game


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Import users from a website to another"
    )
    parser.add_argument(
        "columns",
        help="Number of columns to render",
    )
    parser.add_argument(
        "rows",
        help="Number of rows to render",
    )
    parser.add_argument("mode", help="Game mode", choices=["i", "t"])

    args = parser.parse_args()

    cellW = 252
    cellH = 80

    # you can modify default main colors here
    colors = {
        "panel-bg": "#30261c",
        "main-bg": "#1F5F61",
        "disabled-bg": "#0B8185",
    }
    master = Tk()
    Game(
        cellW,
        cellH,
        int(args.rows),
        int(args.columns),
        master,
        args.mode,
        colors=colors,
    )
    master.mainloop()


main()
