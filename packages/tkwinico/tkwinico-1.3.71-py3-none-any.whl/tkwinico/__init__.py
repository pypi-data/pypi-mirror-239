from tkwinico.load import load_winico
from tkwinico.command import *
from tkwinico.const import *
from tkwinico.winico import Winico


if __name__ == '__main__':
    import tkinter as tk

    Window = tk.Tk()

    Ico = Winico(Window)


    def CallBack(Message, X, Y):
        if Message == WM_RBUTTONDOWN:
            Menu = tk.Menu(tearoff=False)
            Menu.add_command(label="Quit", command=Window.quit)
            Menu.tk_popup(X, Y)


    Ico.taskbar(ADD, Ico.load(APPLICATION), callback=CallBack, args=[MESSAGE, X, Y])

    Window.mainloop()