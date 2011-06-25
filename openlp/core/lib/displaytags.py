# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

from openlp.core.lib import translate

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
        base_tags = []
        # Append the base tags.
        # Hex Color tags from http://www.w3schools.com/html/html_colornames.asp
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Red'),
            u'start tag': u'{r}',
            u'start html': u'<span style="-webkit-text-fill-color:red">',
            u'end tag': u'{/r}', u'end html': u'</span>', u'protected': True})
        base_tags.append({u'desc':  translate('OpenLP.DisplayTags', 'Black'),
            u'start tag': u'{b}',
            u'start html': u'<span style="-webkit-text-fill-color:black">',
            u'end tag': u'{/b}', u'end html': u'</span>', u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Blue'),
            u'start tag': u'{bl}',
            u'start html': u'<span style="-webkit-text-fill-color:blue">',
            u'end tag': u'{/bl}', u'end html': u'</span>', u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Yellow'),
            u'start tag': u'{y}',
            u'start html': u'<span style="-webkit-text-fill-color:yellow">',
            u'end tag': u'{/y}', u'end html': u'</span>', u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Green'),
            u'start tag': u'{g}',
            u'start html': u'<span style="-webkit-text-fill-color:green">',
            u'end tag': u'{/g}', u'end html': u'</span>', u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Pink'),
            u'start tag': u'{pk}',
            u'start html': u'<span style="-webkit-text-fill-color:#FFC0CB">',
            u'end tag': u'{/pk}', u'end html': u'</span>', u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Orange'),
            u'start tag': u'{o}',
            u'start html': u'<span style="-webkit-text-fill-color:#FFA500">',
            u'end tag': u'{/o}', u'end html': u'</span>', u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Purple'),
            u'start tag': u'{pp}',
            u'start html': u'<span style="-webkit-text-fill-color:#800080">',
            u'end tag': u'{/pp}', u'end html': u'</span>', u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'White'),
            u'start tag': u'{w}',
            u'start html': u'<span style="-webkit-text-fill-color:white">',
            u'end tag': u'{/w}', u'end html': u'</span>', u'protected': True})
        base_tags.append({
            u'desc': translate('OpenLP.DisplayTags', 'Superscript'),
            u'start tag': u'{su}', u'start html': u'<sup>',
            u'end tag': u'{/su}', u'end html': u'</sup>', u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Subscript'),
            u'start tag': u'{sb}', u'start html': u'<sub>',
            u'end tag': u'{/sb}', u'end html': u'</sub>', u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Paragraph'),
            u'start tag': u'{p}', u'start html': u'<p>', u'end tag': u'{/p}',
            u'end html': u'</p>', u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Bold'),
            u'start tag': u'{st}', u'start html': u'<strong>',
            u'end tag': u'{/st}', u'end html': u'</strong>',
            u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Italics'),
            u'start tag': u'{it}', u'start html': u'<em>', u'end tag': u'{/it}',
            u'end html': u'</em>', u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Underline'),
            u'start tag': u'{u}',
            u'start html': u'<span style="text-decoration: underline;">',
            u'end tag': u'{/u}', u'end html': u'</span>', u'protected': True})
        base_tags.append({u'desc': translate('OpenLP.DisplayTags', 'Break'),
            u'start tag': u'{br}', u'start html': u'<br>', u'end tag': u'',
            u'end html': u'', u'protected': True})
        DisplayTags.add_html_tags(base_tags)

    @staticmethod
    def add_html_tags(tags):
        """
        Add a list of tags to the list
        """
        DisplayTags.html_expands.extend(tags)

    @staticmethod
    def remove_html_tag(tag_id):
        """
        Removes an individual html_expands tag.
        """
        DisplayTags.html_expands.pop(tag_id)
