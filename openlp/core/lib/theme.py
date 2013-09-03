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
Provide the theme XML and handling functions for OpenLP v2 themes.
"""
import os
import re
import logging

from xml.dom.minidom import Document
from lxml import etree, objectify

from openlp.core.lib import str_to_bool, ScreenList

log = logging.getLogger(__name__)

BLANK_THEME_XML = \
'''<?xml version="1.0" encoding="utf-8"?>
 <theme version="1.0">
   <name> </name>
   <background type="image">
      <filename></filename>
      <borderColor>#000000</borderColor>
   </background>
   <background type="gradient">
      <startColor>#000000</startColor>
      <endColor>#000000</endColor>
      <direction>vertical</direction>
   </background>
   <background type="solid">
      <color>#000000</color>
   </background>
   <font type="main">
      <name>Arial</name>
      <color>#FFFFFF</color>
      <size>40</size>
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
      <line_adjustment>0</line_adjustment>
      <shadow shadowColor="#000000" shadowSize="5">True</shadow>
      <outline outlineColor="#000000" outlineSize="2">False</outline>
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


class BackgroundType(object):
    """
    Type enumeration for backgrounds.
    """
    Solid = 0
    Gradient = 1
    Image = 2
    Transparent = 3

    @staticmethod
    def to_string(background_type):
        """
        Return a string representation of a background type.
        """
        if background_type == BackgroundType.Solid:
            return 'solid'
        elif background_type == BackgroundType.Gradient:
            return 'gradient'
        elif background_type == BackgroundType.Image:
            return 'image'
        elif background_type == BackgroundType.Transparent:
            return 'transparent'

    @staticmethod
    def from_string(type_string):
        """
        Return a background type for the given string.
        """
        if type_string == 'solid':
            return BackgroundType.Solid
        elif type_string == 'gradient':
            return BackgroundType.Gradient
        elif type_string == 'image':
            return BackgroundType.Image
        elif type_string == 'transparent':
            return BackgroundType.Transparent


class BackgroundGradientType(object):
    """
    Type enumeration for background gradients.
    """
    Horizontal = 0
    Vertical = 1
    Circular = 2
    LeftTop = 3
    LeftBottom = 4

    @staticmethod
    def to_string(gradient_type):
        """
        Return a string representation of a background gradient type.
        """
        if gradient_type == BackgroundGradientType.Horizontal:
            return 'horizontal'
        elif gradient_type == BackgroundGradientType.Vertical:
            return 'vertical'
        elif gradient_type == BackgroundGradientType.Circular:
            return 'circular'
        elif gradient_type == BackgroundGradientType.LeftTop:
            return 'leftTop'
        elif gradient_type == BackgroundGradientType.LeftBottom:
            return 'leftBottom'

    @staticmethod
    def from_string(type_string):
        """
        Return a background gradient type for the given string.
        """
        if type_string == 'horizontal':
            return BackgroundGradientType.Horizontal
        elif type_string == 'vertical':
            return BackgroundGradientType.Vertical
        elif type_string == 'circular':
            return BackgroundGradientType.Circular
        elif type_string == 'leftTop':
            return BackgroundGradientType.LeftTop
        elif type_string == 'leftBottom':
            return BackgroundGradientType.LeftBottom


class HorizontalType(object):
    """
    Type enumeration for horizontal alignment.
    """
    Left = 0
    Right = 1
    Center = 2
    Justify = 3

    Names = ['left', 'right', 'center', 'justify']


class VerticalType(object):
    """
    Type enumeration for vertical alignment.
    """
    Top = 0
    Middle = 1
    Bottom = 2

    Names = ['top', 'middle', 'bottom']


BOOLEAN_LIST = ['bold', 'italics', 'override', 'outline', 'shadow', 'slide_transition']

INTEGER_LIST = ['size', 'line_adjustment', 'x', 'height', 'y', 'width', 'shadow_size', 'outline_size',
    'horizontal_align', 'vertical_align', 'wrap_style']


class ThemeXML(object):
    """
    A class to encapsulate the Theme XML.
    """
    FIRST_CAMEL_REGEX = re.compile('(.)([A-Z][a-z]+)')
    SECOND_CAMEL_REGEX = re.compile('([a-z0-9])([A-Z])')

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
        if self.background_type == 'image':
            if self.background_filename and path:
                self.theme_name = self.theme_name.strip()
                self.background_filename = self.background_filename.strip()
                self.background_filename = os.path.join(path, self.theme_name, self.background_filename)

    def _new_document(self, name):
        """
        Create a new theme XML document.
        """
        self.theme_xml = Document()
        self.theme = self.theme_xml.createElement('theme')
        self.theme_xml.appendChild(self.theme)
        self.theme.setAttribute('version', '2.0')
        self.name = self.theme_xml.createElement('name')
        text_node = self.theme_xml.createTextNode(name)
        self.name.appendChild(text_node)
        self.theme.appendChild(self.name)

    def add_background_transparent(self):
        """
        Add a transparent background.
        """
        background = self.theme_xml.createElement('background')
        background.setAttribute('type', 'transparent')
        self.theme.appendChild(background)

    def add_background_solid(self, bkcolor):
        """
        Add a Solid background.

        ``bkcolor``
            The color of the background.
        """
        background = self.theme_xml.createElement('background')
        background.setAttribute('type', 'solid')
        self.theme.appendChild(background)
        self.child_element(background, 'color', str(bkcolor))

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
        background = self.theme_xml.createElement('background')
        background.setAttribute('type', 'gradient')
        self.theme.appendChild(background)
        # Create startColor element
        self.child_element(background, 'startColor', str(startcolor))
        # Create endColor element
        self.child_element(background, 'endColor', str(endcolor))
        # Create direction element
        self.child_element(background, 'direction', str(direction))

    def add_background_image(self, filename, borderColor):
        """
        Add a image background.

        ``filename``
            The file name of the image.
        """
        background = self.theme_xml.createElement('background')
        background.setAttribute('type', 'image')
        self.theme.appendChild(background)
        # Create Filename element
        self.child_element(background, 'filename', filename)
        # Create endColor element
        self.child_element(background, 'borderColor', str(borderColor))

    def add_font(self, name, color, size, override, fonttype='main', bold='False', italics='False',
        line_adjustment=0, xpos=0, ypos=0, width=0, height=0, outline='False', outline_color='#ffffff',
        outline_pixel=2, shadow='False', shadow_color='#ffffff', shadow_pixel=5):
        """
        Add a Font.

        ``name``
            The name of the font.

        ``color``
            The colour of the font.

        ``size``
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
        background = self.theme_xml.createElement('font')
        background.setAttribute('type', fonttype)
        self.theme.appendChild(background)
        # Create Font name element
        self.child_element(background, 'name', name)
        # Create Font color element
        self.child_element(background, 'color', str(color))
        # Create Proportion name element
        self.child_element(background, 'size', str(size))
        # Create weight name element
        self.child_element(background, 'bold', str(bold))
        # Create italics name element
        self.child_element(background, 'italics', str(italics))
        # Create indentation name element
        self.child_element(background, 'line_adjustment', str(line_adjustment))
        # Create Location element
        element = self.theme_xml.createElement('location')
        element.setAttribute('override', str(override))
        element.setAttribute('x', str(xpos))
        element.setAttribute('y', str(ypos))
        element.setAttribute('width', str(width))
        element.setAttribute('height', str(height))
        background.appendChild(element)
        # Shadow
        element = self.theme_xml.createElement('shadow')
        element.setAttribute('shadowColor', str(shadow_color))
        element.setAttribute('shadowSize', str(shadow_pixel))
        value = self.theme_xml.createTextNode(str(shadow))
        element.appendChild(value)
        background.appendChild(element)
        # Outline
        element = self.theme_xml.createElement('outline')
        element.setAttribute('outlineColor', str(outline_color))
        element.setAttribute('outlineSize', str(outline_pixel))
        value = self.theme_xml.createTextNode(str(outline))
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
        background = self.theme_xml.createElement('display')
        self.theme.appendChild(background)
        # Horizontal alignment
        element = self.theme_xml.createElement('horizontalAlign')
        value = self.theme_xml.createTextNode(str(horizontal))
        element.appendChild(value)
        background.appendChild(element)
        # Vertical alignment
        element = self.theme_xml.createElement('verticalAlign')
        value = self.theme_xml.createTextNode(str(vertical))
        element.appendChild(value)
        background.appendChild(element)
        # Slide Transition
        element = self.theme_xml.createElement('slideTransition')
        value = self.theme_xml.createTextNode(str(transition))
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

    def set_default_header_footer(self):
        """
        Set the header and footer size into the current primary screen.
        10 px on each side is removed to allow for a border.
        """
        current_screen = ScreenList().current
        self.font_main_y = 0
        self.font_main_width = current_screen['size'].width() - 20
        self.font_main_height = current_screen['size'].height() * 9 / 10
        self.font_footer_width = current_screen['size'].width() - 20
        self.font_footer_y = current_screen['size'].height() * 9 / 10
        self.font_footer_height = current_screen['size'].height() / 10

    def dump_xml(self):
        """
        Dump the XML to file used for debugging
        """
        return self.theme_xml.toprettyxml(indent='  ')

    def extract_xml(self):
        """
        Print out the XML string.
        """
        self._build_xml_from_attrs()
        return self.theme_xml.toxml('utf-8').decode('utf-8')

    def extract_formatted_xml(self):
        """
        Pull out the XML string formatted for human consumption
        """
        self._build_xml_from_attrs()
        return self.theme_xml.toprettyxml(indent='    ', newl='\n', encoding='utf-8')

    def parse(self, xml):
        """
        Read in an XML string and parse it.

        ``xml``
            The XML string to parse.
        """
        self.parse_xml(str(xml))

    def parse_xml(self, xml):
        """
        Parse an XML string.

        ``xml``
            The XML string to parse.
        """
        # remove encoding string
        line = xml.find('?>')
        if line:
            xml = xml[line + 2:]
        try:
            theme_xml = objectify.fromstring(xml)
        except etree.XMLSyntaxError:
            log.exception('Invalid xml %s', xml)
            return
        xml_iter = theme_xml.getiterator()
        for element in xml_iter:
            master = ''
            if element.tag == 'background':
                if element.attrib:
                    for attr in element.attrib:
                        self._create_attr(element.tag, attr, element.attrib[attr])
            parent = element.getparent()
            if parent is not None:
                if parent.tag == 'font':
                    master = parent.tag + '_' + parent.attrib['type']
                # set up Outline and Shadow Tags and move to font_main
                if parent.tag == 'display':
                    if element.tag.startswith('shadow') or element.tag.startswith('outline'):
                        self._create_attr('font_main', element.tag, element.text)
                    master = parent.tag
                if parent.tag == 'background':
                    master = parent.tag
            if master:
                self._create_attr(master, element.tag, element.text)
                if element.attrib:
                    for attr in element.attrib:
                        base_element = attr
                        # correction for the shadow and outline tags
                        if element.tag == 'shadow' or element.tag == 'outline':
                            if not attr.startswith(element.tag):
                                base_element = element.tag + '_' + attr
                        self._create_attr(master, base_element, element.attrib[attr])
            else:
                if element.tag == 'name':
                    self._create_attr('theme', element.tag, element.text)

    def _translate_tags(self, master, element, value):
        """
        Clean up XML removing and redefining tags
        """
        master = master.strip().lstrip()
        element = element.strip().lstrip()
        value = str(value).strip().lstrip()
        if master == 'display':
            if element == 'wrapStyle':
                return True, None, None, None
            if element.startswith('shadow') or element.startswith('outline'):
                master = 'font_main'
        # fix bold font
        if element == 'weight':
            element = 'bold'
            if value == 'Normal':
                value = False
            else:
                value = True
        if element == 'proportion':
            element = 'size'
        return False, master, element, value

    def _create_attr(self, master, element, value):
        """
        Create the attributes with the correct data types and name format
        """
        reject, master, element, value = self._translate_tags(master, element, value)
        if reject:
            return
        field = self._de_hump(element)
        tag = master + '_' + field
        if field in BOOLEAN_LIST:
            setattr(self, tag, str_to_bool(value))
        elif field in INTEGER_LIST:
            setattr(self, tag, int(value))
        else:
            # make string value unicode
            if not isinstance(value, str):
                value = str(str(value), 'utf-8')
            # None means an empty string so lets have one.
            if value == 'None':
                value = ''
            setattr(self, tag, str(value).strip().lstrip())

    def __str__(self):
        """
        Return a string representation of this object.
        """
        theme_strings = []
        for key in dir(self):
            if key[0:1] != '_':
                theme_strings.append('%30s: %s' % (key, getattr(self, key)))
        return '\n'.join(theme_strings)

    def _de_hump(self, name):
        """
        Change Camel Case string to python string
        """
        sub_name = ThemeXML.FIRST_CAMEL_REGEX.sub(r'\1_\2', name)
        return ThemeXML.SECOND_CAMEL_REGEX.sub(r'\1_\2', sub_name).lower()

    def _build_xml_from_attrs(self):
        """
        Build the XML from the varables in the object
        """
        self._new_document(self.theme_name)
        if self.background_type == BackgroundType.to_string(BackgroundType.Solid):
            self.add_background_solid(self.background_color)
        elif self.background_type == BackgroundType.to_string(BackgroundType.Gradient):
            self.add_background_gradient(
                self.background_start_color,
                self.background_end_color,
                self.background_direction
            )
        elif self.background_type == BackgroundType.to_string(BackgroundType.Image):
            filename = os.path.split(self.background_filename)[1]
            self.add_background_image(filename, self.background_border_color)
        elif self.background_type == BackgroundType.to_string(BackgroundType.Transparent):
            self.add_background_transparent()
        self.add_font(
            self.font_main_name,
            self.font_main_color,
            self.font_main_size,
            self.font_main_override, 'main',
            self.font_main_bold,
            self.font_main_italics,
            self.font_main_line_adjustment,
            self.font_main_x,
            self.font_main_y,
            self.font_main_width,
            self.font_main_height,
            self.font_main_outline,
            self.font_main_outline_color,
            self.font_main_outline_size,
            self.font_main_shadow,
            self.font_main_shadow_color,
            self.font_main_shadow_size
        )
        self.add_font(
            self.font_footer_name,
            self.font_footer_color,
            self.font_footer_size,
            self.font_footer_override, 'footer',
            self.font_footer_bold,
            self.font_footer_italics,
            0,  # line adjustment
            self.font_footer_x,
            self.font_footer_y,
            self.font_footer_width,
            self.font_footer_height,
            self.font_footer_outline,
            self.font_footer_outline_color,
            self.font_footer_outline_size,
            self.font_footer_shadow,
            self.font_footer_shadow_color,
            self.font_footer_shadow_size
        )
        self.add_display(
            self.display_horizontal_align,
            self.display_vertical_align,
            self.display_slide_transition
        )
