"""Minimal stand-in for the Python 2 Tkinter module.

Every widget constructor returns an object whose grid()/pack() do nothing.
The engine modules import Tkinter at module level; this keeps them importable
on a server with no display.
"""


class _Widget:
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    def grid(self, *args, **kwargs):
        return None

    def pack(self, *args, **kwargs):
        return None

    def configure(self, *args, **kwargs):
        return None

    def destroy(self):
        return None


Label = Button = Checkbutton = Frame = Tk = Toplevel = Listbox = Scrollbar = _Widget


class IntVar:
    def __init__(self, value=0):
        self._v = value

    def get(self):
        return self._v

    def set(self, v):
        self._v = v


StringVar = IntVar
END = "end"
