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

class Ui_EditVerseDialog(object):
    def setupUi(self, EditVerseForm):
        EditVerseForm.setObjectName(u'EditVerseDialog')
        EditVerseForm.resize(500, 521)
        EditVerseForm.setModal(True)
        self.layoutWidget = QtGui.QWidget(EditVerseForm)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 1, 471, 491))
        self.layoutWidget.setObjectName(u'layoutWidget')
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u'verticalLayout_3')
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.VerseTypeLabel = QtGui.QLabel(self.layoutWidget)
        self.VerseTypeLabel.setTextFormat(QtCore.Qt.PlainText)
        self.VerseTypeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.VerseTypeLabel.setObjectName(u'VerseTypeLabel')
        self.verticalLayout.addWidget(self.VerseTypeLabel)
        self.VerseListComboBox = QtGui.QComboBox(self.layoutWidget)
        self.VerseListComboBox.setObjectName(u'VerseListComboBox')
        self.VerseListComboBox.addItem(u'')
        self.VerseListComboBox.addItem(u'')
        self.VerseListComboBox.addItem(u'')
        self.VerseListComboBox.addItem(u'')
        self.VerseListComboBox.addItem(u'')
        self.VerseListComboBox.addItem(u'')
        self.VerseListComboBox.addItem(u'')
        self.verticalLayout.addWidget(self.VerseListComboBox)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(u'verticalLayout_2')
        self.VerseNumberLabel = QtGui.QLabel(self.layoutWidget)
        self.VerseNumberLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.VerseNumberLabel.setObjectName(u'VerseNumberLabel')
        self.verticalLayout_2.addWidget(self.VerseNumberLabel)
        self.SubVerseListComboBox = QtGui.QComboBox(self.layoutWidget)
        self.SubVerseListComboBox.setObjectName(u'SubVerseListComboBox')
        self.verticalLayout_2.addWidget(self.SubVerseListComboBox)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.VerseTextEdit = QtGui.QTextEdit(self.layoutWidget)
        self.VerseTextEdit.setAcceptRichText(False)
        self.VerseTextEdit.setObjectName(u'VerseTextEdit')
        self.verticalLayout_3.addWidget(self.VerseTextEdit)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u'horizontalLayout_2')
        self.addBridge = QtGui.QPushButton(self.layoutWidget)
        self.addBridge.setObjectName(u'addBridge')
        self.horizontalLayout_2.addWidget(self.addBridge)
        self.addVerse = QtGui.QPushButton(self.layoutWidget)
        self.addVerse.setObjectName(u'addVerse')
        self.horizontalLayout_2.addWidget(self.addVerse)
        self.addChorus = QtGui.QPushButton(self.layoutWidget)
        self.addChorus.setObjectName(u'addChorus')
        self.horizontalLayout_2.addWidget(self.addChorus)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u'horizontalLayout_3')
        self.addPreChorus = QtGui.QPushButton(self.layoutWidget)
        self.addPreChorus.setObjectName(u'addPreChorus')
        self.horizontalLayout_3.addWidget(self.addPreChorus)
        self.addIntro = QtGui.QPushButton(self.layoutWidget)
        self.addIntro.setObjectName(u'addIntro')
        self.horizontalLayout_3.addWidget(self.addIntro)
        self.addOther = QtGui.QPushButton(self.layoutWidget)
        self.addOther.setObjectName(u'addOther')
        self.horizontalLayout_3.addWidget(self.addOther)
        self.addEnding = QtGui.QPushButton(self.layoutWidget)
        self.addEnding.setObjectName(u'addEnding')
        self.horizontalLayout_3.addWidget(self.addEnding)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.ButtonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.ButtonBox.setObjectName(u'ButtonBox')
        self.verticalLayout_3.addWidget(self.ButtonBox)

        self.retranslateUi(EditVerseForm)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL(u'accepted()'), EditVerseForm.accept)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL(u'rejected()'), EditVerseForm.reject)
        QtCore.QMetaObject.connectSlotsByName(EditVerseForm)

    def retranslateUi(self, EditVerseForm):
        EditVerseForm.setWindowTitle(translate('EditVerseForm', 'Edit Verse'))
        self.VerseTypeLabel.setText(translate('EditVerseForm', 'Verse Type'))
        self.VerseListComboBox.setItemText(0, translate('EditVerseForm', 'Intro'))
        self.VerseListComboBox.setItemText(1, translate('EditVerseForm', 'Verse'))
        self.VerseListComboBox.setItemText(2, translate('EditVerseForm', 'Pre-Chorus'))
        self.VerseListComboBox.setItemText(3, translate('EditVerseForm', 'Chorus'))
        self.VerseListComboBox.setItemText(4, translate('EditVerseForm', 'Bridge'))
        self.VerseListComboBox.setItemText(5, translate('EditVerseForm', 'Ending'))
        self.VerseListComboBox.setItemText(6, translate('EditVerseForm', 'Other'))
        self.VerseNumberLabel.setText(translate('EditVerseForm', 'Number'))
        self.addBridge.setText(translate('EditVerseForm', 'Bridge'))
        self.addVerse.setText(translate('EditVerseForm', 'Verse'))
        self.addChorus.setText(translate('EditVerseForm', 'Chorus'))
        self.addPreChorus.setText(translate('EditVerseForm', 'Pre-Chorus'))
        self.addIntro.setText(translate('EditVerseForm', 'Intro'))
        self.addOther.setText(translate('EditVerseForm', 'Other'))
        self.addEnding.setText(translate('EditVerseForm', 'Ending'))

