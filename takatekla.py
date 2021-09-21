from tkinter import *
from game import Game
import sys

columns = int(sys.argv[1])
rows = int(sys.argv[2])
mode = sys.argv[3]

cellW = 252
cellH = 80

# you can modify default main colors here
colors = {"panel-bg": "#30261c", "main-bg": "#1F5F61", "disabled-bg": "#0B8185"}

master = Tk()
game = Game(cellW, cellH, rows, columns, master, mode, colors=colors)
master.mainloop()
