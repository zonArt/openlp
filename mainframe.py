"""

wx.Frame for the main OpenLP.org window

"""

import wx

import mainpanel

class MainFrame(wx.Frame):
    "Main OpenLP.org frame"

    def __init__(self, *args, **kwargs):
        "MainFrame constructor"

        wx.Frame.__init__(self, *args, **kwargs)

        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()

        item = FileMenu.Append(wx.ID_EXIT, text = "&Exit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)

        item = FileMenu.Append(wx.ID_ANY, text = "&Open")
        self.Bind(wx.EVT_MENU, self.OnOpen, item)

        item = FileMenu.Append(wx.ID_PREFERENCES, text = "&Preferences")
        self.Bind(wx.EVT_MENU, self.OnPrefs, item)

        MenuBar.Append(FileMenu, "&File")

        HelpMenu = wx.Menu()

        item = HelpMenu.Append(wx.ID_HELP, "OpenLP.org &Help")
        self.Bind(wx.EVT_MENU, self.OnHelp, item)

        # This gets put in the App menu on OS X
        item = HelpMenu.Append(wx.ID_ABOUT, "&About")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)

        MenuBar.Append(HelpMenu, "&Help")

        self.SetMenuBar(MenuBar)

        self.Panel = mainpanel.MainPanel(self)

        self.Fit()


    def OnQuit(self,Event):
        self.Destroy()


    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This is a small program to test\n"
                "the use of menus on Mac, etc.\n",
                "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def OnHelp(self, event):
        dlg = wx.MessageDialog(self, "This would be help\n"
                "If there was any\n", "Test Help", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def OnOpen(self, event):
        dlg = wx.MessageDialog(self, "This would be an open Dialog\n"
                "If there was anything to open\n", "Open File",
                wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def OnPrefs(self, event):
        dlg = wx.MessageDialog(self, "This would be an preferences Dialog\n"
                "If there were any preferences to set.\n",
                "Preferences", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

# vim: autoindent shiftwidth=4 expandtab textwidth=80
