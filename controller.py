"""

wx.Notebook that contains controls from each module

"""

import wx

class Controller(wx.Notebook):
    "wx.Notebook for modules"

    def __init__(self, parent, *args, **kwargs):
        "Notebook constructor"

        wx.Notebook.__init__(self, parent, *args, **kwargs)

        self.AddPage(wx.Panel(self), "foo module")

# vim: autoindent shiftwidth=4 expandtab textwidth=80
