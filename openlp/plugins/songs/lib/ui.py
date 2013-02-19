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
The :mod:`openlp.plugins.songs.lib.ui` module provides standard UI components
for the songs plugin.
"""
from openlp.core.lib import translate

class SongStrings(object):
    """
    Provide standard strings for use throughout the songs plugin.
    """
    # These strings should need a good reason to be retranslated elsewhere.
    Author = translate('OpenLP.Ui', 'Author', 'Singular')
    Authors = translate('OpenLP.Ui', 'Authors', 'Plural')
    AuthorUnknown = u'Author Unknown' # Used to populate the database.
    CopyrightSymbol = translate('OpenLP.Ui', '\xa9', 'Copyright symbol.')
    SongBook = translate('OpenLP.Ui', 'Song Book', 'Singular')
    SongBooks = translate('OpenLP.Ui', 'Song Books', 'Plural')
    SongIncomplete = translate('OpenLP.Ui','Title and/or verses not found')
    SongMaintenance = translate('OpenLP.Ui', 'Song Maintenance')
    Topic = translate('OpenLP.Ui', 'Topic', 'Singular')
    Topics = translate('OpenLP.Ui', 'Topics', 'Plural')
    XMLSyntaxError = translate('OpenLP.Ui', 'XML syntax error')
