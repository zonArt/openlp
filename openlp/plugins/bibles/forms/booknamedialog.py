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

from openlp.core.lib import translate
from openlp.core.lib.ui import create_button_box

class Ui_BookNameDialog(object):
    def setupUi(self, bookNameDialog):
        bookNameDialog.setObjectName(u'bookNameDialog')
        bookNameDialog.resize(400, 271)
        self.bookNameLayout = QtGui.QVBoxLayout(bookNameDialog)
        self.bookNameLayout.setSpacing(8)
        self.bookNameLayout.setMargin(8)
        self.bookNameLayout.setObjectName(u'bookNameLayout')
        self.infoLabel = QtGui.QLabel(bookNameDialog)
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setObjectName(u'infoLabel')
        self.bookNameLayout.addWidget(self.infoLabel)
        self.correspondingLayout = QtGui.QGridLayout()
        self.correspondingLayout.setColumnStretch(1, 1)
        self.correspondingLayout.setSpacing(8)
        self.correspondingLayout.setObjectName(u'correspondingLayout')
        self.currentLabel = QtGui.QLabel(bookNameDialog)
        self.currentLabel.setObjectName(u'currentLabel')
        self.correspondingLayout.addWidget(self.currentLabel, 0, 0, 1, 1)
        self.currentBookLabel = QtGui.QLabel(bookNameDialog)
        self.currentBookLabel.setObjectName(u'currentBookLabel')
        self.correspondingLayout.addWidget(self.currentBookLabel, 0, 1, 1, 1)
        self.correspondingLabel = QtGui.QLabel(bookNameDialog)
        self.correspondingLabel.setObjectName(u'correspondingLabel')
        self.correspondingLayout.addWidget(self.correspondingLabel, 1, 0, 1, 1)
        self.correspondingComboBox = QtGui.QComboBox(bookNameDialog)
        self.correspondingComboBox.setObjectName(u'correspondingComboBox')
        self.correspondingLayout.addWidget(self.correspondingComboBox, 1, 1, 1, 1)
        self.bookNameLayout.addLayout(self.correspondingLayout)
        self.optionsGroupBox = QtGui.QGroupBox(bookNameDialog)
        self.optionsGroupBox.setObjectName(u'optionsGroupBox')
        self.optionsLayout = QtGui.QVBoxLayout(self.optionsGroupBox)
        self.optionsLayout.setSpacing(8)
        self.optionsLayout.setMargin(8)
        self.optionsLayout.setObjectName(u'optionsLayout')
        self.oldTestamentCheckBox = QtGui.QCheckBox(self.optionsGroupBox)
        self.oldTestamentCheckBox.setObjectName(u'oldTestamentCheckBox')
        self.oldTestamentCheckBox.setCheckState(QtCore.Qt.Checked)
        self.optionsLayout.addWidget(self.oldTestamentCheckBox)
        self.newTestamentCheckBox = QtGui.QCheckBox(self.optionsGroupBox)
        self.newTestamentCheckBox.setObjectName(u'newTestamentCheckBox')
        self.newTestamentCheckBox.setCheckState(QtCore.Qt.Checked)
        self.optionsLayout.addWidget(self.newTestamentCheckBox)
        self.apocryphaCheckBox = QtGui.QCheckBox(self.optionsGroupBox)
        self.apocryphaCheckBox.setObjectName(u'apocryphaCheckBox')
        self.apocryphaCheckBox.setCheckState(QtCore.Qt.Checked)
        self.optionsLayout.addWidget(self.apocryphaCheckBox)
        self.bookNameLayout.addWidget(self.optionsGroupBox)
        self.button_box = create_button_box(bookNameDialog, u'button_box', [u'cancel', u'ok'])
        self.bookNameLayout.addWidget(self.button_box)

        self.retranslateUi(bookNameDialog)

    def retranslateUi(self, bookNameDialog):
        bookNameDialog.setWindowTitle(translate('BiblesPlugin.BookNameDialog', 'Select Book Name'))
        self.infoLabel.setText(translate('BiblesPlugin.BookNameDialog',
            'The following book name cannot be matched up internally. '
            'Please select the corresponding name from the list.'))
        self.currentLabel.setText(translate('BiblesPlugin.BookNameDialog', 'Current name:'))
        self.correspondingLabel.setText(translate('BiblesPlugin.BookNameDialog', 'Corresponding name:'))
        self.optionsGroupBox.setTitle(translate('BiblesPlugin.BookNameDialog', 'Show Books From'))
        self.oldTestamentCheckBox.setText(translate('BiblesPlugin.BookNameDialog', 'Old Testament'))
        self.newTestamentCheckBox.setText(translate('BiblesPlugin.BookNameDialog', 'New Testament'))
        self.apocryphaCheckBox.setText(translate('BiblesPlugin.BookNameDialog', 'Apocrypha'))
