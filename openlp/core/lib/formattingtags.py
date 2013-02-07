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
Provide HTML Tag management and Formatting Tag access class
"""
import cPickle

from openlp.core.lib import Settings, translate


class FormattingTags(object):
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
        return FormattingTags.html_expands

    @staticmethod
    def save_html_tags():
        """
        Saves all formatting tags except protected ones.
        """
        tags = []
        for tag in FormattingTags.html_expands:
            if not tag[u'protected'] and not tag.get(u'temporary'):
                # Using dict ensures that copy is made and encoding of values
                # a little later does not affect tags in the original list
                tags.append(dict(tag))
                tag = tags[-1]
                # Remove key 'temporary' from tags.
                # It is not needed to be saved.
                if u'temporary' in tag:
                    del tag[u'temporary']
                for element in tag:
                    if isinstance(tag[element], unicode):
                        tag[element] = tag[element].encode('utf8')
        # Formatting Tags were also known as display tags.
        Settings().setValue(u'displayTags/html_tags', cPickle.dumps(tags) if tags else u'')

    @staticmethod
    def load_tags():
        """
        Load the Tags from store so can be used in the system or used to
        update the display.
        """
        temporary_tags = [tag for tag in FormattingTags.html_expands
            if tag.get(u'temporary')]
        FormattingTags.html_expands = []
        base_tags = []
        # Append the base tags.
        # Hex Color tags from http://www.w3schools.com/html/html_colornames.asp
        base_tags.append({u'desc': translate('OpenLP.FormattingTags', 'Red'),
            u'start tag': u'{r}',
            u'start html': u'<span style="-webkit-text-fill-color:red">',
            u'end tag': u'{/r}', u'end html': u'</span>', u'protected': True,
            u'temporary': False})
        base_tags.append({u'desc': translate('OpenLP.FormattingTags', 'Black'),
            u'start tag': u'{b}',
            u'start html': u'<span style="-webkit-text-fill-color:black">',
            u'end tag': u'{/b}', u'end html': u'</span>', u'protected': True,
            u'temporary': False})
        base_tags.append({u'desc': translate('OpenLP.FormattingTags', 'Blue'),
            u'start tag': u'{bl}',
            u'start html': u'<span style="-webkit-text-fill-color:blue">',
            u'end tag': u'{/bl}', u'end html': u'</span>', u'protected': True,
            u'temporary': False})
        base_tags.append({u'desc': translate('OpenLP.FormattingTags', 'Yellow'),
            u'start tag': u'{y}',
            u'start html': u'<span style="-webkit-text-fill-color:yellow">',
            u'end tag': u'{/y}', u'end html': u'</span>', u'protected': True,
            u'temporary': False})
        base_tags.append({u'desc': translate('OpenLP.FormattingTags', 'Green'),
            u'start tag': u'{g}',
            u'start html': u'<span style="-webkit-text-fill-color:green">',
            u'end tag': u'{/g}', u'end html': u'</span>', u'protected': True,
            u'temporary': False})
        base_tags.append({u'desc': translate('OpenLP.FormattingTags', 'Pink'),
            u'start tag': u'{pk}',
            u'start html': u'<span style="-webkit-text-fill-color:#FFC0CB">',
            u'end tag': u'{/pk}', u'end html': u'</span>', u'protected': True,
            u'temporary': False})
        base_tags.append({u'desc': translate('OpenLP.FormattingTags', 'Orange'),
            u'start tag': u'{o}',
            u'start html': u'<span style="-webkit-text-fill-color:#FFA500">',
            u'end tag': u'{/o}', u'end html': u'</span>', u'protected': True,
            u'temporary': False})
        base_tags.append({u'desc': translate('OpenLP.FormattingTags', 'Purple'),
            u'start tag': u'{pp}',
            u'start html': u'<span style="-webkit-text-fill-color:#800080">',
            u'end tag': u'{/pp}', u'end html': u'</span>', u'protected': True,
            u'temporary': False})
        base_tags.append({u'desc': translate('OpenLP.FormattingTags', 'White'),
            u'start tag': u'{w}',
            u'start html': u'<span style="-webkit-text-fill-color:white">',
            u'end tag': u'{/w}', u'end html': u'</span>', u'protected': True,
            u'temporary': False})
        base_tags.append({
            u'desc': translate('OpenLP.FormattingTags', 'Superscript'),
            u'start tag': u'{su}', u'start html': u'<sup>',
            u'end tag': u'{/su}', u'end html': u'</sup>', u'protected': True,
            u'temporary': False})
        base_tags.append({
            u'desc': translate('OpenLP.FormattingTags', 'Subscript'),
            u'start tag': u'{sb}', u'start html': u'<sub>',
            u'end tag': u'{/sb}', u'end html': u'</sub>', u'protected': True,
            u'temporary': False})
        base_tags.append({
            u'desc': translate('OpenLP.FormattingTags', 'Paragraph'),
            u'start tag': u'{p}', u'start html': u'<p>', u'end tag': u'{/p}',
            u'end html': u'</p>', u'protected': True,
            u'temporary': False})
        base_tags.append({u'desc': translate('OpenLP.FormattingTags', 'Bold'),
            u'start tag': u'{st}', u'start html': u'<strong>',
            u'end tag': u'{/st}', u'end html': u'</strong>',
            u'protected': True, u'temporary': False})
        base_tags.append({
            u'desc': translate('OpenLP.FormattingTags', 'Italics'),
            u'start tag': u'{it}', u'start html': u'<em>', u'end tag': u'{/it}',
            u'end html': u'</em>', u'protected': True, u'temporary': False})
        base_tags.append({
            u'desc': translate('OpenLP.FormattingTags', 'Underline'),
            u'start tag': u'{u}',
            u'start html': u'<span style="text-decoration: underline;">',
            u'end tag': u'{/u}', u'end html': u'</span>', u'protected': True,
            u'temporary': False})
        base_tags.append({u'desc': translate('OpenLP.FormattingTags', 'Break'),
            u'start tag': u'{br}', u'start html': u'<br>', u'end tag': u'',
            u'end html': u'', u'protected': True, u'temporary': False})
        FormattingTags.add_html_tags(base_tags)
        FormattingTags.add_html_tags(temporary_tags)

        # Formatting Tags were also known as display tags.
        user_expands = Settings().value(u'displayTags/html_tags')
        # cPickle only accepts str not unicode strings
        user_expands_string = str(user_expands)
        if user_expands_string:
            user_tags = cPickle.loads(user_expands_string)
            for tag in user_tags:
                for element in tag:
                    if isinstance(tag[element], str):
                        tag[element] = tag[element].decode('utf8')
            # If we have some user ones added them as well
            FormattingTags.add_html_tags(user_tags)

    @staticmethod
    def add_html_tags(tags):
        """
        Add a list of tags to the list.

        ``tags``
            The list with tags to add.

        Each **tag** has to be a ``dict`` and should have the following keys:

        * desc
            The formatting tag's description, e. g. **Red**

        * start tag
            The start tag, e. g. ``{r}``

        * end tag
            The end tag, e. g. ``{/r}``

        * start html
            The start html tag. For instance ``<span style="
            -webkit-text-fill-color:red">``

        * end html
            The end html tag. For example ``</span>``

        * protected
            A boolean stating whether this is a build-in tag or not. Should be
            ``True`` in most cases.

        * temporary
            A temporary tag will not be saved, but is also considered when
            displaying text containing the tag. It has to be a ``boolean``.
        """
        FormattingTags.html_expands.extend(tags)

    @staticmethod
    def remove_html_tag(tag_id):
        """
        Removes an individual html_expands tag.
        """
        FormattingTags.html_expands.pop(tag_id)
