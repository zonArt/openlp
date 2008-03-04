import wx

class Canvas(wx.Window):
    
    def __init__(self, parent, *args, **kwargs):
        
        wx.Window.__init__(self, parent, *args, **kwargs)
        
        self.SetBackgroundColour(wx.Colour(150,150,150))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, event):
        DC = wx.PaintDC(self)
        if (self.GetSize().GetWidth()*3/4) > self.GetSize().GetHeight():
            Height = self.GetSize().GetHeight()-40
            Width = (Height*4)/3
            
            x = (self.GetSize().GetWidth()-Width)/2
            Rectangle = wx.Rect(x, 20, Width, Height)
        else:
            Width = self.GetSize().GetWidth()-40
            Height = (Width*3)/4
            
            y = (self.GetSize().GetHeight()-Height)/2
            Rectangle = wx.Rect(20, y, Width, Height)
        DC.SetBrush(wx.Brush(wx.Colour(0,0,0)))
        DC.SetPen(wx.Pen(wx.Colour(255,255,255)))

        if self.IsExposedRect(Rectangle):
            DC.DrawRectangleRect(Rectangle)
    