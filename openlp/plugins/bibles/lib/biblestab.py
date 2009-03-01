# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

from PyQt4 import QtCore, QtGui

from openlp.core import translate
from openlp.core.lib import SettingsTab
from openlp.core.resources import *

class BiblesTab(SettingsTab):
    """
    BiblesTab is the Bibles settings tab in the settings dialog.
    """
    def __init__(self):
        SettingsTab.__init__(self, u'Bibles')

    def setupUi(self):
        self.setObjectName(u'BiblesTab')

        self.formLayout_3 = QtGui.QFormLayout(self)
        self.formLayout_3.setObjectName("formLayout_3")
        self.VerseDisplayGroupBox = QtGui.QGroupBox(self)
        self.VerseDisplayGroupBox.setObjectName("VerseDisplayGroupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.VerseDisplayGroupBox)
        self.gridLayout_2.setMargin(8)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.VerseTypeWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.VerseTypeWidget.setObjectName("VerseTypeWidget")
        self.VerseTypeLayout = QtGui.QHBoxLayout(self.VerseTypeWidget)
        self.VerseTypeLayout.setSpacing(8)
        self.VerseTypeLayout.setMargin(0)
        self.VerseTypeLayout.setObjectName("VerseTypeLayout")
        self.VerseRadioButton = QtGui.QRadioButton(self.VerseTypeWidget)
        self.VerseRadioButton.setObjectName("VerseRadioButton")
        self.VerseTypeLayout.addWidget(self.VerseRadioButton)
        self.ParagraphRadioButton = QtGui.QRadioButton(self.VerseTypeWidget)
        self.ParagraphRadioButton.setChecked(True)
        self.ParagraphRadioButton.setObjectName("ParagraphRadioButton")
        self.VerseTypeLayout.addWidget(self.ParagraphRadioButton)
        self.gridLayout_2.addWidget(self.VerseTypeWidget, 0, 0, 1, 1)
        self.NewChaptersCheckBox = QtGui.QCheckBox(self.VerseDisplayGroupBox)
        self.NewChaptersCheckBox.setObjectName("NewChaptersCheckBox")
        self.gridLayout_2.addWidget(self.NewChaptersCheckBox, 1, 0, 1, 1)
        self.DisplayStyleWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.DisplayStyleWidget.setObjectName("DisplayStyleWidget")
        self.DisplayStyleLayout = QtGui.QHBoxLayout(self.DisplayStyleWidget)
        self.DisplayStyleLayout.setSpacing(8)
        self.DisplayStyleLayout.setMargin(0)
        self.DisplayStyleLayout.setObjectName("DisplayStyleLayout")
        self.DisplayStyleLabel = QtGui.QLabel(self.DisplayStyleWidget)
        self.DisplayStyleLabel.setObjectName("DisplayStyleLabel")
        self.DisplayStyleLayout.addWidget(self.DisplayStyleLabel)
        self.DisplayStyleComboBox = QtGui.QComboBox(self.DisplayStyleWidget)
        self.DisplayStyleComboBox.setObjectName("DisplayStyleComboBox")
        self.DisplayStyleComboBox.addItem(QtCore.QString())
        self.DisplayStyleComboBox.addItem(QtCore.QString())
        self.DisplayStyleComboBox.addItem(QtCore.QString())
        self.DisplayStyleComboBox.addItem(QtCore.QString())
        self.DisplayStyleLayout.addWidget(self.DisplayStyleComboBox)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.DisplayStyleLayout.addItem(spacerItem6)
        self.gridLayout_2.addWidget(self.DisplayStyleWidget, 2, 0, 1, 1)
        self.ChangeNoteLabel = QtGui.QLabel(self.VerseDisplayGroupBox)
        self.ChangeNoteLabel.setObjectName("ChangeNoteLabel")
        self.gridLayout_2.addWidget(self.ChangeNoteLabel, 3, 0, 1, 1)
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.VerseDisplayGroupBox)
        self.SearchGroupBox_2 = QtGui.QGroupBox(self)
        self.SearchGroupBox_2.setObjectName("SearchGroupBox_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.SearchGroupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.SearchCheckBox_2 = QtGui.QCheckBox(self.SearchGroupBox_2)
        self.SearchCheckBox_2.setChecked(True)
        self.SearchCheckBox_2.setObjectName("SearchCheckBox_2")
        self.verticalLayout_2.addWidget(self.SearchCheckBox_2)
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.SearchGroupBox_2)


    def retranslateUi(self):        
        self.VerseDisplayGroupBox.setTitle(translate("SettingsForm", "Verse Display"))
        self.VerseRadioButton.setText(translate("SettingsForm", "Verse style"))
        self.ParagraphRadioButton.setText(translate("SettingsForm", "Paragraph style"))
        self.NewChaptersCheckBox.setText(translate("SettingsForm", "Only show new chapter numbers"))
        self.DisplayStyleLabel.setText(translate("SettingsForm", "Display Style:"))
        self.DisplayStyleComboBox.setItemText(0, translate("SettingsForm", "No brackets"))
        self.DisplayStyleComboBox.setItemText(1, translate("SettingsForm", "( and )"))
        self.DisplayStyleComboBox.setItemText(2, translate("SettingsForm", "{ and }"))
        self.DisplayStyleComboBox.setItemText(3, translate("SettingsForm", "[ and ]"))
        self.ChangeNoteLabel.setText(translate("SettingsForm", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Changes don\'t affect verses already in the service</span></p></body></html>"))
        self.SearchGroupBox_2.setTitle(translate("SettingsForm", "Search"))
        self.SearchCheckBox_2.setText(translate("SettingsForm", "Enabled search-as-you-type"))
