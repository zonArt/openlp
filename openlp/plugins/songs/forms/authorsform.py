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

from PyQt4 import QtGui, QtCore

from openlp.core.lib import translate
from openlp.core.lib.ui import critical_error_message_box
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
        self._autoDisplayName = False
        QtCore.QObject.connect(self.firstNameEdit,
            QtCore.SIGNAL(u'textEdited(QString)'),
            self.onFirstNameEditTextEdited)
        QtCore.QObject.connect(self.lastNameEdit,
            QtCore.SIGNAL(u'textEdited(QString)'),
            self.onLastNameEditTextEdited)

    def exec_(self, clear=True):
        if clear:
            self.firstNameEdit.clear()
            self.lastNameEdit.clear()
            self.displayEdit.clear()
        self.firstNameEdit.setFocus()
        return QtGui.QDialog.exec_(self)

    def onFirstNameEditTextEdited(self, text):
        if not self._autoDisplayName:
            return
        display_name = text
        if self.lastNameEdit.text() != u'':
            display_name = display_name + u' ' + self.lastNameEdit.text()
        self.displayEdit.setText(display_name)

    def onLastNameEditTextEdited(self, text):
        if not self._autoDisplayName:
            return
        display_name = text
        if self.firstNameEdit.text() != u'':
            display_name = self.firstNameEdit.text() + u' ' + display_name
        self.displayEdit.setText(display_name)

    def autoDisplayName(self):
        return self._autoDisplayName

    def setAutoDisplayName(self, on):
        self._autoDisplayName = on

    def accept(self):
        if not self.firstNameEdit.text():
            critical_error_message_box(
                message=translate('SongsPlugin.AuthorsForm',
                'You need to type in the first name of the author.'))
            self.firstNameEdit.setFocus()
            return False
        elif not self.lastNameEdit.text():
            critical_error_message_box(
                message=translate('SongsPlugin.AuthorsForm',
                'You need to type in the last name of the author.'))
            self.lastNameEdit.setFocus()
            return False
        elif not self.displayEdit.text():
            if critical_error_message_box(
                message=translate('SongsPlugin.AuthorsForm',
                'You have not set a display name for the '
                'author, combine the first and last names?'),
                parent=self, question=True) == QtGui.QMessageBox.Yes:
                self.displayEdit.setText(self.firstNameEdit.text() + \
                    u' ' + self.lastNameEdit.text())
                return QtGui.QDialog.accept(self)
            else:
                self.displayEdit.setFocus()
                return False
        else:
            return QtGui.QDialog.accept(self)
