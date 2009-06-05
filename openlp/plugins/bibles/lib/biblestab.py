# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

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

from PyQt4 import Qt, QtCore, QtGui

from openlp.core.lib import translate, str_to_bool
from openlp.core.lib import SettingsTab

class BiblesTab(SettingsTab):
    """
    BiblesTab is the Bibles settings tab in the settings dialog.
    """
    def __init__(self):
        self.paragraph_style = True
        self.show_new_chapters = False
        self.display_style = 0
        self.bible_search = True
        SettingsTab.__init__(self, translate(u'BiblesTab', u'Bibles'), u'Bibles')

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

        self.BibleThemeWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.BibleThemeWidget.setObjectName(u'BibleThemeWidget')
        self.BibleThemeLayout = QtGui.QHBoxLayout(self.BibleThemeWidget)
        self.BibleThemeLayout.setSpacing(8)
        self.BibleThemeLayout.setMargin(0)
        self.BibleThemeLayout.setObjectName(u'BibleThemeLayout')

        self.BibleThemeLabel = QtGui.QLabel(self.BibleThemeWidget)
        self.BibleThemeLabel.setObjectName(u'BibleThemeLabel')
        self.BibleThemeLayout.addWidget(self.BibleThemeLabel)
        self.BibleThemeComboBox = QtGui.QComboBox(self.BibleThemeWidget)
        self.BibleThemeComboBox.setObjectName(u'BibleThemeComboBox')
        self.BibleThemeComboBox.addItem(QtCore.QString())
        self.BibleThemeLayout.addWidget(self.BibleThemeComboBox)
        self.VerseDisplayLayout.addWidget(self.BibleThemeWidget, 3, 0, 1, 1)

        self.ChangeNoteLabel = QtGui.QLabel(self.VerseDisplayGroupBox)
        self.ChangeNoteLabel.setObjectName(u'ChangeNoteLabel')
        self.VerseDisplayLayout.addWidget(self.ChangeNoteLabel, 4, 0, 1, 1)
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
            QtCore.SIGNAL(u'stateChanged(int)'), self.onNewChaptersCheckBoxChanged)
        QtCore.QObject.connect(self.BibleSearchCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.onBibleSearchCheckBoxChanged)
        QtCore.QObject.connect(self.VerseRadioButton,
            QtCore.SIGNAL(u'pressed()'), self.onVerseRadioButtonPressed)
        QtCore.QObject.connect(self.ParagraphRadioButton,
            QtCore.SIGNAL(u'pressed()'), self.onParagraphRadioButtonPressed)
        QtCore.QObject.connect(self.DisplayStyleComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onDisplayStyleComboBoxChanged)
        QtCore.QObject.connect(self.BibleThemeComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onBibleThemeComboBoxChanged)

    def retranslateUi(self):
        self.VerseDisplayGroupBox.setTitle(translate(u'SettingsForm', u'Verse Display'))
        self.VerseRadioButton.setText(translate(u'SettingsForm', u'Verse style'))
        self.ParagraphRadioButton.setText(translate(u'SettingsForm', u'Paragraph style'))
        self.NewChaptersCheckBox.setText(translate(u'SettingsForm', u'Only show new chapter numbers'))
        self.DisplayStyleLabel.setText(translate(u'SettingsForm', u'Display Style:'))
        self.BibleThemeLabel.setText(translate(u'SettingsForm', u'Bible Theme:'))
        self.DisplayStyleComboBox.setItemText(0, translate(u'SettingsForm', u'No brackets'))
        self.DisplayStyleComboBox.setItemText(1, translate(u'SettingsForm', u'( and )'))
        self.DisplayStyleComboBox.setItemText(2, translate(u'SettingsForm', u'{ and }'))
        self.DisplayStyleComboBox.setItemText(3, translate(u'SettingsForm', u'[ and ]'))
        self.ChangeNoteLabel.setText(translate(u'SettingsForm', u'Note:\nChanges don\'t affect verses already in the service'))
        self.BibleSearchGroupBox.setTitle(translate(u'SettingsForm', u'Search'))
        self.BibleSearchCheckBox.setText(translate(u'SettingsForm', u'Search-as-you-type'))

    def onBibleThemeComboBoxChanged(self):
        self.bible_theme = self.BibleThemeComboBox.currentText()

    def onDisplayStyleComboBoxChanged(self):
        self.display_style = self.DisplayStyleComboBox.currentIndex()

    def onVerseRadioButtonPressed(self):
        self.paragraph_style = False

    def onParagraphRadioButtonPressed(self):
        self.paragraph_style = True

    def onNewChaptersCheckBoxChanged(self):
        check_state = self.NewChaptersCheckBox.checkState()
        self.show_new_chapters = False
        if check_state == 2: # we have a set value convert to True/False
            self.show_new_chapters = True

    def onBibleSearchCheckBoxChanged(self):
        check_state = self.BibleSearchCheckBox.checkState()
        self.bible_search = False
        if check_state == 2: # we have a set value convert to True/False
            self.bible_search = True

    def load(self):
        self.paragraph_style = str_to_bool(self.config.get_config(u'paragraph style', u'True'))
        self.show_new_chapters = str_to_bool(self.config.get_config(u'display new chapter', u'False'))
        self.display_style = int(self.config.get_config(u'display brackets', u'0'))
        self.bible_theme = self.config.get_config(u'bible theme', u'0')
        self.bible_search = str_to_bool(self.config.get_config(u'search as type', u'True'))
        if self.paragraph_style:
            self.ParagraphRadioButton.setChecked(True)
        else:
            self.VerseRadioButton.setChecked(True)
        self.NewChaptersCheckBox.setChecked(self.show_new_chapters)
        self.DisplayStyleComboBox.setCurrentIndex(self.display_style)
        self.BibleSearchCheckBox.setChecked(self.bible_search)

    def save(self):
        self.config.set_config(u'paragraph style', str(self.paragraph_style))
        self.config.set_config(u'display new chapter', str(self.show_new_chapters))
        self.config.set_config(u'display brackets', str(self.display_style))
        self.config.set_config(u'search as type', str(self.bible_search))
        self.config.set_config(u'bible theme', str(self.bible_theme))

    def updateThemeList(self, theme_list):
        """
        Called from ThemeManager when the Themes have changed
        """
        self.BibleThemeComboBox.clear()
        self.BibleThemeComboBox.addItem(u'')
        for theme in theme_list:
            self.BibleThemeComboBox.addItem(theme)
        id = self.BibleThemeComboBox.findText(str(self.bible_theme), QtCore.Qt.MatchExactly)
        if id == -1:
            # Not Found
            id = 0
            self.bible_theme = u''
        self.BibleThemeComboBox.setCurrentIndex(id)
