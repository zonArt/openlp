"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Carsten Tinggaard

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

import platform
ver = platform.python_version()
if ver >= '2.5':
    from xml.etree.ElementTree import ElementTree, XML
else:
    from elementtree import ElementTree, XML


# borrowed from theme - can be common
DelphiColors={"clRed":0xFF0000,
               "clBlack":0x000000,
               "clWhite":0xFFFFFF}

class RootClass(object):
    """Root class for themes, songs etc
    
    provides interface for parsing xml files into object attributes
    """
    def _setFromXml(self, xml, rootTag):
        """Set song properties from given xml content
        
        xml (string) -- formatted as xml tags and values
        rootTag -- main tag of the xml
        """
        root=ElementTree(element=XML(xml))
        iter=root.getiterator()
        for element in iter:
            if element.tag != rootTag:
                t=element.text
                #print element.tag, t, type(t)
                if type(t) == type(None): # easy!
                    val=t
                if type(t) == type(" "): # strings need special handling to sort the colours out
                    #print "str",
                    if t[0] == "$": # might be a hex number
                        #print "hex",
                        try:
                            val=int(t[1:], 16)
                        except ValueError: # nope
                            #print "nope",
                            pass
                    elif DelphiColors.has_key(t):
                        #print "colour",
                        val=DelphiColors[t]
                    else:
                        #print "last chance",
                        try:
                            val=int(t)
                            #print "int",
                        except ValueError:
                            #print "give up",
                            val=t
                if (element.tag.find("Color") > 0 or
                    (element.tag.find("BackgroundParameter") == 0 and type(val) == type(0))):
                    # convert to a QtGui.Color
                    val= QtGui.QColor((val>>16) & 0xFF, (val>>8)&0xFF, val&0xFF)
                #print [val]
                setattr(self,element.tag, val)
        pass
    
    def __str__(self):
        """Return string with all public attributes
        
        The string is formatted with one attribute per line
        If the string is split on newline then the length of the
        list is equal to the number of attributes
        """
        l = []
        for k in dir(self):
            if not k.startswith("_"):
                l.append("%30s : %s" %(k,getattr(self,k)))
        return "\n".join(l)

    def _get_as_string(self):
        """Return one string with all public attributes"""
        s=""
        for k in dir(self):
            if not k.startswith("_"):
                s+= "_%s_" %(getattr(self,k))
        return s
            

blankSongXml = \
'''<?xml version="1.0" encoding="iso-8859-1"?>
<Song>
  <title>BlankSong</title>
  <searchableTitle></searchableTitle>
  <authorList></authorList>
  <songCcliNo></songCcliNo>
  <copyright></copyright>
  <showTitle>1</showTitle>
  <showAuthorList>1</showAuthorList>
  <showSongCcli>1</showSongCcli>
  <showCopyright>1</showCopyright>
  <theme></theme>
  <categoryArray></categoryArray>
  <songBook></songBook>
  <songNumber></songNumber>
  <comments></comments>
  <verseOrder></verseOrder>
  <lyrics></lyrics>
</Song>
'''

class Song(RootClass) :
    """Class for handling song properties"""
    
    def __init__(self, xmlContent = None):
        """Initialize from given xml content
        
        xmlContent (string) -- xml formatted string
        
        attributes
            title -- title of the song
            searchableTitle -- title without punctuation chars
            authorList -- list of authors
            songCcliNo -- CCLI number for this song
            copyright -- copyright string
            showTitle -- 0: no show, 1: show
            showAuthorList -- 0: no show, 1: show
            showCopyright -- 0: no show, 1: show
            showCcliNo -- 0: no show, 1: show
            theme -- name of theme or blank
            categoryArray -- list of user defined properties (hymn, gospel)
            songBook -- name of originating book
            songNumber -- number of the song, related to a songbook
            comments -- free comment
            verseOrder -- presentation order of the slides
            lyrics -- simple or xml formatted (tbd)
        """
        super(Song, self).__init__()
        global blankSongXml
        self._setFromXml(blankSongXml, "Song")
        
