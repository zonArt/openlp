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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, SpellTextEdit

class Ui_CustomSlideEditDialog(object):
    def setupUi(self, customSlideEditDialog):
        customSlideEditDialog.setObjectName(u'customSlideEditDialog')
        customSlideEditDialog.resize(474, 442)
        self.buttonBox = QtGui.QDialogButtonBox(customSlideEditDialog)
        self.buttonBox.setGeometry(QtCore.QRect(8, 407, 458, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(u'buttonBox')
        self.slideTextEdit = SpellTextEdit(self)
        self.slideTextEdit.setGeometry(QtCore.QRect(8, 8, 458, 349))
        self.slideTextEdit.setObjectName(u'slideTextEdit')
        self.splitButton = QtGui.QPushButton(customSlideEditDialog)
        self.splitButton.setGeometry(QtCore.QRect(380, 370, 85, 27))
        self.splitButton.setObjectName(u'splitButton')
        self.retranslateUi(customSlideEditDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'accepted()'),
            customSlideEditDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'rejected()'),
            customSlideEditDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(customSlideEditDialog)

    def retranslateUi(self, customSlideEditDialog):
        self.splitButton.setText(
            translate('CustomPlugin.EditCustomForm', 'Split Slide'))
        self.splitButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Split a slide into two '
            'by inserting a slide splitter.'))