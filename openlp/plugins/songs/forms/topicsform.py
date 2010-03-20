# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

from openlp.plugins.songs.forms.topicsdialog import Ui_TopicsDialog

class TopicsForm(QtGui.QDialog, Ui_TopicsDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

    def exec_(self, clear=True):
        if clear:
            self.NameEdit.clear()
        self.NameEdit.setFocus()
        return QtGui.QDialog.exec_(self)

    def accept(self):
        if not self.NameEdit.text():
            QtGui.QMessageBox.critical(
                self, self.trUtf8('Error'),
                self.trUtf8('You need to type in a topic name!'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
            self.NameEdit.setFocus()
            return False
        else:
            return QtGui.QDialog.accept(self)
