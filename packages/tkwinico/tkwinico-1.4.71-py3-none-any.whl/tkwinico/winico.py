from tkinter import Tk
import contextlib
import os


class TclPyListTranslator(object):
    def __init__(self, tcl):
        self._tcl = tcl

    def to_py(self, tcl_list, dtype=str):
        # convert a Tcl List to python list, also convert elements of each leaf
        # node to dtype
        self._tcl.eval("set tcl_list %s" % tcl_list)
        numItems = int(self._tcl.eval("llength $tcl_list"))
        if numItems > 1:
            result = [self._tcl.eval("lindex $tcl_list %d" % i) for i in range(
                numItems)]
            for i in range(numItems):
                result[i] = self.to_py("{" + result[i] + "}", dtype)
        else:
            result = dtype(self._tcl.eval("lindex $tcl_list %d" % 0))
        return result


class Winico(object):
    Smiley = os.path.abspath(os.path.dirname(__file__)) + "//smiley.ico"

    TkChat = os.path.abspath(os.path.dirname(__file__)) + "//tkchat.ico"

    def __init__(self, master: Tk = None):
        if master is None:
            from tkinter import _default_root
            master = _default_root
        self.master = master
        self.__load_winico()

    @contextlib.contextmanager
    def __chdir(self, target: str):
        """Context-managed chdir, original implementation by GitHub @Akuli"""
        current = os.getcwd()
        try:
            os.chdir(target)
            yield
        finally:
            os.chdir(current)

    def __load_winico(self, version: str = "0.7.1"):
        local = os.path.abspath(os.path.dirname(__file__))
        with self.__chdir(local):
            self.master.eval("set dir [file dirname [info script]]")
            self.master.eval("source pkgIndex.tcl")
            self.master.eval("package require Winico " + version)

    def winico_require(self, version="0.7.1"):
        self.__load_winico(version)

    def winico_version(self):
        return self.master.eval("package provide Winico")

    def smiley(self):
        return self._createfrom(self.Smiley)

    def tkchat(self):
        return self._createfrom(self.TkChat)

    def _load(self, resourcename, filename=None) -> str:
        """
        application, asterisk, error, exclamation, hand, question, information, warning, winlogo.
        """
        return self.master.call("winico", "load", resourcename, filename)

    def _createfrom(self, filename=None) -> str:
        return self.master.call("winico", "createfrom", filename)

    def _info(self, id):
        list = TclPyListTranslator(self.master.tk).to_py(self.master.call("winico", "info", id))
        list2 = []
        for i in range(len(list)):
            if i % 2 == 0:
                list2.append(i)
        dict = {}
        for i in list2:
            dict[list[i][1:]] = list[i + 1]
        return dict

    def _delete(self, id):
        return self.master.call("winico", "delete", id)

    def _taskbar(self, action, id, callback=None, callback_args=("%message", "%i", "%x", "%y"), text: str = None):
        """
        action: add, modify, delete
        args: %m, %i, %x, %y, %X, %Y, %t, %w, %l
        """
        if callback is not None:
            _callback = [self.master.register(callback)]
            for arg in callback_args:
                _callback.append(arg)

        a = ["winico", "taskbar", action, id]
        if callback is not None:
            a.append("-callback")
            a.append(_callback)
        if text is not None:
            a.append("-text")
            a.append(text)
        return self.master.call(*a)

    def icon(self, icon_name=None, icon_file=None):
        """
        icon_name: (application, asterisk, error, exclamation, hand, question, information, warning, winlogo)
        icon_file: 图标文件地址.
        返回图标ID
        """
        if icon_name is not None:
            return self._load(icon_name)
        else:
            if icon_file is not None:
                return self._createfrom(icon_file)
            else:
                return None

    def icon_info(self, icon_id):
        """
        返回图标的信息
        """
        return self._info(icon_id)

    def icon_delete(self, icon_id):
        """
        删除图标
        """
        self._delete(icon_id)

    def tray_add(self, icon_id, callback=None, callback_args=("%message", "%i", "%x", "%y"), tooltip: str = None):
        """
        icon_id: 图标ID
        callback: 回调事件，会得到callback_args中的参数
        callback_args: 回调事件参数 (%m, %i, %x, %y, %X, %Y, %t, %w, %l)
        tooltip: 工具提示，将鼠标放上会显示提示
        将图标添加进托盘
        """
        self._taskbar(action="add", id=icon_id, callback=callback, callback_args=callback_args, text=tooltip)

    def tray_delete(self, icon_id):
        """
        icon_id: 图标ID)
        将图标从托盘中移除
        """
        self._taskbar(action="delete", id=icon_id)

    def tray_modify(self, icon_id, callback=None, callback_args=("%message", "%i", "%x", "%y"), tooltip: str = None):
        """
        icon_id: 图标ID
        callback: 回调事件，会得到callback_args中的参数
        callback_args: 回调事件参数 (%m, %i, %x, %y, %X, %Y, %t, %w, %l)
        tooltip: 工具提示，将鼠标放上会显示提示
        修改托盘图标
        """
        self._taskbar(action="modify", id=icon_id, callback=callback, callback_args=callback_args, text=tooltip)


if __name__ == '__main__':
    root = Tk()

    winico = Winico()


    def callback(msg, i, x, y):
        print(msg)
        if msg == "WM_MBUTTONDOWNessage":
            root.quit()
            winico.tray_delete(i)


    # id = winico.icon("application")
    id = winico.smiley()
    winico.tray_add(id, callback=callback)

    winico.tray_modify(id, tooltip="HelloWorld")

    root.mainloop()
