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

from openlp.core.lib import Registry, translate
from openlp.plugins.songusage.lib.db import SongUsageItem
from .songusagedeletedialog import Ui_SongUsageDeleteDialog


class SongUsageDeleteForm(QtGui.QDialog, Ui_SongUsageDeleteDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, manager, parent):
        """
        Constructor
        """
        self.manager = manager
        super(SongUsageDeleteForm, self).__init__(parent)
        self.setupUi(self)
        self.button_box.clicked.connect(self.on_button_box_clicked)

    def on_button_box_clicked(self, button):
        if self.button_box.standardButton(button) == QtGui.QDialogButtonBox.Ok:
            ret = QtGui.QMessageBox.question(self,
                translate('SongUsagePlugin.SongUsageDeleteForm', 'Delete Selected Song Usage Events?'),
                translate('SongUsagePlugin.SongUsageDeleteForm',
                    'Are you sure you want to delete selected Song Usage data?'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No), QtGui.QMessageBox.No)
            if ret == QtGui.QMessageBox.Yes:
                delete_date = self.delete_calendar.selectedDate().toPyDate()
                self.manager.delete_all_objects(SongUsageItem, SongUsageItem.usagedate <= delete_date)
                self.main_window.information_message(
                    translate('SongUsagePlugin.SongUsageDeleteForm', 'Deletion Successful'),
                    translate(
                        'SongUsagePlugin.SongUsageDeleteForm', 'All requested data has been deleted successfully.')
                )
                self.accept()
        else:
            self.reject()

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, '_main_window'):
            self._main_window = Registry().get('main_window')
        return self._main_window

    main_window = property(_get_main_window)
