# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate

class Ui_ExceptionDialog(object):
    def setupUi(self, exceptionDialog):
        exceptionDialog.setObjectName(u'exceptionDialog')
        exceptionDialog.resize(580, 407)
        self.exceptionLayout = QtGui.QVBoxLayout(exceptionDialog)
        self.exceptionLayout.setSpacing(8)
        self.exceptionLayout.setMargin(8)
        self.exceptionLayout.setObjectName(u'exceptionLayout')
        self.messageLayout = QtGui.QHBoxLayout()
        self.messageLayout.setSpacing(0)
        self.messageLayout.setContentsMargins(0, -1, 0, -1)
        self.messageLayout.setObjectName(u'messageLayout')
        self.bugLabel = QtGui.QLabel(exceptionDialog)
        self.bugLabel.setMinimumSize(QtCore.QSize(64, 64))
        self.bugLabel.setMaximumSize(QtCore.QSize(64, 64))
        self.bugLabel.setText(u'')
        self.bugLabel.setPixmap(QtGui.QPixmap(u':/graphics/exception.png'))
        self.bugLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.bugLabel.setObjectName(u'bugLabel')
        self.messageLayout.addWidget(self.bugLabel)
        self.messageLabel = QtGui.QLabel(exceptionDialog)
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setObjectName(u'messageLabel')
        self.messageLayout.addWidget(self.messageLabel)
        self.exceptionLayout.addLayout(self.messageLayout)
        self.exceptionTextEdit = QtGui.QPlainTextEdit(exceptionDialog)
        self.exceptionTextEdit.setReadOnly(True)
        self.exceptionTextEdit.setBackgroundVisible(False)
        self.exceptionTextEdit.setObjectName(u'exceptionTextEdit')
        self.exceptionLayout.addWidget(self.exceptionTextEdit)
        self.exceptionButtonBox = QtGui.QDialogButtonBox(exceptionDialog)
        self.exceptionButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.exceptionButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.exceptionButtonBox.setObjectName(u'exceptionButtonBox')
        self.exceptionLayout.addWidget(self.exceptionButtonBox)

        self.retranslateUi(exceptionDialog)
        QtCore.QObject.connect(self.exceptionButtonBox,
            QtCore.SIGNAL(u'accepted()'), exceptionDialog.accept)
        QtCore.QObject.connect(self.exceptionButtonBox,
            QtCore.SIGNAL(u'rejected()'), exceptionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(exceptionDialog)

    def retranslateUi(self, exceptionDialog):
        exceptionDialog.setWindowTitle(
            translate('OpenLP.ExceptionDialog', 'Error Occured'))
        self.messageLabel.setText(translate('OpenLP.ExceptionDialog', 'Oops! '
            'OpenLP hit a problem, and couldn\'t recover. The text in the box '
            'below contains information that might be helpful to the OpenLP '
            'developers, so please e-mail it to bugs@openlp.org, along with a '
            'detailed description of what you were doing when the problem '
            'occurred.'))
