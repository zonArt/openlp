"""

Order of Service panel

"""

# TODO: change this from a list box to our own custom widget to allow the
# traditional OpenLP OOS entry with an icon

import wx

class OrderOfService(wx.Panel):
    "Order Of Service Panel"

    def __init__(self, parent, *args, **kwargs):
        "Panel constructor"

        wx.Panel.__init__(self, parent, *args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.list = wx.ListBox(self, size=wx.Size(180, 250))

        self.list.Append("foo")

        sizer.Add(self.list, 1)
        #sizer.Add(self.list, 1, wx.GROW)

        self.SetSizer(sizer)

# vim: autoindent shiftwidth=4 expandtab textwidth=80
