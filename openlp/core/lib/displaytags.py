# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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
Provide Html Tag management and Display Tag access class
"""

from openlp.core.lib import base_html_expands

class DisplayTags(object):
    """
    Static Class to HTML Tags to be access around the code the list is managed
    by the Options Tab.
    """
    html_expands = []

    @staticmethod
    def get_html_tags():
        """
        Provide access to the html_expands list.
        """
        return DisplayTags.html_expands

    @staticmethod
    def reset_html_tags():
        """
        Resets the html_expands list.
        """
        DisplayTags.html_expands = []
        for html in base_html_expands:
            DisplayTags.html_expands.append(html)

    @staticmethod
    def add_html_tag(tag):
        """
        Add a new tag to the list
        """
        DisplayTags.html_expands.append(tag)

    @staticmethod
    def remove_html_tag(tag_id):
        """
        Removes an individual html_expands tag.
        """
        DisplayTags.html_expands.pop(tag_id)
