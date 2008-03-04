"""

The openlp.org Control Panel

"""

import wx

from openlp.controls import slidepanel

class ControlPanel(wx.Window):
    
    Title = ""
    Heading1 = ""
    Heading2 = ""
    Loaded = False;
    
    def __init__(self, parent, title, *args, **kwargs):
        
        wx.Window.__init__(self, parent, *args, **kwargs)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        MainSizer.AddSpacer(60)
        
        self.Title = title
        
        self.SlidePanel = slidepanel.SlidePanel(self)
        
        MainSizer.Add(self.SlidePanel, flag=wx.EXPAND)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.SetSizer(MainSizer)
        self.SetAutoLayout(True)
        self.Layout()
        
    def OnPaint(self, event):
        
        DC = wx.PaintDC(self)
        DC.SetFont(wx.Font(pointSize=16, family=wx.FONTFAMILY_MODERN, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD,underline=False,face="Tahoma"))
        DC.DrawText(text=self.Title,x=(self.GetSize().GetWidth()-DC.GetTextExtent(self.Title)[0])/2,y=0)
        
        y = DC.GetTextExtent(self.Title)[1]
        DC.SetFont(wx.Font(pointSize=12, family=wx.FONTFAMILY_MODERN, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD,underline=False,face="Tahoma"))
        DC.SetBrush(wx.Brush(wx.Colour(55,102,255)))
        DC.SetPen(wx.Pen(wx.Colour(55,102,255)))
        
        fontHeight = DC.GetTextExtent("by")[1]
        DC.DrawRectangle(0,y,self.GetSize().GetWidth(),fontHeight);
        DC.SetTextForeground(wx.Colour(255,255,255))
        
        if self.Heading1 == "":
            DC.DrawText("No media item loaded",5,y)
        else:
            DC.DrawText(self.Heading1,5,y)
            
        DC.SetFont(wx.Font(pointSize=10, family=wx.FONTFAMILY_MODERN, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL,underline=False,face="Tahoma"))
        DC.DrawRectangle(0,fontHeight+y,self.GetSize().GetWidth(),fontHeight)
        DC.DrawText(self.Heading2,5,fontHeight+y)
        self.SlidePanel.Refresh()        
    
    def OnSize(self, event):
        self.Layout()