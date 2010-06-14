# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

import os
import sys

from xml.etree.ElementTree import ElementTree, XML

sys.path.append(os.path.abspath(os.path.join(u'.', u'..', u'..')))

class XmlRootClass(object):
    """
    Root class for themes, songs etc

    This class provides interface for parsing xml files into object attributes.

    If you overload this class and provide a function called `post_tag_hook`,
    it will be called thusly for each `tag, value` pair::

        (element.tag, val) = self.post_tag_hook(element.tag, val)
    """
    def _set_from_xml(self, xml, root_tag):
        """
        Set song properties from given xml content.

        ``xml``
            Formatted xml tags and values.
        ``root_tag``
            The root tag of the xml.
        """
        root = ElementTree(element=XML(xml))
        xml_iter = root.getiterator()
        for element in xml_iter:
            if element.tag != root_tag:
                text = element.text
                if text is None:
                    val = text
                elif isinstance(text, basestring):
                    # Strings need special handling to sort the colours out
                    if text[0] == u'$':
                        # This might be a hex number, let's try to convert it.
                        try:
                            val = int(text[1:], 16)
                        except ValueError:
                            pass
                    else:
                        # Let's just see if it's a integer.
                        try:
                            val = int(text)
                        except ValueError:
                            # Ok, it seems to be a string.
                            val = text
                    if hasattr(self, u'post_tag_hook'):
                        (element.tag, val) = \
                            self.post_tag_hook(element.tag, val)
                setattr(self, element.tag, val)

    def __str__(self):
        """
        Return string with all public attributes

        The string is formatted with one attribute per line
        If the string is split on newline then the length of the
        list is equal to the number of attributes
        """
        attributes = []
        for attrib in dir(self):
            if not attrib.startswith(u'_'):
                attributes.append(
                    u'%30s : %s' % (attrib, getattr(self, attrib)))
        return u'\n'.join(attributes)

    def _get_as_string(self):
        """
        Return one string with all public attributes
        """
        result = u''
        for attrib in dir(self):
            if not attrib.startswith(u'_'):
                result += u'_%s_' % getattr(self, attrib)
        return result

