from elementtree.ElementTree import ElementTree, XML
import wx
DelphiColors={"clRed":0xFF0000,
               "clBlack":0x000000,
               "clWhite":0xFFFFFF}

blankstylexml=\
'''<?xml version="1.0" encoding="iso-8859-1"?>
<Theme>
  <Name>BlankStyle</Name>
  <BackgroundType>0</BackgroundType>
  <BackgroundParameter1>$000000</BackgroundParameter1>
  <BackgroundParameter2/>
  <BackgroundParameter3/>
  <FontName>Arial</FontName>
  <FontColor>clWhite</FontColor>
  <FontProportion>30</FontProportion>
  <Shadow>0</Shadow>
  <Outline>0</Outline>
  <HorizontalAlign>0</HorizontalAlign>
  <VerticalAlign>0</VerticalAlign>
  
</Theme>
'''

class Theme:
    def __init__(self, xmlfile=None):
        """ stores the info about a theme
        attributes:
          name : theme name
          
          BackgroundType   : 0 - solid color
                             1 - gradient color
                             2 - image

          BackgroundParameter1 : for image - filename
                                 for gradient - start color
                                 for solid - color
          BackgroundParameter2 : for image - border colour
                                 for gradient - end color
                                 for solid - N/A
          BackgroundParameter3 : for image - N/A
                                 for gradient - 0 -> vertical, 1 -> horizontal
                             
          FontName       : name of font to use
          FontColor      : color for main font
          FontProportion : point size of font

          Shadow       : 0 - no shadow, non-zero use shadow
          ShadowColor  : color for drop shadow
          Outline      : 0 - no outline, non-zero use outline
          OutlineColor : color for outline (or None for no outline)

          HorizontalAlign : 0 - left align
                            1 - right align
                            2 - centre align
          VerticalAlign   : 0 - top align
                            1 - bottom align
                            2 - centre align
          WrapStyle       : 0 - normal
                            1 - lyrics
        """
        # init to defaults
        self._set_from_XML(blankstylexml)
        if xmlfile != None:
            # init from xmlfile
            file=open(xmlfile)
            t=''.join(file.readlines()) # read the file and change list to a string
            self._set_from_XML(t)

    def get_as_string(self):
        s=""
        keys=dir(self)
        keys.sort()
        for k in keys:
            if k[0:1] != "_":
                s+= "_%s_" %(getattr(self,k))
        return s
    def _set_from_XML(self, xml):
        root=ElementTree(element=XML(xml))
        iter=root.getiterator()
        for element in iter:
            if element.tag != "Theme":
                t=element.text
#                 print element.tag, t, type(t)
                if type(t) == type(None): # easy!
                    val=t
                if type(t) == type(" "): # strings need special handling to sort the colours out
#                    print "str",
                    if t[0] == "$": # might be a hex number
#                        print "hex",
                        try:
                            val=int(t[1:], 16)
                        except ValueError: # nope
#                            print "nope",
                            pass
                    elif DelphiColors.has_key(t):
#                        print "colour", 
                        val=DelphiColors[t]
                    else:
#                        print "last chance",
                        try:
                            val=int(t)
#                            print "int", 
                        except ValueError:
#                            print "give up",
                            val=t
                if (element.tag.find("Color") > 0 or
                    (element.tag.find("BackgroundParameter") == 0 and type(val) == type(0))):
                    # convert to a wx.Colour
                    val= wx.Colour((val>>16) & 0xFF, (val>>8)&0xFF, val&0xFF)
 #               print [val]
                setattr(self,element.tag, val)
        

    def __str__(self):
        s=""
        for k in dir(self):
            if k[0:1] != "_":
                s+= "%30s : %s\n" %(k,getattr(self,k))
        return s

if __name__=="__main__":
    test_theme.test_read_theme()
