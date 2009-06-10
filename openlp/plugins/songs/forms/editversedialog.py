# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/raoul/Projects/openlp-2/resources/forms/editversedialog.ui'
#
# Created: Sat Mar  7 11:11:49 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from openlp.core.lib import translate

class Ui_EditVerseDialog(object):
    def setupUi(self, EditVerseDialog):
        EditVerseDialog.setObjectName(u'EditVerseDialog')
        EditVerseDialog.resize(492, 373)
        EditVerseDialog.setModal(True)
        self.DialogLayout = QtGui.QVBoxLayout(EditVerseDialog)
        self.DialogLayout.setSpacing(8)
        self.DialogLayout.setMargin(8)
        self.DialogLayout.setObjectName(u'DialogLayout')
        self.VerseTextEdit = QtGui.QTextEdit(EditVerseDialog)
        self.VerseTextEdit.setAcceptRichText(False)
        self.VerseTextEdit.setObjectName(u'VerseTextEdit')
        self.DialogLayout.addWidget(self.VerseTextEdit)
        self.ButtonBox = QtGui.QDialogButtonBox(EditVerseDialog)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.ButtonBox.setObjectName(u'ButtonBox')
        self.DialogLayout.addWidget(self.ButtonBox)

        self.retranslateUi(EditVerseDialog)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL(u'accepted()'), EditVerseDialog.accept)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL(u'rejected()'), EditVerseDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditVerseDialog)

    def retranslateUi(self, EditVerseDialog):
        EditVerseDialog.setWindowTitle(translate(u'EditVerseDialog', u'Dialog'))
