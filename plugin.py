"""

Custom classes for plugins

"""

import wx

# OOSItem should be extended into a plugin-specific object that encapsulates
# the data needed for that plugin to reference back to its internal data
# (like the songid or the path to a video file)
class OOSItem:
    "'Order of Service' entry item"

    def __init__(self):
        "OOSItem constructor"

        self.title = "Scaffold item"

    def gettitle(self):
        "Accessor for title"

        return self.title

    def golive(self, window):
        "Display this item onscreen"
        pass

    def blank(self, window):  
        "Blank the screen, plugin is allowed to keep data ready"
        pass

    def stop(self, window):
        "Stop this plugin and destroy any canvases"
        pass


# OLPPlugin describes a base class which will be extended by the each particular
# plugin.  The plugin provides a series of objects to the host application:
#  * panel to add to the control interface (class Controller)
#  * operations for `go live', `[un]blank', `stop'
class OLPPlugin(wx.Panel):
    "Plugin type"

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
