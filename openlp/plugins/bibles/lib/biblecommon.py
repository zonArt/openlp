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

import os
import os.path
import sys
import urllib2

import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')

class BibleCommon:
    global log
    log=logging.getLogger("BibleCommon")
    log.info("BibleCommon")
    def __init__(self):
        """
        """
    def _get_web_text(self, urlstring, proxyurl):
        log.debug( "get_web_text %s %s", proxyurl, urlstring)

        if  proxyurl != "" or len(proxyurl) > 0 :
            print "ProxyUrl " ,  proxyurl + " " + str(len(proxyurl))
            proxy_support = urllib2.ProxyHandler({'http':  self.proxyurl})
            http_support = urllib2.HTTPHandler()
            opener= urllib2.build_opener(proxy_support, http_support)
            urllib2.install_opener(opener)

        xml_string = ""
        req = urllib2.Request(urlstring)
        req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
        try:
            handle = urllib2.urlopen(req)
            xml_string = handle.read()
        except IOError, e:
            if hasattr(e, 'reason'):
                log.error( 'Reason : ')
                log.error( e.reason)
        return xml_string

    def _clean_text(self, text):
        """
        Clean up text and remove extra characters
        after been downloaded from web
        """
        #return text.rstrip()
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


