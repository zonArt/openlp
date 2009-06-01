# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten Tinggaard

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
from xml.dom.minidom import  Document
from xml.etree.ElementTree import ElementTree, XML, dump

For XML Schema see wiki.openlp.org
"""
import os,  os.path
from openlp.core.lib import str_to_bool
from xml.dom.minidom import  Document
from xml.etree.ElementTree import ElementTree, XML, dump

blankthemexml=\
'''<?xml version="1.0" encoding="iso-8859-1"?>
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
      <location override="False" x="0" y="0" width="0" height="0"/>
   </font>
   <font type="footer">
      <name>Arial</name>
      <color>#000000</color>
      <proportion>12</proportion>
      <location override="False" x="0" y="0" width="0" height="0"/>
   </font>
   <display>
      <shadow color="#000000">True</shadow>
      <outline color="#000000">False</outline>
       <horizontalAlign>0</horizontalAlign>
       <verticalAlign>0</verticalAlign>
       <wrapStyle>0</wrapStyle>
   </display>
 </theme>
'''

class ThemeXML():
    def __init__(self):
        # Create the minidom document
        self.theme_xml = Document()

    def extend_image_filename(self, path):
        """
        Add the path name to the image name so the background can be rendered.
        """
        if self.background_filename is not None:
            self.background_filename = os.path.join(path, self.theme_name, self.background_filename)

    def new_document(self, name):
        self.theme = self.theme_xml.createElement(u'theme')
        self.theme_xml.appendChild(self.theme)
        self.theme.setAttribute(u'version', u'1.0')

        self.name = self.theme_xml.createElement(u'name')
        ctn = self.theme_xml.createTextNode(name)
        self.name.appendChild(ctn)
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
        """
        background = self.theme_xml.createElement(u'background')
        background.setAttribute(u'mode', u'opaque')
        background.setAttribute(u'type', u'solid')
        self.theme.appendChild(background)

        self.child_element(background, u'color', bkcolor)

    def add_background_gradient(self, startcolor, endcolor, direction):
        """
        Add a gradient background.
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
        """
        background = self.theme_xml.createElement(u'background')
        background.setAttribute(u'mode', u'opaque')
        background.setAttribute(u'type', u'image')
        self.theme.appendChild(background)

        #Create Filename element
        self.child_element(background, u'filename', filename)

    def add_font(self, name, color, proportion, override, fonttype=u'main', xpos=0, ypos=0 ,width=0, height=0):
        """
        Add a Font.
        """
        background = self.theme_xml.createElement(u'font')
        background.setAttribute(u'type',fonttype)
        self.theme.appendChild(background)

        #Create Font name element
        self.child_element(background, u'name', name)

        #Create Font color element
        self.child_element(background, u'color', color)

        #Create Proportion name element
        self.child_element(background, u'proportion', proportion)

        #Create Proportion name element
        self.child_element(background, u'proportion', proportion)

        #Create Location element
        element = self.theme_xml.createElement(u'location')
        element.setAttribute(u'override',override)

        if override == u'True':
            element.setAttribute(u'x', xpos)
            element.setAttribute(u'y', ypos)
            element.setAttribute(u'width', width)
            element.setAttribute(u'height', height)
        background.appendChild(element)

    def add_display(self, shadow, shadowColor, outline, outlineColor, horizontal, vertical, wrap):
        """
        Add a Display options.
        """
        background = self.theme_xml.createElement(u'display')
        self.theme.appendChild(background)

        tagElement = self.theme_xml.createElement(u'shadow')

        tagElement.setAttribute(u'color',shadowColor)
        tagValue = self.theme_xml.createTextNode(shadow)
        tagElement.appendChild(tagValue)
        background.appendChild(tagElement)

        tagElement = self.theme_xml.createElement(u'outline')
        tagElement.setAttribute(u'color',outlineColor)
        tagValue = self.theme_xml.createTextNode(outline)
        tagElement.appendChild(tagValue)
        background.appendChild(tagElement)

        tagElement = self.theme_xml.createElement(u'horizontalAlign')
        tagValue = self.theme_xml.createTextNode(horizontal)
        tagElement.appendChild(tagValue)
        background.appendChild(tagElement)

        tagElement = self.theme_xml.createElement(u'verticalAlign')
        tagValue = self.theme_xml.createTextNode(vertical)
        tagElement.appendChild(tagValue)
        background.appendChild(tagElement)

        tagElement = self.theme_xml.createElement(u'wrapStyle')
        tagValue = self.theme_xml.createTextNode(wrap)
        tagElement.appendChild(tagValue)
        background.appendChild(tagElement)

    def child_element(self, element, tag, value):
        child = self.theme_xml.createElement(tag)
        child.appendChild(self.theme_xml.createTextNode(value))
        element.appendChild(child)
        return child

    def dump_xml(self):
        # Debugging aid to see what we have
        print self.theme_xml.toprettyxml(indent=u'  ')

    def extract_xml(self):
        # Print our newly created XML
        return self.theme_xml.toxml()

    def parse(self, xml):
        self.baseParseXml()
        self.parse_xml(xml)
        self.theme_filename_extended = False

    def baseParseXml(self):
        self.parse_xml(blankthemexml)

    def parse_xml(self, xml):
        theme_xml = ElementTree(element=XML(xml))
        iter = theme_xml.getiterator()
        master = u''
        for element in iter:
            #print  element.tag, element.text
            if len(element.getchildren()) > 0:
                master = element.tag + u'_'
            if len(element.attrib) > 0:
                #print "D", element.tag , element.attrib
                for e in element.attrib.iteritems():
                    #print "A", master,  e[0], e[1]
                    if master == u'font_' and e[0] == u'type':
                        master += e[1] + u'_'
                    elif master == u'display_' and (element.tag == u'shadow' or element.tag == u'outline'):
                        #print "b", master, element.tag, element.text, e[0], e[1]
                        et = str_to_bool(element.text)
                        setattr(self, master + element.tag , et)
                        setattr(self, master + element.tag + u'_'+ e[0], e[1])
                    else:
                        field = master + e[0]
                        e1 = e[1]
                        if e[1] == u'True' or e[1] == u'False':
                            e1 = str_to_bool(e[1])
                        setattr(self, field, e1)
            else:
                #print "c", element.tag, element.text
                if element.tag is not None:
                    field = master + element.tag
                    setattr(self, field, element.text)

    def __str__(self):
        s = u''
        for k in dir(self):
            if k[0:1] != u'_':
                s += u'%30s : %s\n' %(k,getattr(self,k))
        return s
