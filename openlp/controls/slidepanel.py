import wx

from openlp.controls import slide

class SlidePanel(wx.Window):
    
    SlideEnum = 1
    NextY = 0
    
    def __init__(self, parent, *args, **kwargs):
        
        wx.Window.__init__(self, parent, *args, **kwargs)
        
    def AddSlide(self, slideText, slideType):
        slide = slide.Slide(self, pos=wx.Point(0,self.NextY+10), slideText=slideText, slideNum=self.SlideEnum, slideType=slideType)
        self.SlideEnum = self.SlideEnum+1
        self.NextY = self.NextY + slide.GetHeight()+10
        self.SetVirtualSize(self.GetSize().GetWidth(),self.NextY)
        self.SetScrollRate(1,1)
        slide.Refresh()
        
    def SetSelected(self, index):
        WindowList = self.GetChildren()
        
        for Node in WindowList:
            Current = Node.GetData()
            if Current.GetIndex() == index:
                Current.SetSelected()
            else:
                Current.DropSelected()