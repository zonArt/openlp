import wx

class Slide(wx.Window):

    SlideNum = 0
    Selected = False
    SlideText = ""
    SlideType = ""
    
    def __init__(self, parent, slideText, slideNum, slideType, *args, **kwargs):
        wx.Window.__init__(self, parent, *args, **kwargs)
        
        self.SlideText = slideText
        self.SlideNum = slideNum
        self.SlideType = slideType
        
        self.Bind(wx.EVT_MOUSEDOWN, self.OnMouseDown)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def GetHeight(self):
        DC = wx.ClientDC(self)
        
        DC.SetFont(wx.Font(pointSize=8, family=wx.FONTFAMILY_MODERN, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL,underline=False,face="Tahoma"))
        FontHeight = DC.GetTextExtent("by")[1]
        Tokenizer = wx.StringTokenizer(self.SlideText,"\n")
        ArrayString = wx.ArrayString()
        
        while Tokenizer.HasMoreTokens():
            Token = Tokenizer.GetNextToken()
            ArrayString.Add(Token)
            
        return FontHeight*(ArrayString.Count()+1)
        
    def GetIndex(self):
        return self.SlideNum
    
    def SetSelected(self):
        if not self.Selected:
            self.Selected = True
            Refresh()
            
    def DropSelected(self):
        if self.Selected:
            self.Selected = False
            Refresh()
    
    def OnPaint(self, event):
        DC = wx.PaintDC(self)
        DC.SetFont(wx.Font(pointSize=9, family=wx.FONTFAMILY_MODERN, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL,underline=False,face="Tahoma"))
        if self.Selected:
            Colour = wx.Colour(0,26,102)
        else:
            Colour = wx.Colour(55,102,255)
        DC.SetBrush(wx.Brush(Colour))
        DC.SetPen(wx.Pen(Colour))
        
        FontHeight = DC.GetTextExtent("by")[1]
        DC.DrawRectangle(0,0,self.GetParent().GetSize().GetWidth(),FontHeight)
        DC.SetTextForeground(wx.Colour(255,255,255))
        DC.DrawText(self.SlideType,5,0)
        
        Tokenizer = wx.StringTokenizer(self.SlideText,"\n")
        ArrayString = wx.ArrayString()
        
        while Tokenizer.HasMoreTokens():
            Token = Tokenizer.GetNextToken()
            ArrayString.Add(Token)

        self.SetSize(wx.Size(self.GetParent().GetSize().GetWidth(),FontHeight*(ArrayString.Count()+1)))
        DC.SetBrush(wx.Brush(wx.Colour(255,255,255)))
        DC.SetPen(wx.Pen(wx.Colour(255,255,255)))
        
        DC.DrawRectangle(0,FontHeight,self.GetSize().GetWidth(),self.GetSize().GetHeight()-FontHeight)
        DC.SetTextForeGround(wx.Colour(0,0,0))

        for i in range(0,ArrayString.Count()):
            DC.DrawText(ArrayString.Item(i),5,(i+1)*FontHeight)           
            
    def OnMouseDown(self, event):
        self.GetParent().SetSelected(self.SlideNum)