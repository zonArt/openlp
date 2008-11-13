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
        after been downloaded from web
        """
        # Remove Headings from the Text
        i = text.find("<h")
        while i > -1:
            j=text.find("</h", i)            
            text = text[ : (i - 1)]+text[(j+4)]
            i = text.find("<h")
            
        # Remove Support References from the Text
        x = text.find("<sup>")
        while x > -1:
            y = text.find("</sup>")            
            text= text[:x] + text[y + 6:len(text)]
            x = text.find("<sup>")

        # Static Clean ups
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
        i = text.find("<")
        while i > -1 :
            j = text.find(">", i)
            text= text[:i] + text[j+1:]            
            i = text.find("<")
      
        text= text.replace('>', '')
        return text.rstrip()
