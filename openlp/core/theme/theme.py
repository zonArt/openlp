# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import types

from xml.etree.ElementTree import ElementTree, XML
from PyQt4 import QtGui

DELPHI_COLORS = {"clRed":0xFF0000,
                 "clBlue":0x0000FF,
                 "clYellow":0xFFFF00,
                 "clBlack":0x000000,
                 "clWhite":0xFFFFFF}

BLANK_STYLE_XML = \
'''<?xml version="1.0" encoding="iso-8859-1"?>
<Theme>
  <Name>BlankStyle</Name>
  <BackgroundMode>1</BackgroundMode>
  <BackgroundType>0</BackgroundType>
  <BackgroundParameter1>$000000</BackgroundParameter1>
  <BackgroundParameter2/>
  <BackgroundParameter3/>
  <FontName>Arial</FontName>
  <FontColor>clWhite</FontColor>
  <FontProportion>30</FontProportion>
  <FontUnits>pixels</FontUnits>
  <Shadow>0</Shadow>
  <Outline>0</Outline>
  <HorizontalAlign>0</HorizontalAlign>
  <VerticalAlign>0</VerticalAlign>
  <WrapStyle>0</WrapStyle>
</Theme>
'''

class Theme(object):
    def __init__(self, xml):
        """ stores the info about a theme
        attributes:
          name : theme name

           BackgroundMode   : 1 - Transparent
                             1 - Opaque

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
          FontProportion : size of font
          FontUnits      : whether size of font is in <pixels> or <points>

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
        self._set_from_XML(BLANK_STYLE_XML)
        self._set_from_XML(xml)

    def _get_as_string(self):
        theme_strings = []
        keys = dir(self)
        keys.sort()
        for key in keys:
            if key[0:1] != u'_':
                theme_strings.append(u'_%s_' % (getattr(self, key)))
        return u''.join(theme_strings)

    def _set_from_XML(self, xml):
        root = ElementTree(element=XML(xml))
        iter = root.getiterator()
        for element in iter:
            delphiColorChange = False
            if element.tag != u'Theme':
                element_text = element.text
                val = 0
                # easy!
                if element_text is None:
                    val = element_text
                # strings need special handling to sort the colours out
                if type(element_text) is types.StringType or \
                    type(element_text) is types.UnicodeType:
                    if element_text[0] == u'$': # might be a hex number
                        try:
                            val = int(element_text[1:], 16)
                        except ValueError: # nope
                            pass
                    elif DELPHI_COLORS.has_key(element_text):
                        val = DELPHI_COLORS[element_text]
                        delphiColorChange = True
                    else:
                        try:
                            val = int(element_text)
                        except ValueError:
                            val = element_text
                if (element.tag.find(u'Color') > 0 or
                    (element.tag.find(u'BackgroundParameter') == 0 and
                    type(val) == type(0))):
                    # convert to a wx.Colour
                    if not delphiColorChange:
                        val = QtGui.QColor(
                            val&0xFF, (val>>8)&0xFF, (val>>16)&0xFF)
                    else:
                        val = QtGui.QColor(
                            (val>>16)&0xFF, (val>>8)&0xFF, val&0xFF)
                setattr(self, element.tag, val)

    def __str__(self):
        theme_strings = []
        for key in dir(self):
            if key[0:1] != u'_':
                theme_strings.append(u'%30s : %s' % (key, getattr(self, key)))
        return u'\n'.join(theme_strings)
