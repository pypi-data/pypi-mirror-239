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
        self.load_winico()

    @contextlib.contextmanager
    def chdir(self, target: str):
        """Context-managed chdir, original implementation by GitHub @Akuli"""
        current = os.getcwd()
        try:
            os.chdir(target)
            yield
        finally:
            os.chdir(current)

    def load_winico(self, version: str = "0.6"):
        local = os.path.abspath(os.path.dirname(__file__))
        with self.chdir(local):
            self.master.eval("set dir [file dirname [info script]]")
            self.master.eval("source pkgIndex.tcl")
            self.master.eval("package require Winico " + version)

    def smiley(self):
        return self.createfrom(self.Smiley)

    def tkchat(self):
        return self.createfrom(TkChat)

    def load(self, resourcename, filename=None) -> str:
        """
        application, asterisk, error, exclamation, hand, question, information, warning, winlogo.
        """
        return self.master.call("winico", "load", resourcename, filename)

    def createfrom(self, filename=None) -> str:
        return self.master.call("winico", "createfrom", filename)

    def info(self, id):
        list = TclPyListTranslator(self.master.tk).to_py(self.master.call("winico", "info", id))
        list2 = []
        for i in range(len(list)):
            if i % 2 == 0:
                list2.append(i)
        dict = {}
        for i in list2:
            dict[list[i][1:]] = list[i+1]
        return dict

    def delete(self, id):
        return self.master.call("winico", "delete", id)

    def taskbar(self, id, procname="$winico", callback=None, args=("%message", "%i", "%x", "%y"), text: str = ""):
        """
        id: add, modify, delete
        args: %m, %i, %x, %y, %X, %Y, %t, %w, %l
        """
        if callback is None:
            def func(*args, **kwargs):
                pass

            _callback = self.master.register(func)
        else:
            _callback = [self.master.register(callback)]
            for arg in args:
                _callback.append(arg)
        return self.master.call("winico", "taskbar", id, procname,
                                "-callback", tuple(_callback),
                                "-text", text
                                )


if __name__ == '__main__':
    root = Tk()

    winico = Winico()
    id = winico.load("question")
    winico.taskbar("add", winico.smiley(), callback=lambda msg, i, x, y: print(msg, x, y))
    print(winico.info(id))
    root.mainloop()
