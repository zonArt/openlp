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

from PyQt4 import QtGui

from openlp.core.lib import translate, Receiver
from openlp.plugins.songusage.lib.db import SongUsageItem
from songusagedeletedialog import Ui_SongUsageDeleteDialog

class SongUsageDeleteForm(QtGui.QDialog, Ui_SongUsageDeleteDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, manager, parent):
        """
        Constructor
        """
        self.manager = manager
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

    def accept(self):
        ret = QtGui.QMessageBox.question(self,
            translate('SongUsagePlugin.SongUsageDeleteForm',
                'Delete Selected Song Usage Events?'),
            translate('SongUsagePlugin.SongUsageDeleteForm',
                'Are you sure you want to delete selected Song Usage data?'),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok |
                QtGui.QMessageBox.Cancel),
            QtGui.QMessageBox.Cancel)
        if ret == QtGui.QMessageBox.Ok:
            deleteDate = self.deleteCalendar.selectedDate().toPyDate()
            self.manager.delete_all_objects(SongUsageItem,
                SongUsageItem.usagedate <= deleteDate)
            Receiver.send_message(u'openlp_information_message', {
                u'title': translate('SongUsagePlugin.SongUsageDeleteForm',
                'Deletion Successful'),
                u'message': translate('SongUsagePlugin.SongUsageDeleteForm',
                'All requested data has been deleted successfully. ')})
        self.close()
