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
import logging

from xml.dom.minidom import Document
from xml.etree.ElementTree import ElementTree, XML
from lxml import etree, objectify

from openlp.core.lib import str_to_bool

log = logging.getLogger(__name__)

BLANK_THEME_XML = \
'''<?xml version="1.0" encoding="utf-8"?>
 <theme version="1.0">
   <name>BlankStyle</name>
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
      <color>#FFFFFF</color>
      <size>30</size>
      <bold>False</bold>
      <italics>False</italics>
      <line_adjustment>0</line_adjustment>
      <shadow shadowColor="#000000" shadowSize="5">True</shadow>
      <outline outlineColor="#000000" outlineSize="2">False</outline>
      <location override="False" x="10" y="10" width="1004" height="690"/>
   </font>
   <font type="footer">
      <name>Arial</name>
      <color>#FFFFFF</color>
      <size>12</size>
      <bold>False</bold>
      <italics>False</italics>
      <shadow shadowColor="#000000" shadowSize="5">True</shadow>
      <outline outlineColor="#000000" outlineSize="2">False</outline>
      <line_adjustment>0</line_adjustment>
      <location override="False" x="10" y="690" width="1004" height="78"/>
   </font>
   <display>
      <horizontalAlign>0</horizontalAlign>
      <verticalAlign>0</verticalAlign>
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

boolean_list = [u'bold', u'italics', u'override', u'outline', u'shadow', \
u'slide_transition']

integer_list =[u'size', u'line_adjustment', u'x', u'height', u'y', \
u'width', u'shadow_size', u'outline_size', u'horizontal_align', \
u'vertical_align']

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
        self.parse_xml(BLANK_THEME_XML)

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
        self.theme.setAttribute(u'version', u'2.0')
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
        # Create Filename element
        self.child_element(background, u'filename', filename)

    def add_font(self, name, color, proportion, override, fonttype=u'main',
        bold=u'False', italics=u'False', line_adjustment=0,
        xpos=0, ypos=0, width=0, height=0 , outline=u'False', outline_color=u'#ffffff',
        outline_pixel=2,  shadow=u'False', shadow_color=u'#ffffff', shadow_pixel=5):
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

        ``outline``
            Whether or not to show an outline.

        ``outline_color``
            The colour of the outline.

        ``outline_size``
            How big the Shadow is

        ``shadow``
            Whether or not to show a shadow.

        ``shadow_color``
            The colour of the shadow.

        ``shadow_size``
            How big the Shadow is


        """
        background = self.theme_xml.createElement(u'font')
        background.setAttribute(u'type', fonttype)
        self.theme.appendChild(background)
        # Create Font name element
        self.child_element(background, u'name', name)
        # Create Font color element
        self.child_element(background, u'color', color)
        # Create Proportion name element
        self.child_element(background, u'size', proportion)
        # Create weight name element
        self.child_element(background, u'bold', bold)
        # Create italics name element
        self.child_element(background, u'italics', italics)
        # Create indentation name element
        self.child_element(
            background, u'line_adjustment', unicode(line_adjustment))
        # Create Location element
        element = self.theme_xml.createElement(u'location')
        element.setAttribute(u'override', override)
        if override == u'True':
            element.setAttribute(u'x', xpos)
            element.setAttribute(u'y', ypos)
            element.setAttribute(u'width', width)
            element.setAttribute(u'height', height)
        background.appendChild(element)
        # Shadow
        element = self.theme_xml.createElement(u'shadow')
        element.setAttribute(u'shadowColor', unicode(shadow_color))
        element.setAttribute(u'shadowSize', unicode(shadow_pixel))
        value = self.theme_xml.createTextNode(unicode(shadow))
        element.appendChild(value)
        background.appendChild(element)
        # Outline
        element = self.theme_xml.createElement(u'outline')
        element.setAttribute(u'outlineColor', unicode(outline_color))
        element.setAttribute(u'outlineSize', unicode(outline_pixel))
        value = self.theme_xml.createTextNode(unicode(outline))
        element.appendChild(value)
        background.appendChild(element)

    def add_display(self, horizontal, vertical, transition):
        """
        Add a Display options.

        ``horizontal``
            The horizontal alignment of the text.

        ``vertical``
            The vertical alignment of the text.

        ``transition``
            Whether the slide transition is active.

        """
        background = self.theme_xml.createElement(u'display')
        self.theme.appendChild(background)
        # Horizontal alignment
        element = self.theme_xml.createElement(u'horizontalAlign')
        value = self.theme_xml.createTextNode(unicode(horizontal))
        element.appendChild(value)
        background.appendChild(element)
        # Vertical alignment
        element = self.theme_xml.createElement(u'verticalAlign')
        value = self.theme_xml.createTextNode(unicode(vertical))
        element.appendChild(value)
        background.appendChild(element)
        # Slide Transition
        element = self.theme_xml.createElement(u'slideTransition')
        value = self.theme_xml.createTextNode(unicode(transition))
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
        Dump the XML to file used for debugging
        """
        return self.theme_xml.toprettyxml(indent=u'  ')

    def extract_xml(self):
        """
        Print out the XML string.
        """
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
        self.parse_xml(unicode(xml))
        print self

    def parse_xml(self, xml):
        """
        Parse an XML string.

        ``xml``
            The XML string to parse.
        """
        # remove encoding string
        line = xml.find(u'?>')
        if line:
            xml = xml[line + 2:]
        try:
           theme_xml = objectify.fromstring(xml)
        except etree.XMLSyntaxError:
            log.exception(u'Invalid xml %s', xml)
            return
        # print objectify.dump(theme_xml)
        xml_iter = theme_xml.getiterator()
        for element in xml_iter:
            parent = element.getparent()
            master = u''
            if parent is not None:
                if element.getparent().tag == u'font':
                    master = element.getparent().tag + u'_' + element.getparent().attrib[u'type']
                # set up Outline and Shadow Tags and move to font_main
                if element.getparent().tag == u'display':
                    self._create_attr(u'font_main', element.tag, element.text)
                    master = element.getparent().tag
                if element.getparent().tag == u'background':
                    master = element.getparent().tag
                    if element.getparent().attrib:
                        for attr in element.getparent().attrib:
                            self._create_attr(master, attr, element.getparent().attrib[attr])
            if master:
                if element.attrib:
                    for attr in element.attrib:
                        base_element = attr
                        # correction for the shadow and outline tags
                        if element.tag == u'shadow' or element.tag == u'outline':
                            if not attr.startswith(element.tag):
                                base_element = element.tag + u'_' + attr
                        self._create_attr(master, base_element,
                            element.attrib[attr])
                else:
                   self._create_attr(master,  element.tag, element.text)
            else:
                if element.tag == u'name':
                    self._create_attr(u'theme',  element.tag, element.text)

    def _translate_tags(self, master, element, value):
        """
        Clean up XML removing and redefining tags
        """
        master = master.strip().lstrip()
        element = element.strip().lstrip()
        value = unicode(value).strip().lstrip()
        print "start", master, element, value
        if master == u'display':
            if element == u'wrapStyle':
                return True, None, None, None
            if element == u'shadow' or element == u'outline':
                master = u'font_main'
        # fix bold font
        if element == u'weight':
            element = u'bold'
            if value == u'Normal':
                value = False
            else:
                value = True
        if element == u'proportion':
            element = u'size'
        print "end", master, element, value
        return False, master, element, value

    def _create_attr(self, master , element, value):
        """
        Create the attributes with the correct data types and name format
        """
        reject, master, element, value = \
            self._translate_tags(master, element, value)
        if reject:
            return
        field = self._de_hump(element)
        tag = master + u'_' + field
        if element in boolean_list:
            setattr(self, tag, str_to_bool(value))
        elif element in integer_list:
            setattr(self, tag, int(value))
        else:
            # make string value unicode
            if not isinstance(value, unicode):
                value = unicode(str(value), u'utf-8')
            setattr(self, tag, unicode(value).strip().lstrip())

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
        """
        Change Camel Case string to python string
        """
        s1 = re.sub(u'(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub(u'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def build_xml_from_attrs(self, ):
        """
        Build the XML from the varables in the object
        """
        if self.background_type == u'solid':
            self.add_background_solid(
                unicode(self.background_color))
        elif self.background_type == u'gradient':
            self.add_background_gradient(
                unicode(self.background_start_color),
                unicode(self.background_end_color),
                self.background_direction)
        else:
            filename = \
                os.path.split(unicode(self.background_filename))[1]
            self.add_background_image(filename)
        self.add_font(unicode(self.font_main_name),
            unicode(self.font_main_color),
            unicode(self.font_main_proportion),
            unicode(self.font_main_override), u'main',
            unicode(self.font_main_weight),
            unicode(self.font_main_italics),
            unicode(self.font_main_line_adjustment),
            unicode(self.font_main_x),
            unicode(self.font_main_y),
            unicode(self.font_main_width),
            unicode(self.font_main_height),
            self.font_main_outline,
            self.font_main_outline_color,
            self.font_main_outline_size,
            self.font_main_shadow,
            self.font_main_shadow_color,
            self.font_main_shadow_size)
        self.add_font(unicode(self.font_footer_name),
            unicode(self.font_footer_color),
            unicode(self.font_footer_proportion),
            unicode(self.font_footer_override), u'footer',
            unicode(self.font_footer_weight),
            unicode(self.font_footer_italics),
            0, # line adjustment
            unicode(self.font_footer_x),
            unicode(self.font_footer_y),
            unicode(self.font_footer_width),
            unicode(self.font_footer_height),
            self.font_footer_outline,
            self.font_footer_outline_color,
            self.font_footer_outline_size,
            self.font_footer_shadow,
            self.font_footer_shadow_color,
            self.font_footer_shadow_size)
        self.add_display(self.display_horizontal_align,
            self.display_vertical_align,
            self.display_slide_transition)
