"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

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

import os, os.path
import sys
import urllib2

import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')
                
class BibleCommon:
    def __init__(self):
        """
        """
    def _cleanText(self, text):
        """
        Clean up text and remove extra characters
        """
#        text = text.replace('\n', '')
#        text = text.replace('\r', '')
#        text = text.replace('&nbsp;', '')
#        text = text.replace('<P>', '')
#        text = text.replace('"', '')
        x = text.find("<sup>")
        while x > -1:
            y = text.find("</sup>")            
            #print x, y
            #print verseText[:x]
            #print verseText[y + 6:len(verseText)]
            text= text[:x] + text[y + 6:len(text)]
            x = text.find("<sup>")
            #print "text= " + text

        text= text.replace('\n', '')
        text= text.replace('\r', '')
        text= text.replace('&nbsp;', '')
        text= text.replace('<P>', '')
        text= text.replace('<I>', '')
        text= text.replace('</I>', '')        
        text= text.replace('<P />', '')
        text= text.replace('<p />', '')        
        text= text.replace('</P>', '')
        text= text.replace('<BR>', '')            
        text= text.replace('<BR />', '')                    
        text= text.replace(chr(189), '1/2')
        text= text.replace("&quot;", '"')
        text= text.replace("&apos;", "'")
        x = text.find("<")
        #print verseText
#        while x > -1:
#            y = text.find(">")
#            #print x ,  y
#            #print verseText[:x-1]
#            #print verseText[y : y-1]
#            text= text[:x] + text[y+1 : len(text)]            
#            x = text.find("<")            
        text= text.replace('>', '')
        return text.rstrip()
