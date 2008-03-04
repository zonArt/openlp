#!/usr/bin/env pythonw

"""

Entry point for OpenLP wx.App

"""

import wx

import mainframe


class OpenLP(wx.PySimpleApp):
    def OnInit(self):
        frame = mainframe.MainFrame(None, title="openlp.org")
        frame.Show()

        import sys
        for f in sys.argv[1:]:
            self.OpenFileMessage(f)

        return True;


    def OpenFileMessage(self, filename):

        # TODO: OOS loading here
        #       rename function, too

        dlg = wx.MessageDialog(None,
                    "This app was just asked to open:\n%s\n"%filename,
                    "File Opened", wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    app = OpenLP()
    app.MainLoop()

# vim: autoindent shiftwidth=4 expandtab textwidth=80
