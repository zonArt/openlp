# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

from openlp.core.lib import Receiver, SettingsTab, translate
from openlp.core.lib.ui import UiStrings, find_and_set_in_combo_box
from openlp.plugins.bibles.lib import LayoutStyle, DisplayStyle, \
    update_reference_separators, get_reference_separator

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
        self.verseDisplayLayout.addRow(self.displayStyleLabel,
            self.displayStyleComboBox)
        self.layoutStyleLabel = QtGui.QLabel(self.verseDisplayGroupBox)
        self.layoutStyleLabel.setObjectName(u'layoutStyleLabel')
        self.layoutStyleComboBox = QtGui.QComboBox(self.verseDisplayGroupBox)
        self.layoutStyleComboBox.setObjectName(u'layoutStyleComboBox')
        self.layoutStyleComboBox.addItems([u'', u'', u''])
        self.verseDisplayLayout.addRow(self.layoutStyleLabel,
            self.layoutStyleComboBox)
        self.bibleSecondCheckBox = QtGui.QCheckBox(self.verseDisplayGroupBox)
        self.bibleSecondCheckBox.setObjectName(u'bibleSecondCheckBox')
        self.verseDisplayLayout.addRow(self.bibleSecondCheckBox)
        self.bibleThemeLabel = QtGui.QLabel(self.verseDisplayGroupBox)
        self.bibleThemeLabel.setObjectName(u'BibleThemeLabel')
        self.bibleThemeComboBox = QtGui.QComboBox(self.verseDisplayGroupBox)
        self.bibleThemeComboBox.setSizeAdjustPolicy(
            QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.bibleThemeComboBox.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.bibleThemeComboBox.addItem(u'')
        self.bibleThemeComboBox.setObjectName(u'BibleThemeComboBox')
        self.verseDisplayLayout.addRow(self.bibleThemeLabel,
            self.bibleThemeComboBox)
        self.changeNoteLabel = QtGui.QLabel(self.verseDisplayGroupBox)
        self.changeNoteLabel.setWordWrap(True)
        self.changeNoteLabel.setObjectName(u'changeNoteLabel')
        self.verseDisplayLayout.addRow(self.changeNoteLabel)
        self.leftLayout.addWidget(self.verseDisplayGroupBox)
        self.scriptureReferenceGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.scriptureReferenceGroupBox.setObjectName(
            u'scriptureReferenceGroupBox')
        self.scriptureReferenceLayout = QtGui.QGridLayout(
            self.scriptureReferenceGroupBox)
        self.verseSeparatorCheckBox = QtGui.QCheckBox(
            self.scriptureReferenceGroupBox)
        self.verseSeparatorCheckBox.setObjectName(u'verseSeparatorCheckBox')
        self.scriptureReferenceLayout.addWidget(self.verseSeparatorCheckBox, 0,
            0)
        self.verseSeparatorLineEdit = QtGui.QLineEdit(
            self.scriptureReferenceGroupBox)
        self.verseSeparatorLineEdit.setObjectName(u'verseSeparatorLineEdit')
        self.scriptureReferenceLayout.addWidget(self.verseSeparatorLineEdit, 0,
            1)
        self.rangeSeparatorCheckBox = QtGui.QCheckBox(
            self.scriptureReferenceGroupBox)
        self.rangeSeparatorCheckBox.setObjectName(u'rangeSeparatorCheckBox')
        self.scriptureReferenceLayout.addWidget(self.rangeSeparatorCheckBox, 1,
            0)
        self.rangeSeparatorLineEdit = QtGui.QLineEdit(
            self.scriptureReferenceGroupBox)
        self.rangeSeparatorLineEdit.setObjectName(u'rangeSeparatorLineEdit')
        self.scriptureReferenceLayout.addWidget(self.rangeSeparatorLineEdit, 1,
            1)
        self.listSeparatorCheckBox = QtGui.QCheckBox(
            self.scriptureReferenceGroupBox)
        self.listSeparatorCheckBox.setObjectName(u'listSeparatorCheckBox')
        self.scriptureReferenceLayout.addWidget(self.listSeparatorCheckBox, 2,
            0)
        self.listSeparatorLineEdit = QtGui.QLineEdit(
            self.scriptureReferenceGroupBox)
        self.listSeparatorLineEdit.setObjectName(u'listSeparatorLineEdit')
        self.scriptureReferenceLayout.addWidget(self.listSeparatorLineEdit, 2,
            1)
        self.endSeparatorCheckBox = QtGui.QCheckBox(
            self.scriptureReferenceGroupBox)
        self.endSeparatorCheckBox.setObjectName(u'endSeparatorCheckBox')
        self.scriptureReferenceLayout.addWidget(self.endSeparatorCheckBox, 3,
            0)
        self.endSeparatorLineEdit = QtGui.QLineEdit(
            self.scriptureReferenceGroupBox)
        self.endSeparatorLineEdit.setObjectName(u'endSeparatorLineEdit')
        self.scriptureReferenceLayout.addWidget(self.endSeparatorLineEdit, 3,
            1)
        self.leftLayout.addWidget(self.scriptureReferenceGroupBox)
        self.leftLayout.addStretch()
        self.rightColumn.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.rightLayout.addStretch()
        # Signals and slots
        QtCore.QObject.connect(
            self.newChaptersCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onNewChaptersCheckBoxChanged)
        QtCore.QObject.connect(
            self.displayStyleComboBox, QtCore.SIGNAL(u'activated(int)'),
            self.onDisplayStyleComboBoxChanged)
        QtCore.QObject.connect(
            self.bibleThemeComboBox, QtCore.SIGNAL(u'activated(int)'),
            self.onBibleThemeComboBoxChanged)
        QtCore.QObject.connect(
            self.layoutStyleComboBox, QtCore.SIGNAL(u'activated(int)'),
            self.onLayoutStyleComboBoxChanged)
        QtCore.QObject.connect(
            self.bibleSecondCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onBibleSecondCheckBox)
        QtCore.QObject.connect(
            self.verseSeparatorCheckBox, QtCore.SIGNAL(u'clicked(bool)'),
            self.onVerseSeparatorCheckBoxToggled)
        QtCore.QObject.connect(
            self.verseSeparatorLineEdit, QtCore.SIGNAL(u'textEdited(QString)'),
            self.onVerseSeparatorLineEditEdited)
        QtCore.QObject.connect(
            self.verseSeparatorLineEdit, QtCore.SIGNAL(u'editingFinished()'),
            self.onVerseSeparatorLineEditFinished)
        QtCore.QObject.connect(
            self.rangeSeparatorCheckBox, QtCore.SIGNAL(u'clicked(bool)'),
            self.onRangeSeparatorCheckBoxToggled)
        QtCore.QObject.connect(
            self.rangeSeparatorLineEdit, QtCore.SIGNAL(u'textEdited(QString)'),
            self.onRangeSeparatorLineEditEdited)
        QtCore.QObject.connect(
            self.rangeSeparatorLineEdit, QtCore.SIGNAL(u'editingFinished()'),
            self.onRangeSeparatorLineEditFinished)
        QtCore.QObject.connect(
            self.listSeparatorCheckBox, QtCore.SIGNAL(u'clicked(bool)'),
            self.onListSeparatorCheckBoxToggled)
        QtCore.QObject.connect(
            self.listSeparatorLineEdit, QtCore.SIGNAL(u'textEdited(QString)'),
            self.onListSeparatorLineEditEdited)
        QtCore.QObject.connect(
            self.listSeparatorLineEdit, QtCore.SIGNAL(u'editingFinished()'),
            self.onListSeparatorLineEditFinished)
        QtCore.QObject.connect(
            self.endSeparatorCheckBox, QtCore.SIGNAL(u'clicked(bool)'),
            self.onEndSeparatorCheckBoxToggled)
        QtCore.QObject.connect(
            self.endSeparatorLineEdit, QtCore.SIGNAL(u'textEdited(QString)'),
            self.onEndSeparatorLineEditEdited)
        QtCore.QObject.connect(
            self.endSeparatorLineEdit, QtCore.SIGNAL(u'editingFinished()'),
            self.onEndSeparatorLineEditFinished)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_list'), self.updateThemeList)

    def retranslateUi(self):
        self.verseDisplayGroupBox.setTitle(
            translate('BiblesPlugin.BiblesTab', 'Verse Display'))
        self.newChaptersCheckBox.setText(
            translate('BiblesPlugin.BiblesTab',
            'Only show new chapter numbers'))
        self.layoutStyleLabel.setText(UiStrings().LayoutStyle)
        self.displayStyleLabel.setText(UiStrings().DisplayStyle)
        self.bibleThemeLabel.setText(
            translate('BiblesPlugin.BiblesTab', 'Bible theme:'))
        self.layoutStyleComboBox.setItemText(LayoutStyle.VersePerSlide,
            UiStrings().VersePerSlide)
        self.layoutStyleComboBox.setItemText(LayoutStyle.VersePerLine,
            UiStrings().VersePerLine)
        self.layoutStyleComboBox.setItemText(LayoutStyle.Continuous,
            UiStrings().Continuous)
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
        self.bibleSecondCheckBox.setText(
            translate('BiblesPlugin.BiblesTab', 'Display second Bible verses'))
        self.scriptureReferenceGroupBox.setTitle(
            translate('BiblesPlugin.BiblesTab', 'Custom Scripture References'))
        self.verseSeparatorCheckBox.setText(
            translate('BiblesPlugin.BiblesTab', 'Verse Separator:'))
        self.rangeSeparatorCheckBox.setText(
            translate('BiblesPlugin.BiblesTab', 'Range Separator:'))
        self.listSeparatorCheckBox.setText(
            translate('BiblesPlugin.BiblesTab', 'List Separator:'))
        self.endSeparatorCheckBox.setText(
            translate('BiblesPlugin.BiblesTab', 'End Mark:'))
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

    def onBibleThemeComboBoxChanged(self):
        self.bible_theme = self.bibleThemeComboBox.currentText()

    def onDisplayStyleComboBoxChanged(self):
        self.display_style = self.displayStyleComboBox.currentIndex()

    def onLayoutStyleComboBoxChanged(self):
        self.layout_style = self.layoutStyleComboBox.currentIndex()

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

    def onVerseSeparatorCheckBoxToggled(self, checked):
        if not checked:
            self.verseSeparatorLineEdit.clear()
        elif self.verseSeparatorCheckBox.hasFocus():
            self.verseSeparatorLineEdit.setFocus()

    def onVerseSeparatorLineEditEdited(self, text):
        self.verseSeparatorCheckBox.setChecked(True)

    def onVerseSeparatorLineEditFinished(self):
        if self.verseSeparatorLineEdit.text().remove(u'|').isEmpty() and \
            not self.verseSeparatorCheckBox.hasFocus():
            self.verseSeparatorCheckBox.setChecked(False)
            self.verseSeparatorLineEdit.clear()

    def onRangeSeparatorCheckBoxToggled(self, checked):
        if not checked:
            self.rangeSeparatorLineEdit.clear()
        elif self.rangeSeparatorCheckBox.hasFocus():
            self.rangeSeparatorLineEdit.setFocus()

    def onRangeSeparatorLineEditEdited(self, text):
        self.rangeSeparatorCheckBox.setChecked(True)

    def onRangeSeparatorLineEditFinished(self):
        if self.rangeSeparatorLineEdit.text().remove(u'|').isEmpty() and \
            not self.rangeSeparatorCheckBox.hasFocus():
            self.rangeSeparatorCheckBox.setChecked(False)
            self.rangeSeparatorLineEdit.clear()

    def onListSeparatorCheckBoxToggled(self, checked):
        if not checked:
            self.listSeparatorLineEdit.clear()
        elif self.listSeparatorCheckBox.hasFocus():
            self.listSeparatorLineEdit.setFocus()

    def onListSeparatorLineEditEdited(self, text):
        self.listSeparatorCheckBox.setChecked(True)

    def onListSeparatorLineEditFinished(self):
        if self.listSeparatorLineEdit.text().remove(u'|').isEmpty() and \
            not self.listSeparatorCheckBox.hasFocus():
            self.listSeparatorCheckBox.setChecked(False)
            self.listSeparatorLineEdit.clear()

    def onEndSeparatorCheckBoxToggled(self, checked):
        if not checked:
            self.endSeparatorLineEdit.clear()
        elif self.endSeparatorCheckBox.hasFocus():
            self.endSeparatorLineEdit.setFocus()

    def onEndSeparatorLineEditEdited(self, text):
        self.endSeparatorCheckBox.setChecked(True)

    def onEndSeparatorLineEditFinished(self):
        if self.endSeparatorLineEdit.text().remove(u'|').isEmpty() and \
            not self.endSeparatorCheckBox.hasFocus():
            self.endSeparatorCheckBox.setChecked(False)
            self.endSeparatorLineEdit.clear()

    def load(self):
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        self.show_new_chapters = settings.value(
            u'display new chapter', QtCore.QVariant(False)).toBool()
        self.display_style = settings.value(
            u'display brackets', QtCore.QVariant(0)).toInt()[0]
        self.layout_style = settings.value(
            u'verse layout style', QtCore.QVariant(0)).toInt()[0]
        self.bible_theme = unicode(
            settings.value(u'bible theme', QtCore.QVariant(u'')).toString())
        self.second_bibles = settings.value(
            u'second bibles', QtCore.QVariant(True)).toBool()
        self.newChaptersCheckBox.setChecked(self.show_new_chapters)
        self.displayStyleComboBox.setCurrentIndex(self.display_style)
        self.layoutStyleComboBox.setCurrentIndex(self.layout_style)
        self.bibleSecondCheckBox.setChecked(self.second_bibles)
        self.verseSeparatorLineEdit.setPlaceholderText(
            get_reference_separator(u'sep_v_default'))
        self.verseSeparatorLineEdit.setText(settings.value(u'verse separator',
            QtCore.QVariant(u'')).toString())
        self.verseSeparatorCheckBox.setChecked(
            self.verseSeparatorLineEdit.text() != u'')
        self.rangeSeparatorLineEdit.setPlaceholderText(
            get_reference_separator(u'sep_r_default'))
        self.rangeSeparatorLineEdit.setText(settings.value(u'range separator',
            QtCore.QVariant(u'')).toString())
        self.rangeSeparatorCheckBox.setChecked(
            self.rangeSeparatorLineEdit.text() != u'')
        self.listSeparatorLineEdit.setPlaceholderText(
            get_reference_separator(u'sep_l_default'))
        self.listSeparatorLineEdit.setText(settings.value(u'list separator',
            QtCore.QVariant(u'')).toString())
        self.listSeparatorCheckBox.setChecked(
            self.listSeparatorLineEdit.text() != u'')
        self.endSeparatorLineEdit.setPlaceholderText(
            get_reference_separator(u'sep_e_default'))
        self.endSeparatorLineEdit.setText(settings.value(u'end separator',
            QtCore.QVariant(u'')).toString())
        self.endSeparatorCheckBox.setChecked(
            self.endSeparatorLineEdit.text() != u'')
        settings.endGroup()

    def save(self):
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'display new chapter',
            QtCore.QVariant(self.show_new_chapters))
        settings.setValue(u'display brackets',
            QtCore.QVariant(self.display_style))
        settings.setValue(u'verse layout style',
            QtCore.QVariant(self.layout_style))
        settings.setValue(u'second bibles', QtCore.QVariant(self.second_bibles))
        settings.setValue(u'bible theme', QtCore.QVariant(self.bible_theme))
        settings.setValue(u'verse separator',
            QtCore.QVariant(self.verseSeparatorLineEdit.text()))
        settings.setValue(u'range separator',
            QtCore.QVariant(self.rangeSeparatorLineEdit.text()))
        settings.setValue(u'list separator',
            QtCore.QVariant(self.listSeparatorLineEdit.text()))
        settings.setValue(u'end separator',
            QtCore.QVariant(self.endSeparatorLineEdit.text()))
        update_reference_separators()
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
        for theme in theme_list:
            self.bibleThemeComboBox.addItem(theme)
        find_and_set_in_combo_box(self.bibleThemeComboBox, self.bible_theme)
