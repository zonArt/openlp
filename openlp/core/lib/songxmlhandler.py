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
class SongXMLBuilder():
    def __init__(self):
        # Create the minidom document        
        self.song_xml = Document()
        
    def new_document(self):
        # Create the <song> base element
        self.song = self.song_xml.createElement("song")
        self.song_xml.appendChild(self.song)
        self.song.setAttribute("version", "1.0")
        
    def add_lyrics_to_song(self):
        # Create the main <lyrics> element
        self.lyrics = self.song_xml.createElement("lyrics")
        self.lyrics.setAttribute("language", "en")
        self.song.appendChild(self.lyrics)
        
    def add_verse_to_lyrics(self, type, number, content): 
        """
        type - type of verse (Chorus, Verse , Bridge, Custom etc
        number - number of item eg verse 1
        content - the text to be stored
        """
        verse = self.song_xml.createElement("verse")
        verse.setAttribute("type", type)
        verse.setAttribute('label', number)        
        self.lyrics.appendChild(verse)
        
        # add data as a CDATA section
        cds = self.song_xml.createCDATASection(content)
        verse.appendChild(cds)
    
    def dump_xml(self):
        # Debugging aid to see what we have
        print self.song_xml.toprettyxml(indent="  ")
        
    def extract_xml(self):
        # Print our newly created XML
        return self.song_xml.toxml()
        
class SongXMLParser():
    def __init__(self, xml):
        self.song_xml = ElementTree(element=XML(xml))
        
    def get_verses(self):
        #return a list of verse's and attributes
        iter=self.song_xml.getiterator()
        verse_list = []
        for element in iter: 
            if element.tag == 'verse':
                verse_list.append([element.attrib, element.text])
        return verse_list
        
    def dump_xml(self):
        # Debugging aid to see what we have
        print dump(self.song_xml)
