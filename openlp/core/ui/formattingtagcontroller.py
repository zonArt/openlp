# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
The :mod:`formattingtagform` provides an Tag Edit facility. The Base set are protected and included each time loaded.
Custom tags can be defined and saved. The Custom Tag arrays are saved in a pickle so QSettings works on them. Base Tags
cannot be changed.
"""

import re
import cgi

from openlp.core.lib import translate


class FormattingTagController(object):
    """
    The :class:`FormattingTagController` manages the non UI functions .
    """
    def __init__(self):
        """
        Initiator
        """
        self.html_tag_regex = re.compile(r'<(?:(?P<close>/(?=[^\s/>]+>))?'
        r'(?P<tag>[^\s/!\?>]+)(?:\s+[^\s=]+="[^"]*")*\s*(?P<empty>/)?'
        r'|(?P<cdata>!\[CDATA\[(?:(?!\]\]>).)*\]\])'
        r'|(?P<procinst>\?(?:(?!\?>).)*\?)'
        r'|(?P<comment>!--(?:(?!-->).)*--))>', re.UNICODE)
        self.html_regex = re.compile(r'^(?:[^<>]*%s)*[^<>]*$' % self.html_tag_regex.pattern)

    def pre_save(self):
        self.custom_tags = []

    def validate_for_save(self, desc, tag, start_html, end_html):
        if not desc:
            pass
        print desc
        print self.start_html_to_end_html(start_html)

    def html_start_validate(self, start, end):
        pass

    def _strip(self, tag):
        """
        Remove tag wrappers for editing.
        """
        tag = tag.replace(u'{', u'')
        tag = tag.replace(u'}', u'')
        return tag

    def start_html_to_end_html(self, start_html):
        """
        Return the end HTML for a given start HTML or None if invalid.
        """
        end_tags = []
        match = self.html_regex.match(start_html)
        if match:
            match = self.html_tag_regex.search(start_html)
            while match:
                if match.group(u'tag'):
                    tag = match.group(u'tag').lower()
                    if match.group(u'close'):
                        if match.group(u'empty') or not end_tags or end_tags.pop() != tag:
                            return
                    elif not match.group(u'empty'):
                        end_tags.append(tag)
                match = self.html_tag_regex.search(start_html, match.end())
            return u''.join(map(lambda tag: u'</%s>' % tag, reversed(end_tags)))

    def start_tag_changed(self, start_html, end_html):
        end = self.start_html_to_end_html(start_html)
        if not end_html:
            return None, end