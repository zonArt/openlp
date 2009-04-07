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
from xml.dom.minidom import  Document
from xml.etree.ElementTree import ElementTree, XML, dump

class ThemeXML():
    def __init__(self):
        # Create the minidom document
        self.theme_xml = Document()

    def new_document(self, name):
        # Create the <song> base element
        self.theme = self.theme_xml.createElement(u'Theme')
        self.theme_xml.appendChild(self.theme)
        self.theme.setAttribute(u'version', u'1.0')

        self.name = self.theme_xml.createElement(u'Name')
        ctn = self.theme_xml.createTextNode(name)
        self.name.appendChild(ctn)
        self.theme.appendChild(self.name)

    def add_background_transparent(self):
        # Create the main <lyrics> element
        background = self.theme_xml.createElement(u'background')
        background.setAttribute(u'mode', u'transparent')
        self.theme.appendChild(background)

    def add_background_solid(self, bkcolor):
        background = self.theme_xml.createElement(u'background')
        background.setAttribute(u'mode', u'opaque')
        background.setAttribute(u'type', u'solid')
        self.theme.appendChild(background)

        color = self.theme_xml.createElement(u'color')
        bkc = self.theme_xml.createTextNode(bkcolor)
        color.appendChild(bkc)
        background.appendChild(color)

    def add_background_gradient(self, startcolor, endcolor, direction):
        background = self.theme_xml.createElement(u'background')
        background.setAttribute(u'mode', u'opaque')
        background.setAttribute(u'type', u'Gradient')
        self.theme.appendChild(background)

        color = self.theme_xml.createElement(u'startColor')
        bkc = self.theme_xml.createTextNode(startcolor)
        color.appendChild(bkc)
        background.appendChild(color)

        color = self.theme_xml.createElement(u'endColor')
        bkc = self.theme_xml.createTextNode(endcolor)
        color.appendChild(bkc)
        background.appendChild(color)

        color = self.theme_xml.createElement(u'direction')
        bkc = self.theme_xml.createTextNode(direction)
        color.appendChild(bkc)
        background.appendChild(color)

    def add_background_image(self, filename):
        background = self.theme_xml.createElement(u'background')
        background.setAttribute(u'mode', u'opaque')
        background.setAttribute(u'type', u'image')
        self.theme.appendChild(background)

        color = self.theme_xml.createElement(u'filename')
        bkc = self.theme_xml.createCDATASection(filename)
        color.appendChild(bkc)
        background.appendChild(color)

    def add_font(self, fontname, fontcolor, fontproportion, fonttype=u'main'):
        background = self.theme_xml.createElement(u'font')
        background.setAttribute(u'type',fonttype)
        self.theme.appendChild(background)

        name = self.theme_xml.createElement(u'name')
        fn = self.theme_xml.createTextNode(fontname)
        name.appendChild(fn)
        background.appendChild(name)

        name = self.theme_xml.createElement(u'color')
        fn = self.theme_xml.createTextNode(fontcolor)
        name.appendChild(fn)
        background.appendChild(name)

        name = self.theme_xml.createElement(u'proportion')
        fn = self.theme_xml.createTextNode(fontproportion)
        name.appendChild(fn)
        background.appendChild(name)

    def add_display(self, shadow, shadowColor, outline, outlineColor, horizontal, vertical, wrap):
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

    def child_element(self, tag, value):
        tagElement = self.theme_xml.createElement(tag)
        tagValue = self.theme_xml.createTextNode(value)
        tagElement.appendChild(ftagValue)
        self.background.appendChild(tagElement)

    def dump_xml(self):
        # Debugging aid to see what we have
        print self.theme_xml.toprettyxml(indent="  ")

    def extract_xml(self):
        # Print our newly created XML
        return self.theme_xml.toxml()

    def parse(self, xml):
        theme_xml = ElementTree(element=XML(xml))
        iter=theme_xml.getiterator()
        master = u''
        for element in iter:
            #print  element.tag, element.text
            if len(element.getchildren()) > 0:
                master= element.tag + u'_'
            if len(element.attrib) > 0:
                #print "D", element.tag , element.attrib
                for e in element.attrib.iteritems():
                    #print "A", master,  e[0], e[1]
                    if master == u'font_' and e[0] == u'type':
                        master += e[1] + u'_'
                    elif master == u'display_' and (element.tag == u'shadow' or element.tag == u'outline'):
                        #print "b", master, element.tag, element.text, e[0], e[1]
                        setattr(self, master + element.tag , element.text)
                        setattr(self, master + element.tag +u'_'+ e[0], e[1])
                    else:
                        field = master + e[0]
                        setattr(self, field, e[1])
            else:
                #print "c", element.tag
                if element.tag is not None :
                    field = master + element.tag
                    setattr(self, field, element.text)

    def __str__(self):
        s = u''
        for k in dir(self):
            if k[0:1] != u'_':
                s+= u'%30s : %s\n' %(k,getattr(self,k))
        return s
