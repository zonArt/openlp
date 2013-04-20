# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
OpenLP version 1 theme handling

Provides reference data, a default v1 XML theme and class wrapper for
processing version 1 themes in OpenLP version 2.
"""

from xml.etree.ElementTree import ElementTree, XML
from PyQt4 import QtGui

DELPHI_COLORS = {
    u'clAqua': 0x00FFFF,
    u'clBlack': 0x000000,
    u'clBlue': 0x0000FF,
    u'clFuchsia': 0xFF00FF,
    u'clGray': 0x808080,
    u'clGreen': 0x008000,
    u'clLime': 0x00FF00,
    u'clMaroon': 0x800000,
    u'clNavy': 0x000080,
    u'clOlive': 0x808000,
    u'clPurple': 0x800080,
    u'clRed': 0xFF0000,
    u'clSilver': 0xC0C0C0,
    u'clTeal': 0x008080,
    u'clWhite': 0xFFFFFF,
    u'clYellow': 0xFFFF00
}

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
    """
    Provide a class wrapper storing data from an XML theme

    ``name``
        Theme name

    ``BackgroundMode``
        The behaviour of the background. Valid modes are:

            * ``0`` - Transparent
            * ``1`` - Opaque

    ``BackgroundType``
        The content of the background. Valid types are:

            * ``0`` - solid color
            * ``1`` - gradient color
            * ``2`` - image

    ``BackgroundParameter1``
        Extra information about the background. The contents of this attribute
        depend on the BackgroundType:

            * ``image`` - image filename
            * ``gradient`` - start color
            * ``solid`` - color

    ``BackgroundParameter2``
        Extra information about the background. The contents of this attribute
        depend on the BackgroundType:

            * ``image`` - border color
            * ``gradient`` - end color
            * ``solid`` - N/A

    ``BackgroundParameter3``
        Extra information about the background. The contents of this attribute
        depend on the BackgroundType:

            * ``image`` - N/A
            * ``gradient`` - The direction of the gradient. Valid entries are:

                * ``0`` - vertical
                * ``1`` - horizontal

            * ``solid`` - N/A

    ``FontName``
        Name of the font to use for the main font.

    ``FontColor``
        The color for the main font

    ``FontProportion``
        The size of the main font

    ``FontUnits``
        The units for FontProportion, either <pixels> or <points>

    ``Shadow``
        The shadow type to apply to the main font.

            * ``0`` - no shadow
            * non-zero - use shadow

    ``ShadowColor``
        Color for the shadow

    ``Outline``
        The outline to apply to the main font

            * ``0`` - no outline
            * non-zero - use outline

    ``OutlineColor``
        Color for the outline (or None if Outline is 0)

    ``HorizontalAlign``
        The horizontal alignment to apply to text. Valid alignments are:

            * ``0`` - left align
            * ``1`` - right align
            * ``2`` - centre align

    ``VerticalAlign``
        The vertical alignment to apply to the text. Valid alignments are:

            * ``0`` - top align
            * ``1`` - bottom align
            * ``2`` - centre align

    ``WrapStyle``
        The wrap style to apply to the text. Valid styles are:

            * ``0`` - normal
            * ``1`` - lyrics
    """

    def __init__(self, xml):
        """
        Initialise a theme with data from xml

        ``xml``
            The data to initialise the theme with
        """
        # init to defaults
        self._set_from_xml(BLANK_STYLE_XML)
        self._set_from_xml(xml)

    def _get_as_string(self):
        """
        Return single line string representation of a theme
        """
        theme_strings = []
        keys = dir(self)
        keys.sort()
        for key in keys:
            if key[0:1] != u'_':
                theme_strings.append(u'_%s_' % (getattr(self, key)))
        return u''.join(theme_strings)

    def _set_from_xml(self, xml):
        """
        Set theme class attributes with data from XML

        ``xml``
            The data to apply to the theme
        """
        root = ElementTree(element=XML(xml.encode(u'ascii', u'xmlcharrefreplace')))
        xml_iter = root.getiterator()
        for element in xml_iter:
            delphi_color_change = False
            if element.tag != u'Theme':
                element_text = element.text
                val = 0
                if element_text is None:
                    val = element_text
                # strings need special handling to sort the colours out
                if isinstance(element_text, basestring):
                    if element_text[0] == u'$':
                        # might be a hex number
                        try:
                            val = int(element_text[1:], 16)
                        except ValueError:
                            # nope
                            pass
                    elif element_text in DELPHI_COLORS:
                        val = DELPHI_COLORS[element_text]
                        delphi_color_change = True
                    else:
                        try:
                            val = int(element_text)
                        except ValueError:
                            val = element_text
                if (element.tag.find(u'Color') > 0 or (element.tag.find(u'BackgroundParameter') == 0 and
                    isinstance(val, int))):
                    # convert to a wx.Colour
                    if not delphi_color_change:
                        val = QtGui.QColor(val & 0xFF, (val >> 8) & 0xFF, (val >> 16) & 0xFF)
                    else:
                        val = QtGui.QColor((val >> 16) & 0xFF, (val >> 8) & 0xFF, val & 0xFF)
                setattr(self, element.tag, val)

    def __str__(self):
        """
        Provide Python string representation for the class (multiline output)
        """
        theme_strings = []
        for key in dir(self):
            if key[0:1] != u'_':
                theme_strings.append(u'%30s : %s' % (key, getattr(self, key)))
        return u'\n'.join(theme_strings)
