"""

wx.Panel for operator interface

"""

import wx

import controller
import leftpanel

class MainPanel(wx.Panel):
    "Operator interface"

    def __init__(self, parent, *args, **kwargs):
        "Panel constructor"

        wx.Panel.__init__(self, parent, *args, **kwargs)

        controlbook = controller.Controller(self, size=wx.Size(400,300))
        leftside = leftpanel.LeftPanel(self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(leftside, 0, wx.GROW|wx.TOP|wx.BOTTOM|wx.LEFT, 15)
        sizer.Add(controlbook, 1, wx.GROW|wx.ALL, 15)

        self.SetSizerAndFit(sizer)
        sizer.SetSizeHints(parent)

# vim: autoindent shiftwidth=4 expandtab textwidth=80
