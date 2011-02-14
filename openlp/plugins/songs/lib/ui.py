# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
    AuthorUnknown = translate('OpenLP.Ui', 'Author Unknown') # Used in the UI.
    AuthorUnknownUnT = u'Author Unknown' # Used to populate the database.
    CouldNotAdd = unicode(translate('OpenLP.Ui', 'Could not add your %s.'))
    NoDeleteAssigned = unicode(translate('OpenLP.Ui', 'This %s cannot be '
        'deleted as it is currently assigned to at least one song.'))
    SongBook = translate('OpenLP.Ui', 'Song Book', 'Singular')
    SongBooks = translate('OpenLP.Ui', 'Song Books', 'Plural')
    SureDeleteType = unicode(translate('OpenLP.Ui',
        'Are you sure you want to delete the selected %s?'))
    ThisTypeExists = unicode(translate('OpenLP.Ui', 'This %s already exists.'))
    Topic = translate('OpenLP.Ui', 'Topic', 'Singular')
    Topics = translate('OpenLP.Ui', 'Topics', 'Plural')
    TypeInList = unicode(translate('OpenLP.Ui',
        'This %s is already in the list.'))
    TypeMaintenance = unicode(translate('OpenLP.Ui', '%s Maintenance'))
    TypeNotExistAdd = unicode(translate('OpenLP.Ui',
        'This %s does not exist, do you want to add it?'))
