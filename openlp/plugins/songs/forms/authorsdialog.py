# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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
from openlp.core.lib import translate

class Ui_AuthorsDialog(object):
    def setupUi(self, AuthorsForm):
        AuthorsForm.setObjectName(u'AuthorsDialog')
        AuthorsForm.resize(393, 147)
        self.AuthorsLayout = QtGui.QFormLayout(AuthorsForm)
        self.AuthorsLayout.setMargin(8)
        self.AuthorsLayout.setSpacing(8)
        self.AuthorsLayout.setObjectName(u'AuthorsLayout')
        self.FirstNameLabel = QtGui.QLabel(AuthorsForm)
        self.FirstNameLabel.setObjectName(u'FirstNameLabel')
        self.AuthorsLayout.setWidget(0,
            QtGui.QFormLayout.LabelRole, self.FirstNameLabel)
        self.FirstNameEdit = QtGui.QLineEdit(AuthorsForm)
        self.FirstNameEdit.setObjectName(u'FirstNameEdit')
        self.AuthorsLayout.setWidget(0,
            QtGui.QFormLayout.FieldRole, self.FirstNameEdit)
        self.LastNameLabel = QtGui.QLabel(AuthorsForm)
        self.LastNameLabel.setObjectName(u'LastNameLabel')
        self.AuthorsLayout.setWidget(1,
            QtGui.QFormLayout.LabelRole, self.LastNameLabel)
        self.LastNameEdit = QtGui.QLineEdit(AuthorsForm)
        self.LastNameEdit.setObjectName(u'LastNameEdit')
        self.AuthorsLayout.setWidget(1,
            QtGui.QFormLayout.FieldRole, self.LastNameEdit)
        self.DisplayLabel = QtGui.QLabel(AuthorsForm)
        self.DisplayLabel.setObjectName(u'DisplayLabel')
        self.AuthorsLayout.setWidget(2,
            QtGui.QFormLayout.LabelRole, self.DisplayLabel)
        self.DisplayEdit = QtGui.QLineEdit(AuthorsForm)
        self.DisplayEdit.setObjectName(u'DisplayEdit')
        self.AuthorsLayout.setWidget(2,
            QtGui.QFormLayout.FieldRole, self.DisplayEdit)
        self.AuthorButtonBox = QtGui.QDialogButtonBox(AuthorsForm)
        self.AuthorButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.AuthorButtonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.AuthorButtonBox.setObjectName(u'AuthorButtonBox')
        self.AuthorsLayout.setWidget(3,
            QtGui.QFormLayout.FieldRole, self.AuthorButtonBox)

        self.retranslateUi(AuthorsForm)
        QtCore.QObject.connect(self.AuthorButtonBox,
            QtCore.SIGNAL(u'accepted()'), AuthorsForm.accept)
        QtCore.QObject.connect(self.AuthorButtonBox,
            QtCore.SIGNAL(u'rejected()'), AuthorsForm.reject)
        QtCore.QMetaObject.connectSlotsByName(AuthorsForm)

    def retranslateUi(self, AuthorsForm):
        AuthorsForm.setWindowTitle(translate('AuthorsForm', 'Author Maintenance'))
        self.DisplayLabel.setText(translate('AuthorsForm', 'Display name:'))
        self.FirstNameLabel.setText(translate('AuthorsForm', 'First name:'))
        self.LastNameLabel.setText(translate('AuthorsForm', 'Last name:'))
