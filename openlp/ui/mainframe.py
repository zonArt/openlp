"""

wx.Frame for the main OpenLP.org window

"""

import wx
from openlp.controls import controlpanel
from openlp.controls import canvas
from openlp.controls import mediamanager

class MainFrame(wx.Frame):
    "Main OpenLP.org frame"

    def __init__(self, *args, **kwargs):
        "MainFrame constructor"

        wx.Frame.__init__(self, *args, **kwargs)

        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()
        
        MenuBar.Append(FileMenu, "&File")

        self.SetMenuBar(MenuBar)
		
        self.MainSplitter = wx.SplitterWindow(self, size=self.GetClientSize(), style=wx.SP_3D)
        self.PreviewSplitter = wx.SplitterWindow(self.MainSplitter, size=self.MainSplitter.GetClientSize(), style=wx.SP_3D)
        self.LiveSplitter = wx.SplitterWindow(self.MainSplitter, size=self.MainSplitter.GetClientSize(), style=wx.SP_3D)
        LiveControlPanel = controlpanel.ControlPanel(self.LiveSplitter,title="Live")
        PreviewControlPanel = controlpanel.ControlPanel(self.PreviewSplitter,title="Preview")
        LiveCanvas = canvas.Canvas(self.LiveSplitter)
        PreviewCanvas = canvas.Canvas(self.PreviewSplitter)

        self.MainSplitter.SplitVertically(self.PreviewSplitter, self.LiveSplitter)
        self.LiveSplitter.SplitHorizontally(LiveControlPanel,LiveCanvas)
        self.PreviewSplitter.SplitHorizontally(PreviewControlPanel,PreviewCanvas)
        
        self.MainSplitter.SetMinimumPaneSize(200)
        self.LiveSplitter.SetMinimumPaneSize(200)
        self.PreviewSplitter.SetMinimumPaneSize(200)

        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        MediaManager = mediamanager.MediaManager(self, size=wx.Size(200,200))
        OrderOfServiceFrame = wx.Panel(self, size=wx.Size(200,200))
        
        self.SetSizer(MainSizer)
        
        MainSizer.Add(MediaManager, flag=wx.EXPAND)
        MainSizer.Add(self.MainSplitter, proportion=1, flag=wx.EXPAND)
        MainSizer.Add(OrderOfServiceFrame, flag=wx.EXPAND)
        
        self.CreateStatusBar(1)
        self.SetStatusText("openlp.org")
        
        MainSizer.SetSizeHints(self)

        self.SetAutoLayout(True)
        
        self.Layout()
        
        self.MainSplitter.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.MainSplitterOnChanged)
        self.LiveSplitter.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.LiveSplitterOnChanged)
        self.PreviewSplitter.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.PreviewSplitterOnChanged)
        self.Bind(wx.EVT_SIZE, self.OnSize)
               
    def MainSplitterOnChanged(self,event):
        self.MainSplitter.SetSashPosition(self.MainSplitter.GetClientSize().GetWidth()/2,True)
    
    def LiveSplitterOnChanged(self,event):
        
        WindowList = self.LiveSplitter.GetChildren()
        
        for Node in WindowList:
            Node.Refresh()
    
    def PreviewSplitterOnChanged(self,event):
        
        WindowList = self.PreviewSplitter.GetChildren()
        
        for Node in WindowList:
            Node.Refresh()
            
    def OnSize(self,event):
        
        self.Layout()
        
        self.MainSplitterOnChanged(event)
        self.LiveSplitterOnChanged(event)
        self.PreviewSplitterOnChanged(event)