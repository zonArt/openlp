# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
Provide the theme XML and handling functions for OpenLP v2 themes.
"""
import os
import re

from xml.dom.minidom import Document
from xml.etree.ElementTree import ElementTree, XML

from openlp.core.lib import str_to_bool

BLANK_THEME_XML = \
'''<?xml version="1.0" encoding="utf-8"?>
 <theme version="1.0">
   <name>BlankStyle</name>
   <background mode="transparent"/>
   <background type="solid" mode="opaque">
      <color>#000000</color>
   </background>
   <background type="gradient" mode="opaque">
      <startColor>#000000</startColor>
      <endColor>#000000</endColor>
      <direction>vertical</direction>
   </background>
   <background type="image" mode="opaque">
      <filename></filename>
   </background>
   <font type="main">
      <name>Arial</name>
      <color>#000000</color>
      <proportion>30</proportion>
      <weight>Normal</weight>
      <italics>False</italics>
      <line_adjustment>0</line_adjustment>
      <location override="False" x="10" y="10" width="1004" height="690"/>
   </font>
   <font type="footer">
      <name>Arial</name>
      <color>#000000</color>
      <proportion>12</proportion>
      <weight>Normal</weight>
      <italics>False</italics>
      <line_adjustment>0</line_adjustment>
      <location override="False" x="10" y="690" width="1004" height="78"/>
   </font>
   <display>
      <shadow color="#000000" size="5">True</shadow>
      <outline color="#000000" size="2">False</outline>
      <horizontalAlign>0</horizontalAlign>
      <verticalAlign>0</verticalAlign>
      <wrapStyle>0</wrapStyle>
      <slideTransition>False</slideTransition>
   </display>
 </theme>
'''

class ThemeLevel(object):
    """
    Provides an enumeration for the level a theme applies to
    """
    Global = 1
    Service = 2
    Song = 3

boolean_list = [u'font_main_italics', u'font_main_override', \
u'font_footer_italics', u'font_footer_override',  u'display_outline', \
u'display_shadow', u'display_slide_transition']

integer_list =[u'font_main_proportion', u'font_main_line_adjustment', \
u'font_main_x', u'font_main_height', u'font_main_y', u'font_main_width', \
u'font_footer_proportion', u'font_footer_line_adjustment', u'font_footer_x', \
u'font_footer_height', u'font_footer_y', u'font_footer_width', \
u'display_shadow_size', u'display_outline_size', u'display_horizontal_align',\
u'display_vertical_align', u'display_wrap_style' ]

class ThemeXML(object):
    """
    A class to encapsulate the Theme XML.
    """
    def __init__(self):
        """
        Initialise the theme object.
        """
        # Create the minidom document
        self.theme_xml = Document()

    def extend_image_filename(self, path):
        """
        Add the path name to the image name so the background can be rendered.

        ``path``
            The path name to be added.
        """
        if self.background_filename and path:
            self.theme_name = self.theme_name.strip()
            self.background_filename = self.background_filename.strip()
            self.background_filename = os.path.join(path, self.theme_name,
                self.background_filename)

    def new_document(self, name):
        """
        Create a new theme XML document.
        """
        self.theme = self.theme_xml.createElement(u'theme')
        self.theme_xml.appendChild(self.theme)
        self.theme.setAttribute(u'version', u'1.0')
        self.name = self.theme_xml.createElement(u'name')
        text_node = self.theme_xml.createTextNode(name)
        self.name.appendChild(text_node)
        self.theme.appendChild(self.name)

    def add_background_transparent(self):
        """
        Add a transparent background.
        """
        background = self.theme_xml.createElement(u'background')
        background.setAttribute(u'mode', u'transparent')
        self.theme.appendChild(background)

    def add_background_solid(self, bkcolor):
        """
        Add a Solid background.

        ``bkcolor``
            The color of the background.
        """
        background = self.theme_xml.createElement(u'background')
        background.setAttribute(u'mode', u'opaque')
        background.setAttribute(u'type', u'solid')
        self.theme.appendChild(background)
        self.child_element(background, u'color', bkcolor)

    def add_background_gradient(self, startcolor, endcolor, direction):
        """
        Add a gradient background.

        ``startcolor``
            The gradient's starting colour.

        ``endcolor``
            The gradient's ending colour.

        ``direction``
            The direction of the gradient.
        """
        background = self.theme_xml.createElement(u'background')
        background.setAttribute(u'mode', u'opaque')
        background.setAttribute(u'type', u'gradient')
        self.theme.appendChild(background)
        # Create startColor element
        self.child_element(background, u'startColor', startcolor)
        # Create endColor element
        self.child_element(background, u'endColor', endcolor)
        # Create direction element
        self.child_element(background, u'direction', direction)

    def add_background_image(self, filename):
        """
        Add a image background.

        ``filename``
            The file name of the image.
        """
        background = self.theme_xml.createElement(u'background')
        background.setAttribute(u'mode', u'opaque')
        background.setAttribute(u'type', u'image')
        self.theme.appendChild(background)
        #Create Filename element
        self.child_element(background, u'filename', filename)

    def add_font(self, name, color, proportion, override, fonttype=u'main',
        weight=u'Normal', italics=u'False', line_adjustment=0,
        xpos=0, ypos=0, width=0, height=0):
        """
        Add a Font.

        ``name``
            The name of the font.

        ``color``
            The colour of the font.

        ``proportion``
            The size of the font.

        ``override``
            Whether or not to override the default positioning of the theme.

        ``fonttype``
            The type of font, ``main`` or ``footer``. Defaults to ``main``.

        ``weight``
            The weight of then font Defaults to 50 Normal

        ``italics``
            Does the font render to italics Defaults to 0 Normal

        ``xpos``
            The X position of the text block.

        ``ypos``
            The Y position of the text block.

        ``width``
            The width of the text block.

        ``height``
            The height of the text block.
        """
        background = self.theme_xml.createElement(u'font')
        background.setAttribute(u'type', fonttype)
        self.theme.appendChild(background)
        #Create Font name element
        self.child_element(background, u'name', name)
        #Create Font color element
        self.child_element(background, u'color', color)
        #Create Proportion name element
        self.child_element(background, u'proportion', proportion)
        #Create weight name element
        self.child_element(background, u'weight', weight)
        #Create italics name element
        self.child_element(background, u'italics', italics)
        #Create indentation name element
        self.child_element(
            background, u'line_adjustment', unicode(line_adjustment))

        #Create Location element
        element = self.theme_xml.createElement(u'location')
        element.setAttribute(u'override', override)
        if override == u'True':
            element.setAttribute(u'x', xpos)
            element.setAttribute(u'y', ypos)
            element.setAttribute(u'width', width)
            element.setAttribute(u'height', height)
        background.appendChild(element)

    def add_display(self, shadow, shadow_color, outline, outline_color,
        horizontal, vertical, wrap, transition, shadow_pixel=5,
        outline_pixel=2):
        """
        Add a Display options.

        ``shadow``
            Whether or not to show a shadow.

        ``shadow_color``
            The colour of the shadow.

        ``outline``
            Whether or not to show an outline.

        ``outline_color``
            The colour of the outline.

        ``horizontal``
            The horizontal alignment of the text.

        ``vertical``
            The vertical alignment of the text.

        ``wrap``
            Wrap style.

        ``transition``
            Whether the slide transition is active.

        """
        background = self.theme_xml.createElement(u'display')
        self.theme.appendChild(background)
        # Shadow
        element = self.theme_xml.createElement(u'shadow')
        element.setAttribute(u'color', shadow_color)
        element.setAttribute(u'size', unicode(shadow_pixel))
        value = self.theme_xml.createTextNode(shadow)
        element.appendChild(value)
        background.appendChild(element)
        # Outline
        element = self.theme_xml.createElement(u'outline')
        element.setAttribute(u'color', outline_color)
        element.setAttribute(u'size', unicode(outline_pixel))
        value = self.theme_xml.createTextNode(outline)
        element.appendChild(value)
        background.appendChild(element)
        # Horizontal alignment
        element = self.theme_xml.createElement(u'horizontalAlign')
        value = self.theme_xml.createTextNode(horizontal)
        element.appendChild(value)
        background.appendChild(element)
        # Vertical alignment
        element = self.theme_xml.createElement(u'verticalAlign')
        value = self.theme_xml.createTextNode(vertical)
        element.appendChild(value)
        background.appendChild(element)
        # Wrap style
        element = self.theme_xml.createElement(u'wrapStyle')
        value = self.theme_xml.createTextNode(wrap)
        element.appendChild(value)
        background.appendChild(element)
        # Slide Transition
        element = self.theme_xml.createElement(u'slideTransition')
        value = self.theme_xml.createTextNode(transition)
        element.appendChild(value)
        background.appendChild(element)

    def child_element(self, element, tag, value):
        """
        Generic child element creator.
        """
        child = self.theme_xml.createElement(tag)
        child.appendChild(self.theme_xml.createTextNode(value))
        element.appendChild(child)
        return child

    def dump_xml(self):
        """
        Dump the XML to file.
        """
        # Debugging aid to see what we have
        return self.theme_xml.toprettyxml(indent=u'  ')

    def extract_xml(self):
        """
        Pull out the XML string.
        """
        # Print our newly created XML
        return self.theme_xml.toxml(u'utf-8').decode(u'utf-8')

    def extract_formatted_xml(self):
        """
        Pull out the XML string formatted for human consumption
        """
        return self.theme_xml.toprettyxml(indent=u'    ', newl=u'\n',
            encoding=u'utf-8')

    def parse(self, xml):
        """
        Read in an XML string and parse it.

        ``xml``
            The XML string to parse.
        """
        self.parse_xml(BLANK_THEME_XML)
        self.parse_xml(xml)

    def parse_xml(self, xml):
        """
        Parse an XML string.

        ``xml``
            The XML string to parse.
        """
        theme_xml = ElementTree(element=XML(xml.encode(u'ascii',
            u'xmlcharrefreplace')))
        xml_iter = theme_xml.getiterator()
        master = u''
        for element in xml_iter:
            if not isinstance(element.text, unicode):
                element.text = unicode(str(element.text), u'utf-8')
            if element.getchildren():
                master = element.tag + u'_'
            else:
                # background transparent tags have no children so special case
                if element.tag == u'background':
                    for e in element.attrib.iteritems():
                        self._create_attr(element.tag + u'_' + e[0], e[1])
            if element.attrib:
                for e in element.attrib.iteritems():
                    if master == u'font_' and e[0] == u'type':
                        master += e[1] + u'_'
                    elif master == u'display_' and (element.tag == u'shadow' \
                        or element.tag == u'outline' ):
                        et = str_to_bool(element.text)
                        self._create_attr(master + element.tag, et)
                        self._create_attr(master + element.tag + u'_'+ e[0], e[1])
                    else:
                        field = master + e[0]
                        self._create_attr(field, e[1])
            else:
                if element.tag:
                    field = master + element.tag
                    element.text = element.text.strip().lstrip()
                    self._create_attr(field, element.text)

    def _create_attr(self, element, value):
        field = self._de_hump(element)
        if field in boolean_list:
            setattr(self, field, str_to_bool(value))
        elif field in integer_list:
            setattr(self, field, int(value))
        else:
            setattr(self, field, unicode(value))

    def __str__(self):
        """
        Return a string representation of this object.
        """
        theme_strings = []
        for key in dir(self):
            if key[0:1] != u'_':
                theme_strings.append(u'%30s: %s' % (key, getattr(self, key)))
        return u'\n'.join(theme_strings)

    def _de_hump(self, name):

        s1 = re.sub(u'(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub(u'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

