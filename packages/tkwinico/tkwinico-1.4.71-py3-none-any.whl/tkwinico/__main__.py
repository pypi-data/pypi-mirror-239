if __name__ == '__main__':
    from tkinter import Tk, Menu
    from tkwinico import Winico
    import os

    root = Tk()

    winico = Winico()

    root.wm_title(f"Winico {winico.winico_version()} Demo")

    if os.path.exists(winico.TkChat):
        icon = winico.icon(icon_file=winico.TkChat)
    else:
        icon = winico.icon(icon_name="exclamation")

    winico.tray_add(icon, tooltip="Nothing selected (unicode: \u043a\u043c\u0436)")

    def MenuCommand(icon, index):
        text = f"Last selected item {index} (%c)"


    menu = Menu(tearoff=0)
    menu.add_command(label="Item One", command=lambda icon: MenuCommand(icon, 1))

    root.mainloop()
