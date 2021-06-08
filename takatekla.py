from tkinter import *
from game import Game
import sys

columns = int(sys.argv[1])
rows = int(sys.argv[2])

cellW = 250
cellH = 80

# you can modify default main colors here
colors = {
    "main-bg": "#146791", "disabled-bg": "#7798a8"
}

master = Tk()
game = Game(cellW, cellH, rows, columns, master, colors=colors)
master.mainloop()
