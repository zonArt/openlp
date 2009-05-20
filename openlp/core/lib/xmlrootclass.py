# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley, Carsten Tinggaard

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
import sys
import os
from types import StringType, NoneType, UnicodeType
sys.path.append(os.path.abspath(u'./../..'))

from xml.etree.ElementTree import ElementTree, XML


class XmlRootClass(object):
    """Root class for themes, songs etc

    provides interface for parsing xml files into object attributes

    if you overload this class and provide a function called
    post_tag_hook, it will be called thusly for each tag,value pair:

    (element.tag, val) = self.post_tag_hook(element.tag, val)
    """
    def _setFromXml(self, xml, rootTag):
        """Set song properties from given xml content

        xml (string) -- formatted as xml tags and values
        rootTag -- main tag of the xml
        """
        root = ElementTree(element=XML(xml))
        iter = root.getiterator()
        for element in iter:
            if element.tag != rootTag:
                t = element.text
                #print element.tag, t, type(t)
                if type(t) == NoneType:
                    # easy!
                    val=t
                elif type(t) == UnicodeType :
                    val=t
                elif type(t) == StringType:
                    # strings need special handling to sort the colours out
                    #print "str",
                    if t[0] == '$':
                        # might be a hex number
                        #print "hex",
                        try:
                            val = int(t[1:], 16)
                        except ValueError:
                            # nope
                            #print "nope",
                            pass
                    else:
                        #print "last chance",
                        try:
                            val=int(t)
                            #print "int",
                        except ValueError:
                            #print "give up",
                            val=t
                    if hasattr(self, u'post_tag_hook'):
                        (element.tag, val) = self.post_tag_hook(element.tag, val)
                setattr(self, element.tag, val)
        pass

    def __str__(self):
        """Return string with all public attributes

        The string is formatted with one attribute per line
        If the string is split on newline then the length of the
        list is equal to the number of attributes
        """
        l = []
        for k in dir(self):
            if not k.startswith(u'_'):
                l.append(u'%30s : %s' %(k,getattr(self,k)))
        return u'\n'.join(l)

    def _get_as_string(self):
        """Return one string with all public attributes"""
        s=""
        for k in dir(self):
            if not k.startswith(u'_'):
                s+= u'_%s_' %(getattr(self,k))
        return s

