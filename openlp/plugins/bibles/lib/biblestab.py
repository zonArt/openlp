# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from openlp.core.lib import translate, str_to_bool, Receiver
from openlp.core.lib import SettingsTab

class BiblesTab(SettingsTab):
    """
    BiblesTab is the Bibles settings tab in the settings dialog.
    """
    global log
    log = logging.getLogger(u'BibleTab')
    log.info(u'Bible Tab loaded')

    def __init__(self):
        self.paragraph_style = True
        self.show_new_chapters = False
        self.display_style = 0
        SettingsTab.__init__(
            self, translate(u'BiblesTab', u'Bibles'), u'Bibles')

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
        self.NewChaptersCheckBox = QtGui.QCheckBox(self.VerseDisplayGroupBox)
        self.NewChaptersCheckBox.setObjectName(u'NewChaptersCheckBox')
        self.VerseDisplayLayout.addWidget(self.NewChaptersCheckBox, 0, 0, 1, 1)
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
        self.VerseDisplayLayout.addWidget(self.DisplayStyleWidget, 1, 0, 1, 1)
        self.LayoutStyleWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.LayoutStyleWidget.setObjectName(u'LayoutStyleWidget')
        self.LayoutStyleLayout = QtGui.QHBoxLayout(self.LayoutStyleWidget)
        self.LayoutStyleLayout.setSpacing(8)
        self.LayoutStyleLayout.setMargin(0)
        self.LayoutStyleLayout.setObjectName(u'LayoutStyleLayout')
        self.LayoutStyleLabel = QtGui.QLabel(self.LayoutStyleWidget)
        self.LayoutStyleLabel.setObjectName(u'LayoutStyleLabel')
        self.LayoutStyleLayout.addWidget(self.LayoutStyleLabel)
        self.LayoutStyleComboBox = QtGui.QComboBox(self.LayoutStyleWidget)
        self.LayoutStyleComboBox.setObjectName(u'LayoutStyleComboBox')
        self.LayoutStyleComboBox.addItem(QtCore.QString())
        self.LayoutStyleComboBox.addItem(QtCore.QString())
        self.LayoutStyleComboBox.addItem(QtCore.QString())
        self.LayoutStyleLayout.addWidget(self.LayoutStyleComboBox)
        self.VerseDisplayLayout.addWidget(self.LayoutStyleWidget, 2, 0, 1, 1)
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
        self.BibleDuelCheckBox = QtGui.QCheckBox(self.VerseDisplayGroupBox)
        self.BibleDuelCheckBox.setObjectName(u'BibleDuelCheckBox')
        self.VerseDisplayLayout.addWidget(self.BibleDuelCheckBox, 3, 0, 1, 1)
        self.VerseDisplayLayout.addWidget(self.BibleThemeWidget, 4, 0, 1, 1)
        self.ChangeNoteLabel = QtGui.QLabel(self.VerseDisplayGroupBox)
        self.ChangeNoteLabel.setObjectName(u'ChangeNoteLabel')
        self.VerseDisplayLayout.addWidget(self.ChangeNoteLabel, 5, 0, 1, 1)
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
        self.BibleLayout.addWidget(self.BibleRightWidget)
        # Signals and slots
        QtCore.QObject.connect(self.NewChaptersCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onNewChaptersCheckBoxChanged)
        QtCore.QObject.connect(self.DisplayStyleComboBox,
            QtCore.SIGNAL(u'activated(int)'),
            self.onDisplayStyleComboBoxChanged)
        QtCore.QObject.connect(self.BibleThemeComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onBibleThemeComboBoxChanged)
        QtCore.QObject.connect(self.LayoutStyleComboBox,
            QtCore.SIGNAL(u'activated(int)'),
            self.onLayoutStyleComboBoxChanged)
        QtCore.QObject.connect(self.BibleDuelCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onBibleDuelCheckBox)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'update_themes'), self.updateThemeList)

    def retranslateUi(self):
        self.VerseDisplayGroupBox.setTitle(
            translate(u'SettingsForm', u'Verse Display'))
        self.NewChaptersCheckBox.setText(
            translate(u'SettingsForm', u'Only show new chapter numbers'))
        self.LayoutStyleLabel.setText(
            translate(u'SettingsForm', u'Layout Style:'))
        self.DisplayStyleLabel.setText(
            translate(u'SettingsForm', u'Display Style:'))
        self.BibleThemeLabel.setText(
            translate(u'SettingsForm', u'Bible Theme:'))
        self.LayoutStyleComboBox.setItemText(
            0, translate(u'SettingsForm', u'verse per slide'))
        self.LayoutStyleComboBox.setItemText(
            1, translate(u'SettingsForm', u'verse per line'))
        self.LayoutStyleComboBox.setItemText(
            2, translate(u'SettingsForm', u'continuous'))
        self.DisplayStyleComboBox.setItemText(
            0, translate(u'SettingsForm', u'No brackets'))
        self.DisplayStyleComboBox.setItemText(
            1, translate(u'SettingsForm', u'( and )'))
        self.DisplayStyleComboBox.setItemText(
            2, translate(u'SettingsForm', u'{ and }'))
        self.DisplayStyleComboBox.setItemText(
            3, translate(u'SettingsForm', u'[ and ]'))
        self.ChangeNoteLabel.setText(translate(u'SettingsForm',
            u'Note:\nChanges don\'t affect verses already in the service'))
        self.BibleDuelCheckBox.setText(
            translate(u'SettingsForm', u'Display Duel Bible Verses'))

    def onBibleThemeComboBoxChanged(self):
        self.bible_theme = self.BibleThemeComboBox.currentText()

    def onDisplayStyleComboBoxChanged(self):
        self.display_style = self.DisplayStyleComboBox.currentIndex()

    def onLayoutStyleComboBoxChanged(self):
        self.layout_style = self.LayoutStyleComboBox.currentIndex()

    def onNewChaptersCheckBoxChanged(self, check_state):
        self.show_new_chapters = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.show_new_chapters = True

    def onBibleDuelCheckBox(self, check_state):
        self.duel_bibles = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.duel_bibles = True

    def load(self):
        self.show_new_chapters = str_to_bool(
            self.config.get_config(u'display new chapter', u'False'))
        self.display_style = int(
            self.config.get_config(u'display brackets', u'0'))
        self.layout_style = int(
            self.config.get_config(u'verse layout style', u'0'))
        self.bible_theme = self.config.get_config(u'bible theme', u'0')
        self.duel_bibles = str_to_bool(
            self.config.get_config(u'duel bibles', u'True'))
        self.NewChaptersCheckBox.setChecked(self.show_new_chapters)
        self.DisplayStyleComboBox.setCurrentIndex(self.display_style)
        self.LayoutStyleComboBox.setCurrentIndex(self.layout_style)
        self.BibleDuelCheckBox.setChecked(self.duel_bibles)

    def save(self):
        self.config.set_config(
            u'display new chapter', unicode(self.show_new_chapters))
        self.config.set_config(
            u'display brackets', unicode(self.display_style))
        self.config.set_config(
            u'verse layout style', unicode(self.layout_style))
        self.config.set_config(u'duel bibles', unicode(self.duel_bibles))
        self.config.set_config(u'bible theme', unicode(self.bible_theme))

    def updateThemeList(self, theme_list):
        """
        Called from ThemeManager when the Themes have changed
        """
        self.BibleThemeComboBox.clear()
        self.BibleThemeComboBox.addItem(u'')
        for theme in theme_list:
            self.BibleThemeComboBox.addItem(theme)
        id = self.BibleThemeComboBox.findText(
            unicode(self.bible_theme), QtCore.Qt.MatchExactly)
        if id == -1:
            # Not Found
            id = 0
            self.bible_theme = u''
        self.BibleThemeComboBox.setCurrentIndex(id)
