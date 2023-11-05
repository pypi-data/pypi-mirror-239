# tkwinico
为`Windows`系统提供开发系统托盘的功能。

---

## 注意事项
版本号前两位是库的版本号，后一位则是`Winico`的版本号。

如`x.x.71`或`x.x.6`，
`Winico`的`71`版本支持`x64位`电脑
而`6`版本支持`x32位`电脑
请按需要安装

仅支持`Windows`系统

## 示例
```python
from tkwinico import *
import tkinter as tk


Window = tk.Tk()


def CallBack(Message, X, Y):
    if Message == WM_RBUTTONDOWN:
        Menu = tk.Menu(tearoff=False)
        Menu.add_command(label="Quit", command=Window.quit)
        Menu.tk_popup(X, Y)


taskbar(ADD, load(APPLICATION), (Window.register(CallBack), MESSAGE, X, Y))

Window.mainloop()
```
或
```python
from tkwinico import *
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
```