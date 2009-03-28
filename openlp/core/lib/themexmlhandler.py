from xml.dom.minidom import  Document
from xml.etree.ElementTree import ElementTree, XML, dump
"""
<?xml version="1.0" encoding="UTF-8"?>
<song version="1.0">
   <lyrics language="en">
       <verse type="chorus" label="1">
           <![CDATA[ ... ]]>
       </verse>
   </lyrics>
</song>

"""
class ThemeXMLBuilder():
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
        background = self.theme_xml.createElement(u'Background')
        background.setAttribute(u'mode', u'transparent')
        self.theme.appendChild(background)

    def add_background_solid(self, bkcolor):
        background = self.theme_xml.createElement(u'Background')
        background.setAttribute(u'mode', u'opaque')
        background.setAttribute(u'type', u'solid')
        self.theme.appendChild(background)

        color = self.theme_xml.createElement(u'color')
        bkc = self.theme_xml.createTextNode(bkcolor)
        color.appendChild(bkc)
        background.appendChild(color)

    def add_background_gradient(self, startcolor, endcolor):
        background = self.theme_xml.createElement(u'Background')
        background.setAttribute(u'mode', u'opaque')
        background.setAttribute(u'type', u'gradient')
        self.theme.appendChild(background)

        color = self.theme_xml.createElement(u'startcolor')
        bkc = self.theme_xml.createTextNode(startcolor)
        color.appendChild(bkc)
        background.appendChild(color)

        color = self.theme_xml.createElement(u'endcolor')
        bkc = self.theme_xml.createTextNode(endcolor)
        color.appendChild(bkc)
        background.appendChild(color)

    def add_background_image(self, filename, bordercolor):
        background = self.theme_xml.createElement(u'Background')
        background.setAttribute(u'mode', u'opaque')
        background.setAttribute(u'type', u'image')
        self.theme.appendChild(background)

        color = self.theme_xml.createElement(u'filename')
        bkc = self.theme_xml.createCDATASection(filename)
        color.appendChild(bkc)
        background.appendChild(color)

        color = self.theme_xml.createElement(u'bordercolor')
        bkc = self.theme_xml.createTextNode(bordercolor)
        color.appendChild(bkc)
        background.appendChild(color)


    def add_verse_to_lyrics(self, type, number, content):
        """
        type - type of verse (Chorus, Verse , Bridge, Custom etc
        number - number of item eg verse 1
        content - the text to be stored
        """
        verse = self.theme_xml.createElement(u'verse')
        verse.setAttribute(u'type', type)
        verse.setAttribute(u'label', number)
        self.lyrics.appendChild(verse)

        # add data as a CDATA section
        cds = self.theme_xml.createCDATASection(content)
        verse.appendChild(cds)

    def dump_xml(self):
        # Debugging aid to see what we have
        print self.theme_xml.toprettyxml(indent="  ")

    def extract_xml(self):
        # Print our newly created XML
        return self.theme_xml.toxml()

class ThemeXMLParser():
    def __init__(self, xml):
        self.theme_xml = ElementTree(element=XML(xml))

    def get_verses(self):
        #return a list of verse's and attributes
        iter=self.theme_xml.getiterator()
        verse_list = []
        for element in iter:
            if element.tag == u'verse':
                verse_list.append([element.attrib, element.text])
        return verse_list

    def dump_xml(self):
        # Debugging aid to see what we have
        print dump(self.theme_xml)
