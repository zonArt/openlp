# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
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
from openlp.plugins.bibles.lib import LayoutStyle, DisplayStyle
from openlp.core.lib.ui import UiStrings, find_and_set_in_combo_box

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