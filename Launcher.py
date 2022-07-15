import os
from tkinter import *


root = Tk()
root.title("Launcher")
root.geometry("400x400")

def open_app(app):
    os.startfile(app)

#gui for shiz


root.mainloop()
