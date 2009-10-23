# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from PyQt4 import QtGui, QtCore
from openlp.core.lib import translate
from openlp.plugins.songs.forms.authorsdialog import Ui_AuthorsDialog

class AuthorsForm(QtGui.QDialog, Ui_AuthorsDialog):
    """
    Class to control the Maintenance of Authors Dialog
    """
    def __init__(self, parent=None):
        """
        Set up the screen and common data
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.autoDisplayName = False
        QtCore.QObject.connect(self.FirstNameEdit,
            QtCore.SIGNAL(u'textEdited(QString)'), self.onFirstNameEditTextEdited)
        QtCore.QObject.connect(self.LastNameEdit,
            QtCore.SIGNAL(u'textEdited(QString)'), self.onLastNameEditTextEdited)

    def exec_(self, clear=True):
        if clear:
            self.FirstNameEdit.clear()
            self.LastNameEdit.clear()
            self.DisplayEdit.clear()
        self.FirstNameEdit.setFocus()
        return QtGui.QDialog.exec_(self)

    def onFirstNameEditTextEdited(self, text):
        if not self.autoDisplayName:
            return
        display_name = text
        if self.LastNameEdit.text() != u'':
            display_name = display_name + u' ' + self.LastNameEdit.text()
        self.DisplayEdit.setText(display_name)

    def onLastNameEditTextEdited(self, text):
        if not self.autoDisplayName:
            return
        display_name = text
        if self.FirstNameEdit.text() != u'':
            display_name = self.FirstNameEdit.text() + u' ' + display_name
        self.DisplayEdit.setText(display_name)

    def autoDisplayName(self):
        return self.autoDisplayName

    def setAutoDisplayName(self, on):
        self.autoDisplayName = on

    def accept(self):
        if not self.FirstNameEdit.text():
            QtGui.QMessageBox.critical(
                self, self.trUtf8(u'Error'),
                self.trUtf8(u'You need to type in the first name of the author.'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
            self.FirstNameEdit.setFocus()
            return False
        elif not self.LastNameEdit.text():
            QtGui.QMessageBox.critical(
                self, self.trUtf8(u'Error'),
                self.trUtf8(u'You need to type in the last name of the author.'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
            self.LastNameEdit.setFocus()
            return False
        elif not self.DisplayEdit.text():
            if QtGui.QMessageBox.critical(
                    self, self.trUtf8(u'Error'),
                    self.trUtf8(u'You haven\'t set a display name for the '
                        u'author, would you like me to combine the first and '
                        u'last names for you?'),
                    QtGui.QMessageBox.StandardButtons(
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                    ) == QtGui.QMessageBox.Yes:
                self.DisplayEdit.setText(self.FirstNameEdit.text() + \
                    u' ' + self.LastNameEdit.text())
                return QtGui.QDialog.accept(self)
            else:
                self.DisplayEdit.setFocus()
                return False
        else:
            return QtGui.QDialog.accept(self)

