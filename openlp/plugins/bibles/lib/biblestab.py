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

import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, SettingsTab, Settings, UiStrings, translate
from openlp.core.lib.ui import find_and_set_in_combo_box
from openlp.plugins.bibles.lib import LayoutStyle, DisplayStyle, update_reference_separators, \
    get_reference_separator, LanguageSelection

log = logging.getLogger(__name__)

class BiblesTab(SettingsTab):
    """
    BiblesTab is the Bibles settings tab in the settings dialog.
    """
    log.info(u'Bible Tab loaded')

    def __init__(self, parent, title, visible_title, icon_path):
        self.paragraph_style = True
        self.show_new_chapters = False
        self.display_style = 0
        SettingsTab.__init__(self, parent, title, visible_title, icon_path)

    def setupUi(self):
        self.setObjectName(u'BiblesTab')
        SettingsTab.setupUi(self)
        self.verseDisplayGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.verseDisplayGroupBox.setObjectName(u'verseDisplayGroupBox')
        self.verseDisplayLayout = QtGui.QFormLayout(self.verseDisplayGroupBox)
        self.verseDisplayLayout.setObjectName(u'verseDisplayLayout')
        self.newChaptersCheckBox = QtGui.QCheckBox(self.verseDisplayGroupBox)
        self.newChaptersCheckBox.setObjectName(u'newChaptersCheckBox')
        self.verseDisplayLayout.addRow(self.newChaptersCheckBox)
        self.displayStyleLabel = QtGui.QLabel(self.verseDisplayGroupBox)
        self.displayStyleLabel.setObjectName(u'displayStyleLabel')
        self.displayStyleComboBox = QtGui.QComboBox(self.verseDisplayGroupBox)
        self.displayStyleComboBox.addItems([u'', u'', u'', u''])
        self.displayStyleComboBox.setObjectName(u'displayStyleComboBox')
        self.verseDisplayLayout.addRow(self.displayStyleLabel, self.displayStyleComboBox)
        self.layoutStyleLabel = QtGui.QLabel(self.verseDisplayGroupBox)
        self.layoutStyleLabel.setObjectName(u'layoutStyleLabel')
        self.layoutStyleComboBox = QtGui.QComboBox(self.verseDisplayGroupBox)
        self.layoutStyleComboBox.setObjectName(u'layoutStyleComboBox')
        self.layoutStyleComboBox.addItems([u'', u'', u''])
        self.verseDisplayLayout.addRow(self.layoutStyleLabel, self.layoutStyleComboBox)
        self.bibleSecondCheckBox = QtGui.QCheckBox(self.verseDisplayGroupBox)
        self.bibleSecondCheckBox.setObjectName(u'bibleSecondCheckBox')
        self.verseDisplayLayout.addRow(self.bibleSecondCheckBox)
        self.bibleThemeLabel = QtGui.QLabel(self.verseDisplayGroupBox)
        self.bibleThemeLabel.setObjectName(u'BibleThemeLabel')
        self.bibleThemeComboBox = QtGui.QComboBox(self.verseDisplayGroupBox)
        self.bibleThemeComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.bibleThemeComboBox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.bibleThemeComboBox.addItem(u'')
        self.bibleThemeComboBox.setObjectName(u'BibleThemeComboBox')
        self.verseDisplayLayout.addRow(self.bibleThemeLabel, self.bibleThemeComboBox)
        self.changeNoteLabel = QtGui.QLabel(self.verseDisplayGroupBox)
        self.changeNoteLabel.setWordWrap(True)
        self.changeNoteLabel.setObjectName(u'changeNoteLabel')
        self.verseDisplayLayout.addRow(self.changeNoteLabel)
        self.leftLayout.addWidget(self.verseDisplayGroupBox)
        self.scriptureReferenceGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.scriptureReferenceGroupBox.setObjectName(u'scriptureReferenceGroupBox')
        self.scriptureReferenceLayout = QtGui.QGridLayout(self.scriptureReferenceGroupBox)
        self.verseSeparatorCheckBox = QtGui.QCheckBox(self.scriptureReferenceGroupBox)
        self.verseSeparatorCheckBox.setObjectName(u'verseSeparatorCheckBox')
        self.scriptureReferenceLayout.addWidget(self.verseSeparatorCheckBox, 0, 0)
        self.verseSeparatorLineEdit = QtGui.QLineEdit(self.scriptureReferenceGroupBox)
