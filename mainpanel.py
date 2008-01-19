"""

wx.Panel for operator interface

"""

import wx

import controller
import oos

class MainPanel(wx.Panel):
    "Operator interface"

    def __init__(self, parent, *args, **kwargs):
        "Panel constructor"

        wx.Panel.__init__(self, parent, *args, **kwargs)

        controlbook = controller.Controller(self)
        oospanel = oos.OrderOfService(self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(oospanel, 0, wx.ALL, 10)
        sizer.Add(controlbook, 1, wx.TOP|wx.BOTTOM|wx.LEFT, 10)

        self.SetSizerAndFit(sizer)

# vim: autoindent shiftwidth=4 expandtab textwidth=80
