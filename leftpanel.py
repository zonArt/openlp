"""

wx.Panel for operator interface

"""

import wx

import oos

class LeftPanel(wx.Panel):
    "Left half of operator interface"

    def __init__(self, parent, *args, **kwargs):
        "Panel constructor"

        wx.Panel.__init__(self, parent, *args, **kwargs)

        oospanel = oos.OrderOfService(self)

        self.goblank = wx.RadioButton(self, label="Blank Screen",
                style=wx.RB_GROUP)
        self.golive = wx.RadioButton(self, label="Go Live")

        blankersizer = wx.BoxSizer(wx.HORIZONTAL)
        blankersizer.AddStretchSpacer()
        blankersizer.Add(self.goblank, 0, wx.RIGHT|wx.ALIGN_CENTER, 10)
        blankersizer.Add(self.golive, 0, wx.ALIGN_CENTER)
        blankersizer.AddStretchSpacer()

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(oospanel, 1, wx.GROW|wx.BOTTOM, 10)
        mainsizer.Add(blankersizer, 0, wx.GROW)

        self.SetSizer(mainsizer)

# vim: autoindent shiftwidth=4 expandtab textwidth=80