#        self.verseSeparatorLineEdit.setPalette
        self.verseSeparatorLineEdit.setObjectName(u'verseSeparatorLineEdit')
        self.scriptureReferenceLayout.addWidget(self.verseSeparatorLineEdit, 0, 1)
        self.rangeSeparatorCheckBox = QtGui.QCheckBox(self.scriptureReferenceGroupBox)
        self.rangeSeparatorCheckBox.setObjectName(u'rangeSeparatorCheckBox')
        self.scriptureReferenceLayout.addWidget(self.rangeSeparatorCheckBox, 1, 0)
        self.rangeSeparatorLineEdit = QtGui.QLineEdit(self.scriptureReferenceGroupBox)
        self.rangeSeparatorLineEdit.setObjectName(u'rangeSeparatorLineEdit')
        self.scriptureReferenceLayout.addWidget(self.rangeSeparatorLineEdit, 1, 1)
        self.listSeparatorCheckBox = QtGui.QCheckBox(self.scriptureReferenceGroupBox)
        self.listSeparatorCheckBox.setObjectName(u'listSeparatorCheckBox')
        self.scriptureReferenceLayout.addWidget(self.listSeparatorCheckBox, 2, 0)
        self.listSeparatorLineEdit = QtGui.QLineEdit(self.scriptureReferenceGroupBox)
        self.listSeparatorLineEdit.setObjectName(u'listSeparatorLineEdit')
        self.scriptureReferenceLayout.addWidget(self.listSeparatorLineEdit, 2, 1)
        self.endSeparatorCheckBox = QtGui.QCheckBox(self.scriptureReferenceGroupBox)
        self.endSeparatorCheckBox.setObjectName(u'endSeparatorCheckBox')
        self.scriptureReferenceLayout.addWidget(self.endSeparatorCheckBox, 3, 0)
        self.endSeparatorLineEdit = QtGui.QLineEdit(self.scriptureReferenceGroupBox)
        self.endSeparatorLineEdit.setObjectName(u'endSeparatorLineEdit')
        self.endSeparatorLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'[^0-9]*'),
            self.endSeparatorLineEdit))
        self.scriptureReferenceLayout.addWidget(self.endSeparatorLineEdit, 3, 1)
        self.leftLayout.addWidget(self.scriptureReferenceGroupBox)
        self.rightColumn.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.languageSelectionGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.languageSelectionGroupBox.setObjectName(u'languageSelectionGroupBox')
        self.languageSelectionLayout = QtGui.QVBoxLayout(self.languageSelectionGroupBox)
        self.languageSelectionLabel = QtGui.QLabel(self.languageSelectionGroupBox)
        self.languageSelectionLabel.setObjectName(u'languageSelectionLabel')
        self.languageSelectionComboBox = QtGui.QComboBox(self.languageSelectionGroupBox)
        self.languageSelectionComboBox.setObjectName(u'languageSelectionComboBox')
        self.languageSelectionComboBox.addItems([u'', u'', u''])
        self.languageSelectionLayout.addWidget(self.languageSelectionLabel)
        self.languageSelectionLayout.addWidget(self.languageSelectionComboBox)
        self.rightLayout.addWidget(self.languageSelectionGroupBox)
        self.leftLayout.addStretch()
        self.rightLayout.addStretch()
        # Signals and slots
        QtCore.QObject.connect(self.newChaptersCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onNewChaptersCheckBoxChanged)
        QtCore.QObject.connect(self.displayStyleComboBox, QtCore.SIGNAL(u'activated(int)'),
            self.onDisplayStyleComboBoxChanged)
        QtCore.QObject.connect(self.bibleThemeComboBox, QtCore.SIGNAL(u'activated(int)'),
            self.onBibleThemeComboBoxChanged)
        QtCore.QObject.connect(self.layoutStyleComboBox, QtCore.SIGNAL(u'activated(int)'),
            self.onLayoutStyleComboBoxChanged)
        QtCore.QObject.connect(self.bibleSecondCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onBibleSecondCheckBox)
        QtCore.QObject.connect(self.verseSeparatorCheckBox, QtCore.SIGNAL(u'clicked(bool)'),
            self.onVerseSeparatorCheckBoxClicked)
        QtCore.QObject.connect(self.verseSeparatorLineEdit, QtCore.SIGNAL(u'textEdited(QString)'),
            self.onVerseSeparatorLineEditEdited)
        QtCore.QObject.connect(self.verseSeparatorLineEdit, QtCore.SIGNAL(u'editingFinished()'),
            self.onVerseSeparatorLineEditFinished)
        QtCore.QObject.connect(self.rangeSeparatorCheckBox, QtCore.SIGNAL(u'clicked(bool)'),
            self.onRangeSeparatorCheckBoxClicked)
        QtCore.QObject.connect(self.rangeSeparatorLineEdit, QtCore.SIGNAL(u'textEdited(QString)'),
            self.onRangeSeparatorLineEditEdited)
        QtCore.QObject.connect(self.rangeSeparatorLineEdit, QtCore.SIGNAL(u'editingFinished()'),
            self.onRangeSeparatorLineEditFinished)
        QtCore.QObject.connect(self.listSeparatorCheckBox, QtCore.SIGNAL(u'clicked(bool)'),
            self.onListSeparatorCheckBoxClicked)
        QtCore.QObject.connect(self.listSeparatorLineEdit, QtCore.SIGNAL(u'textEdited(QString)'),
            self.onListSeparatorLineEditEdited)
        QtCore.QObject.connect(self.listSeparatorLineEdit, QtCore.SIGNAL(u'editingFinished()'),
            self.onListSeparatorLineEditFinished)
        QtCore.QObject.connect(self.endSeparatorCheckBox, QtCore.SIGNAL(u'clicked(bool)'),
            self.onEndSeparatorCheckBoxClicked)
        QtCore.QObject.connect(self.endSeparatorLineEdit, QtCore.SIGNAL(u'textEdited(QString)'),
            self.onEndSeparatorLineEditEdited)
        QtCore.QObject.connect(self.endSeparatorLineEdit, QtCore.SIGNAL(u'editingFinished()'),
            self.onEndSeparatorLineEditFinished)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'theme_update_list'), self.updateThemeList)
        QtCore.QObject.connect(self.languageSelectionComboBox, QtCore.SIGNAL(u'activated(int)'),
            self.onLanguageSelectionComboBoxChanged)

    def retranslateUi(self):
        self.verseDisplayGroupBox.setTitle(translate('BiblesPlugin.BiblesTab', 'Verse Display'))
        self.newChaptersCheckBox.setText(translate('BiblesPlugin.BiblesTab', 'Only show new chapter numbers'))
        self.layoutStyleLabel.setText(UiStrings().LayoutStyle)
        self.displayStyleLabel.setText(UiStrings().DisplayStyle)
        self.bibleThemeLabel.setText(translate('BiblesPlugin.BiblesTab', 'Bible theme:'))
        self.layoutStyleComboBox.setItemText(LayoutStyle.VersePerSlide, UiStrings().VersePerSlide)
        self.layoutStyleComboBox.setItemText(LayoutStyle.VersePerLine, UiStrings().VersePerLine)
        self.layoutStyleComboBox.setItemText(LayoutStyle.Continuous, UiStrings().Continuous)
        self.displayStyleComboBox.setItemText(DisplayStyle.NoBrackets,
            translate('BiblesPlugin.BiblesTab', 'No Brackets'))
        self.displayStyleComboBox.setItemText(DisplayStyle.Round,
            translate('BiblesPlugin.BiblesTab', '( And )'))
        self.displayStyleComboBox.setItemText(DisplayStyle.Curly,
            translate('BiblesPlugin.BiblesTab', '{ And }'))
        self.displayStyleComboBox.setItemText(DisplayStyle.Square,
            translate('BiblesPlugin.BiblesTab', '[ And ]'))
        self.changeNoteLabel.setText(translate('BiblesPlugin.BiblesTab',
            'Note:\nChanges do not affect verses already in the service.'))
        self.bibleSecondCheckBox.setText(translate('BiblesPlugin.BiblesTab', 'Display second Bible verses'))
        self.scriptureReferenceGroupBox.setTitle(translate('BiblesPlugin.BiblesTab', 'Custom Scripture References'))
        self.verseSeparatorCheckBox.setText(translate('BiblesPlugin.BiblesTab', 'Verse Separator:'))
        self.rangeSeparatorCheckBox.setText(translate('BiblesPlugin.BiblesTab', 'Range Separator:'))
        self.listSeparatorCheckBox.setText(translate('BiblesPlugin.BiblesTab', 'List Separator:'))
        self.endSeparatorCheckBox.setText(translate('BiblesPlugin.BiblesTab', 'End Mark:'))
        #@todo these are common so move to StringsUI and reuse.
        self.verseSeparatorLineEdit.setToolTip(
            translate('BiblesPlugin.BiblesTab', 'Multiple alternative '
                'verse separators may be defined.\nThey have to be separated '
                'by a vertical bar "|".\nPlease clear this edit line to use '
                'the default value.'))
        self.rangeSeparatorLineEdit.setToolTip(
            translate('BiblesPlugin.BiblesTab', 'Multiple alternative '
                'range separators may be defined.\nThey have to be separated '
                'by a vertical bar "|".\nPlease clear this edit line to use '
                'the default value.'))
        self.listSeparatorLineEdit.setToolTip(
            translate('BiblesPlugin.BiblesTab', 'Multiple alternative '
                'list separators may be defined.\nThey have to be separated '
                'by a vertical bar "|".\nPlease clear this edit line to use '
                'the default value.'))
        self.endSeparatorLineEdit.setToolTip(
            translate('BiblesPlugin.BiblesTab', 'Multiple alternative '
                'end marks may be defined.\nThey have to be separated by a '
                'vertical bar "|".\nPlease clear this edit line to use the '
                'default value.'))
        self.languageSelectionGroupBox.setTitle(translate('BiblesPlugin.BiblesTab', 'Default Bible Language'))
        self.languageSelectionLabel.setText(translate('BiblesPlugin.BiblesTab',
            'Book name language in search field,\nsearch results and on display:'))
        self.languageSelectionComboBox.setItemText(LanguageSelection.Bible,
            translate('BiblesPlugin.BiblesTab', 'Bible Language'))
        self.languageSelectionComboBox.setItemText(LanguageSelection.Application,
            translate('BiblesPlugin.BiblesTab', 'Application Language'))
        self.languageSelectionComboBox.setItemText(LanguageSelection.English,
            translate('BiblesPlugin.BiblesTab', 'English'))

    def onBibleThemeComboBoxChanged(self):
        self.bible_theme = self.bibleThemeComboBox.currentText()

    def onDisplayStyleComboBoxChanged(self):
        self.display_style = self.displayStyleComboBox.currentIndex()

    def onLayoutStyleComboBoxChanged(self):
        self.layout_style = self.layoutStyleComboBox.currentIndex()

    def onLanguageSelectionComboBoxChanged(self):
        self.language_selection = self.languageSelectionComboBox.currentIndex()

    def onNewChaptersCheckBoxChanged(self, check_state):
        self.show_new_chapters = False
        # We have a set value convert to True/False.
        if check_state == QtCore.Qt.Checked:
            self.show_new_chapters = True

    def onBibleSecondCheckBox(self, check_state):
        self.second_bibles = False
        # We have a set value convert to True/False.
        if check_state == QtCore.Qt.Checked:
            self.second_bibles = True

    def onVerseSeparatorCheckBoxClicked(self, checked):
        if checked:
            self.verseSeparatorLineEdit.setFocus()
        else:
            self.verseSeparatorLineEdit.setText(get_reference_separator(u'sep_v_default'))
        self.verseSeparatorLineEdit.setPalette(self.getGreyTextPalette(not checked))

    def onVerseSeparatorLineEditEdited(self, text):
        self.verseSeparatorCheckBox.setChecked(True)
        self.verseSeparatorLineEdit.setPalette(self.getGreyTextPalette(False))

    def onVerseSeparatorLineEditFinished(self):
        if self.verseSeparatorLineEdit.isModified():
            text = self.verseSeparatorLineEdit.text()
            if text == get_reference_separator(u'sep_v_default') or not text.replace(u'|', u''):
                self.verseSeparatorCheckBox.setChecked(False)
                self.verseSeparatorLineEdit.setText(get_reference_separator(u'sep_v_default'))
                self.verseSeparatorLineEdit.setPalette(self.getGreyTextPalette(True))

    def onRangeSeparatorCheckBoxClicked(self, checked):
        if checked:
            self.rangeSeparatorLineEdit.setFocus()
        else:
            self.rangeSeparatorLineEdit.setText(get_reference_separator(u'sep_r_default'))
        self.rangeSeparatorLineEdit.setPalette(self.getGreyTextPalette(not checked))

    def onRangeSeparatorLineEditEdited(self, text):
        self.rangeSeparatorCheckBox.setChecked(True)
        self.rangeSeparatorLineEdit.setPalette(self.getGreyTextPalette(False))

    def onRangeSeparatorLineEditFinished(self):
        if self.rangeSeparatorLineEdit.isModified():
            text = self.rangeSeparatorLineEdit.text()
            if text == get_reference_separator(u'sep_r_default') or not text.replace(u'|', u''):
                self.rangeSeparatorCheckBox.setChecked(False)
                self.rangeSeparatorLineEdit.setText(get_reference_separator(u'sep_r_default'))
                self.rangeSeparatorLineEdit.setPalette(self.getGreyTextPalette(True))

    def onListSeparatorCheckBoxClicked(self, checked):
        if checked:
            self.listSeparatorLineEdit.setFocus()
        else:
            self.listSeparatorLineEdit.setText(get_reference_separator(u'sep_l_default'))
        self.listSeparatorLineEdit.setPalette(self.getGreyTextPalette(not checked))

    def onListSeparatorLineEditEdited(self, text):
        self.listSeparatorCheckBox.setChecked(True)
        self.listSeparatorLineEdit.setPalette(self.getGreyTextPalette(False))

    def onListSeparatorLineEditFinished(self):
        if self.listSeparatorLineEdit.isModified():
            text = self.listSeparatorLineEdit.text()
            if text == get_reference_separator(u'sep_l_default') or not text.replace(u'|', u''):
                self.listSeparatorCheckBox.setChecked(False)
                self.listSeparatorLineEdit.setText(get_reference_separator(u'sep_l_default'))
                self.listSeparatorLineEdit.setPalette(self.getGreyTextPalette(True))

    def onEndSeparatorCheckBoxClicked(self, checked):
        if checked:
            self.endSeparatorLineEdit.setFocus()
        else:
            self.endSeparatorLineEdit.setText(get_reference_separator(u'sep_e_default'))
        self.endSeparatorLineEdit.setPalette(self.getGreyTextPalette(not checked))

    def onEndSeparatorLineEditEdited(self, text):
        self.endSeparatorCheckBox.setChecked(True)
        self.endSeparatorLineEdit.setPalette(self.getGreyTextPalette(False))

    def onEndSeparatorLineEditFinished(self):
        if self.endSeparatorLineEdit.isModified():
            text = self.endSeparatorLineEdit.text()
            if text == get_reference_separator(u'sep_e_default') or not text.replace(u'|', u''):
                self.endSeparatorCheckBox.setChecked(False)
                self.endSeparatorLineEdit.setText(get_reference_separator(u'sep_e_default'))
                self.endSeparatorLineEdit.setPalette(self.getGreyTextPalette(True))

    def load(self):
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        self.show_new_chapters = settings.value(u'display new chapter')
        self.display_style = settings.value(u'display brackets')
        self.layout_style = settings.value(u'verse layout style')
        self.bible_theme = settings.value(u'bible theme')
        self.second_bibles = settings.value(u'second bibles')
        self.newChaptersCheckBox.setChecked(self.show_new_chapters)
        self.displayStyleComboBox.setCurrentIndex(self.display_style)
        self.layoutStyleComboBox.setCurrentIndex(self.layout_style)
        self.bibleSecondCheckBox.setChecked(self.second_bibles)
        verse_separator = settings.value(u'verse separator')
        if (verse_separator.strip(u'|') == u'') or (verse_separator == get_reference_separator(u'sep_v_default')):
            self.verseSeparatorLineEdit.setText(get_reference_separator(u'sep_v_default'))
            self.verseSeparatorLineEdit.setPalette(self.getGreyTextPalette(True))
            self.verseSeparatorCheckBox.setChecked(False)
        else:
            self.verseSeparatorLineEdit.setText(verse_separator)
            self.verseSeparatorLineEdit.setPalette(self.getGreyTextPalette(False))
            self.verseSeparatorCheckBox.setChecked(True)
        range_separator = settings.value(u'range separator')
        if (range_separator.strip(u'|') == u'') or (range_separator == get_reference_separator(u'sep_r_default')):
            self.rangeSeparatorLineEdit.setText(get_reference_separator(u'sep_r_default'))
            self.rangeSeparatorLineEdit.setPalette(self.getGreyTextPalette(True))
            self.rangeSeparatorCheckBox.setChecked(False)
        else:
            self.rangeSeparatorLineEdit.setText(range_separator)
            self.rangeSeparatorLineEdit.setPalette(self.getGreyTextPalette(False))
            self.rangeSeparatorCheckBox.setChecked(True)
        list_separator = settings.value(u'list separator')
        if (list_separator.strip(u'|') == u'') or (list_separator == get_reference_separator(u'sep_l_default')):
            self.listSeparatorLineEdit.setText(get_reference_separator(u'sep_l_default'))
            self.listSeparatorLineEdit.setPalette(self.getGreyTextPalette(True))
            self.listSeparatorCheckBox.setChecked(False)
        else:
            self.listSeparatorLineEdit.setText(list_separator)
            self.listSeparatorLineEdit.setPalette(self.getGreyTextPalette(False))
            self.listSeparatorCheckBox.setChecked(True)
        end_separator = settings.value(u'end separator')
        if (end_separator.strip(u'|') == u'') or (end_separator == get_reference_separator(u'sep_e_default')):
            self.endSeparatorLineEdit.setText(get_reference_separator(u'sep_e_default'))
            self.endSeparatorLineEdit.setPalette(self.getGreyTextPalette(True))
            self.endSeparatorCheckBox.setChecked(False)
        else:
            self.endSeparatorLineEdit.setText(end_separator)
            self.endSeparatorLineEdit.setPalette(self.getGreyTextPalette(False))
            self.endSeparatorCheckBox.setChecked(True)
        self.language_selection = settings.value(u'book name language')
        self.languageSelectionComboBox.setCurrentIndex(self.language_selection)
        settings.endGroup()

    def save(self):
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'display new chapter', self.show_new_chapters)
        settings.setValue(u'display brackets', self.display_style)
        settings.setValue(u'verse layout style', self.layout_style)
        settings.setValue(u'book name language', self.language_selection)
        settings.setValue(u'second bibles', self.second_bibles)
        settings.setValue(u'bible theme', self.bible_theme)
        if self.verseSeparatorCheckBox.isChecked():
            settings.setValue(u'verse separator', self.verseSeparatorLineEdit.text())
        else:
            settings.remove(u'verse separator')
        if self.rangeSeparatorCheckBox.isChecked():
            settings.setValue(u'range separator', self.rangeSeparatorLineEdit.text())
        else:
            settings.remove(u'range separator')
        if self.listSeparatorCheckBox.isChecked():
            settings.setValue(u'list separator', self.listSeparatorLineEdit.text())
        else:
            settings.remove(u'list separator')
        if self.endSeparatorCheckBox.isChecked():
            settings.setValue(u'end separator', self.endSeparatorLineEdit.text())
        else:
            settings.remove(u'end separator')
        update_reference_separators()
        Receiver.send_message(u'bibles_load_list')
        settings.endGroup()

    def updateThemeList(self, theme_list):
        """
        Called from ThemeManager when the Themes have changed.

        ``theme_list``
            The list of available themes::

                [u'Bible Theme', u'Song Theme']
        """
        self.bibleThemeComboBox.clear()
        self.bibleThemeComboBox.addItem(u'')
        self.bibleThemeComboBox.addItems(theme_list)
        find_and_set_in_combo_box(self.bibleThemeComboBox, self.bible_theme)

    def getGreyTextPalette(self, greyed):
        """
        Returns a QPalette with greyed out text as used for placeholderText.
        """
        palette = QtGui.QPalette()
        color = self.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Text)
        if greyed:
            color.setAlpha(128)
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Text, color)
        return palette

