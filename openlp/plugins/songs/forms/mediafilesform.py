# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Eric Ludin, Edwin Lunando, Brian T. Meyer,    #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky                                             #
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

import logging
import os

from PyQt4 import QtCore, QtGui

from mediafilesdialog import Ui_MediaFilesDialog

log = logging.getLogger(__name__)

class MediaFilesForm(QtGui.QDialog, Ui_MediaFilesDialog):
    """
    Class to show a list of files from the
    """
    log.info(u'%s MediaFilesForm loaded', __name__)

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

    def populateFiles(self, files):
        self.fileListWidget.clear()
        for file in files:
            item = QtGui.QListWidgetItem(os.path.split(file)[1])
            item.setData(QtCore.Qt.UserRole, file)
            self.fileListWidget.addItem(item)

    def getSelectedFiles(self):
        return map(lambda x: unicode(x.data(QtCore.Qt.UserRole).toString()),
            self.fileListWidget.selectedItems())

