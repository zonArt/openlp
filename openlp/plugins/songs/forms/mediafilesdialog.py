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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, build_icon
from openlp.core.lib.ui import create_button_box


class Ui_MediaFilesDialog(object):
    """
    The user interface for the media files dialog.
    """
    def setupUi(self, media_files_dialog):
        """
        Set up the user interface.
        """
        media_files_dialog.setObjectName('media_files_dialog')
        media_files_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        media_files_dialog.resize(400, 300)
        media_files_dialog.setModal(True)
        media_files_dialog.setWindowIcon(build_icon(':/icon/openlp-logo-16x16.png'))
        self.files_vertical_layout = QtGui.QVBoxLayout(media_files_dialog)
        self.files_vertical_layout.setSpacing(8)
        self.files_vertical_layout.setMargin(8)
        self.files_vertical_layout.setObjectName('files_vertical_layout')
        self.select_label = QtGui.QLabel(media_files_dialog)
        self.select_label.setWordWrap(True)
        self.select_label.setObjectName('select_label')
        self.files_vertical_layout.addWidget(self.select_label)
        self.file_list_widget = QtGui.QListWidget(media_files_dialog)
        self.file_list_widget.setAlternatingRowColors(True)
        self.file_list_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.file_list_widget.setObjectName('file_list_widget')
        self.files_vertical_layout.addWidget(self.file_list_widget)
        self.button_box = create_button_box(media_files_dialog, 'button_box', ['cancel', 'ok'])
        self.files_vertical_layout.addWidget(self.button_box)
        self.retranslateUi(media_files_dialog)

    def retranslateUi(self, media_files_dialog):
        """
        Translate the UI on the fly.
        """
        media_files_dialog.setWindowTitle(translate('SongsPlugin.MediaFilesForm', 'Select Media File(s)'))
        self.select_label.setText(translate('SongsPlugin.MediaFilesForm',
            'Select one or more audio files from the list below, and click OK to import them into this song.'))

