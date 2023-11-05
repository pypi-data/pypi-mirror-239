from tkwinico.const import *
from tkwinico.winico import Winico


if __name__ == '__main__':
    import tkinter as tk

    Window = tk.Tk()

    Ico = Winico(Window)


    def CallBack(Message, X, Y):
        if Message == "WM_RBUTTONDOWNessage":
            Menu = tk.Menu(tearoff=False)
            Menu.add_command(label="Quit", command=Window.quit)
            Menu.tk_popup(X, Y)


    Ico.tray_add(Ico.icon(APPLICATION), callback=CallBack, callback_args=[MESSAGE, X, Y])

    Window.mainloop()