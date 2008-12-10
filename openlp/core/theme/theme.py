# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""


import sys
import os
from PyQt4 import QtGui
sys.path.append(os.path.abspath("./../.."))

from openlp.core.lib import XmlRootClass

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
  <WrapStyle>0</WrapStyle>
</Theme>
'''

DelphiColors={"clRed":0xFF0000,
               "clBlack":0x000000,
               "clWhite":0xFFFFFF}

class Theme(XmlRootClass):
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
        self._setFromXml(blankstylexml, 'Theme')
        if xmlfile != None:
            # init from xmlfile
            file=open(xmlfile)
            t=''.join(file.readlines()) # read the file and change list to a string
            self._setFromXml(t, 'Theme')

    def post_tag_hook(self, tag, val):
        if DelphiColors.has_key(val):
            val=DelphiColors[val]
        if (tag.find("Color") > 0 or
            (tag.find("BackgroundParameter") == 0 and type(val) == type(0))):
            # convert to a QtGui.Color
            val= QtGui.QColor((val>>16) & 0xFF, (val>>8)&0xFF, val&0xFF)

        return (tag, val)
