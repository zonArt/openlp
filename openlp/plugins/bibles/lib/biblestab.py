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
        self.BibleLayout = QtGui.QHBoxLayout(self)
        self.BibleLayout.setSpacing(8)
        self.BibleLayout.setMargin(8)
        self.BibleLayout.setObjectName(u'BibleLayout')
        self.BibleLeftWidget = QtGui.QWidget(self)
        self.BibleLeftWidget.setObjectName(u'BibleLeftWidget')
        self.BibleLeftLayout = QtGui.QVBoxLayout(self.BibleLeftWidget)
        self.BibleLeftLayout.setObjectName(u'BibleLeftLayout')
        self.BibleLeftLayout.setSpacing(8)
        self.BibleLeftLayout.setMargin(0)
        self.VerseDisplayGroupBox = QtGui.QGroupBox(self)
        self.VerseDisplayGroupBox.setObjectName(u'VerseDisplayGroupBox')
        self.VerseDisplayLayout = QtGui.QGridLayout(self.VerseDisplayGroupBox)
        self.VerseDisplayLayout.setMargin(8)
        self.VerseDisplayLayout.setObjectName(u'VerseDisplayLayout')
        self.VerseTypeWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.VerseTypeWidget.setObjectName(u'VerseTypeWidget')
        self.VerseTypeLayout = QtGui.QHBoxLayout(self.VerseTypeWidget)
        self.VerseTypeLayout.setSpacing(8)
        self.VerseTypeLayout.setMargin(0)
        self.VerseTypeLayout.setObjectName(u'VerseTypeLayout')
        self.VerseRadioButton = QtGui.QRadioButton(self.VerseTypeWidget)
        self.VerseRadioButton.setObjectName(u'VerseRadioButton')
        self.VerseTypeLayout.addWidget(self.VerseRadioButton)
        self.ParagraphRadioButton = QtGui.QRadioButton(self.VerseTypeWidget)
        self.ParagraphRadioButton.setObjectName(u'ParagraphRadioButton')
        self.VerseTypeLayout.addWidget(self.ParagraphRadioButton)
        self.VerseDisplayLayout.addWidget(self.VerseTypeWidget, 0, 0, 1, 1)
        self.NewChaptersCheckBox = QtGui.QCheckBox(self.VerseDisplayGroupBox)
        self.NewChaptersCheckBox.setObjectName("NewChaptersCheckBox")
        self.VerseDisplayLayout.addWidget(self.NewChaptersCheckBox, 1, 0, 1, 1)
        self.DisplayStyleWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.DisplayStyleWidget.setObjectName(u'DisplayStyleWidget')
        self.DisplayStyleLayout = QtGui.QHBoxLayout(self.DisplayStyleWidget)
        self.DisplayStyleLayout.setSpacing(8)
        self.DisplayStyleLayout.setMargin(0)
        self.DisplayStyleLayout.setObjectName(u'DisplayStyleLayout')
        self.DisplayStyleLabel = QtGui.QLabel(self.DisplayStyleWidget)
        self.DisplayStyleLabel.setObjectName(u'DisplayStyleLabel')
        self.DisplayStyleLayout.addWidget(self.DisplayStyleLabel)
        self.DisplayStyleComboBox = QtGui.QComboBox(self.DisplayStyleWidget)
        self.DisplayStyleComboBox.setObjectName(u'DisplayStyleComboBox')
        self.DisplayStyleComboBox.addItem(QtCore.QString())
        self.DisplayStyleComboBox.addItem(QtCore.QString())
        self.DisplayStyleComboBox.addItem(QtCore.QString())
        self.DisplayStyleComboBox.addItem(QtCore.QString())
        self.DisplayStyleLayout.addWidget(self.DisplayStyleComboBox)
        self.VerseDisplayLayout.addWidget(self.DisplayStyleWidget, 2, 0, 1, 1)
        self.ChangeNoteLabel = QtGui.QLabel(self.VerseDisplayGroupBox)
        self.ChangeNoteLabel.setObjectName(u'ChangeNoteLabel')
        self.VerseDisplayLayout.addWidget(self.ChangeNoteLabel, 3, 0, 1, 1)
        self.BibleLeftLayout.addWidget(self.VerseDisplayGroupBox)
        self.BibleLeftSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.BibleLeftLayout.addItem(self.BibleLeftSpacer)
        self.BibleLayout.addWidget(self.BibleLeftWidget)

        self.BibleRightWidget = QtGui.QWidget(self)
        self.BibleRightWidget.setObjectName(u'BibleRightWidget')
        self.BibleRightLayout = QtGui.QVBoxLayout(self.BibleRightWidget)
        self.BibleRightLayout.setObjectName(u'BibleRightLayout')
        self.BibleRightLayout.setSpacing(8)
        self.BibleRightLayout.setMargin(0)
        self.BibleSearchGroupBox = QtGui.QGroupBox(self)
        self.BibleSearchGroupBox.setObjectName(u'BibleSearchGroupBox')
        self.BibleSearchLayout = QtGui.QVBoxLayout(self.BibleSearchGroupBox)
        self.BibleSearchLayout.setObjectName(u'BibleSearchLayout')
        self.BibleSearchLayout.setSpacing(8)
        self.BibleSearchLayout.setMargin(8)
        self.BibleSearchCheckBox = QtGui.QCheckBox(self.BibleSearchGroupBox)
        self.BibleSearchCheckBox.setObjectName(u'BibleSearchCheckBox')
        self.BibleSearchLayout.addWidget(self.BibleSearchCheckBox)
        self.BibleRightLayout.addWidget(self.BibleSearchGroupBox)
        self.BibleRightSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.BibleRightLayout.addItem(self.BibleRightSpacer)
        self.BibleLayout.addWidget(self.BibleRightWidget)
        # Signals and slots
        QtCore.QObject.connect(self.NewChaptersCheckBox,
            QtCore.SIGNAL("stateChanged(int)"), self.onNewChaptersCheckBoxChanged)
        QtCore.QObject.connect(self.BibleSearchCheckBox,
            QtCore.SIGNAL("stateChanged(int)"), self.onBibleSearchCheckBoxChanged)
        QtCore.QObject.connect(self.VerseRadioButton,
            QtCore.SIGNAL("pressed()"), self.onVerseRadioButtonPressed)
        QtCore.QObject.connect(self.ParagraphRadioButton,
            QtCore.SIGNAL("pressed()"), self.onParagraphRadioButtonPressed)
        QtCore.QObject.connect(self.DisplayStyleComboBox,
            QtCore.SIGNAL("activated(int)"), self.onDisplayStyleComboBoxChanged)            

    def retranslateUi(self):
        self.VerseDisplayGroupBox.setTitle(translate('SettingsForm', 'Verse Display'))
        self.VerseRadioButton.setText(translate('SettingsForm', 'Verse style'))
        self.ParagraphRadioButton.setText(translate('SettingsForm','Paragraph style'))
        self.NewChaptersCheckBox.setText(translate('SettingsForm', 'Only show new chapter numbers'))
        self.DisplayStyleLabel.setText(translate('SettingsForm', 'Display Style:'))
        self.DisplayStyleComboBox.setItemText(0, translate('SettingsForm', 'No brackets'))
        self.DisplayStyleComboBox.setItemText(1, translate('SettingsForm', '( and )'))
        self.DisplayStyleComboBox.setItemText(2, translate('SettingsForm', '{ and }'))
        self.DisplayStyleComboBox.setItemText(3, translate('SettingsForm', '[ and ]'))
        self.ChangeNoteLabel.setText(translate('SettingsForm', 'Note:\nChanges don\'t affect verses already in the service'))
        self.BibleSearchGroupBox.setTitle(translate('SettingsForm', 'Search'))
        self.BibleSearchCheckBox.setText(translate('SettingsForm', 'Search-as-you-type'))

    def onDisplayStyleComboBoxChanged(self):
        self.display_style = self.DisplayStyleComboBox.currentIndex()
        
    def onVerseRadioButtonPressed(self):
        self.paragraph_style = False

    def onParagraphRadioButtonPressed(self):
        self.paragraph_style = True

    def onNewChaptersCheckBoxChanged(self):
        check_box = self.NewChaptersCheckBox.checkState()
        self.new_chapter_check = False
        if check_box == 2: # we have a set value convert to True/False
            self.new_chapter_check = True
            
    def onBibleSearchCheckBoxChanged(self):
        bible_search = self.BibleSearchCheckBox.checkState()
        self.bible_search_check = False
        if bible_search == 2: # we have a set value convert to True/False
            self.bible_search_check = True            

    def load(self):
        self.paragraph_style = self.convertStringToBoolean(self.config.get_config('paragraph style', u'True'))
        self.new_chapter_check = self.convertStringToBoolean(self.config.get_config('display new chapter', u"False"))
        self.display_style = int(self.config.get_config('display brackets', '0'))
        self.search_as_type = self.convertStringToBoolean(self.config.get_config('search as type', u'True'))   
        if self.paragraph_style:
            self.ParagraphRadioButton.setChecked(True)
        else:
            self.VerseRadioButton.setChecked(True)
        if self.new_chapter_check:
            self.NewChaptersCheckBox.setChecked(True)
        self.DisplayStyleComboBox.setCurrentIndex(self.display_style)
        if self.search_as_type:   
            self.BibleSearchCheckBox.setChecked(True)

    def save(self):
        self.config.set_config("paragraph style", str(self.paragraph_style))
        self.config.set_config("display new chapter", str(self.new_chapter_check))
        self.config.set_config("display brackets", str(self.display_style))
        self.config.set_config("search as type", str(self.bible_search_check))

