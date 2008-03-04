import wx

class MediaManager(wx.Window):

    def __init__(self, parent, *args, **kwargs):
        wx.Window.__init__(self, parent, *args, **kwargs)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        MainSizer.AddSpacer(20)
        
        if wx.Platform == "__WXMAC__":
            self.Notebook = wx.Choicebook(self, size=wx.Size(200,200))
        else:
            self.Notebook = wx.Notebook(self, size=wx.Size(200,200))
            
        MainSizer.Add(self.Notebook, proportion=1, flag=wx.EXPAND)
        
        self.SetSizer(MainSizer)
        self.SetAutoLayout(True)
        self.Layout()
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def OnPaint(self, event):
        DC = wx.PaintDC(self)
        DC.SetFont(wx.Font(pointSize=9, family=wx.FONTFAMILY_MODERN, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL,underline=False,face="Tahoma"))
        DC.GradientFillLinear(wx.Rect(1,1,self.GetSize().GetWidth()-2,DC.GetTextExtent("by")[1]+2), wx.Colour(220,220,220), wx.Colour(255,255,255))
        DC.DrawText("Media Manager", 6, 2)
        
    def OnSize(self, event):
        self.Layout()