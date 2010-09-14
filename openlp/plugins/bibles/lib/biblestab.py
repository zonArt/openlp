# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

log = logging.getLogger(__name__)

class BiblesTab(SettingsTab):
    """
    BiblesTab is the Bibles settings tab in the settings dialog.
    """
    log.info(u'Bible Tab loaded')

    def __init__(self, title):
        self.paragraph_style = True
        self.show_new_chapters = False
        self.display_style = 0
        SettingsTab.__init__(self, title)

    def setupUi(self):
        self.setObjectName(u'BiblesTab')
        self.tabTitleVisible = translate('BiblesPlugin.BiblesTab', 'Bibles')
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
        self.BibleDualCheckBox = QtGui.QCheckBox(self.VerseDisplayGroupBox)
        self.BibleDualCheckBox.setObjectName(u'BibleDualCheckBox')
        self.VerseDisplayLayout.addWidget(self.BibleDualCheckBox, 3, 0, 1, 1)
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
        QtCore.QObject.connect(
            self.NewChaptersCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onNewChaptersCheckBoxChanged)
        QtCore.QObject.connect(
            self.DisplayStyleComboBox, QtCore.SIGNAL(u'activated(int)'),
            self.onDisplayStyleComboBoxChanged)
        QtCore.QObject.connect(
            self.BibleThemeComboBox, QtCore.SIGNAL(u'activated(int)'),
            self.onBibleThemeComboBoxChanged)
        QtCore.QObject.connect(
            self.LayoutStyleComboBox, QtCore.SIGNAL(u'activated(int)'),
            self.onLayoutStyleComboBoxChanged)
        QtCore.QObject.connect(
            self.BibleDualCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onBibleDualCheckBox)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_list'), self.updateThemeList)

    def retranslateUi(self):
        self.VerseDisplayGroupBox.setTitle(
            translate('BiblesPlugin.BiblesTab', 'Verse Display'))
        self.NewChaptersCheckBox.setText(
            translate('BiblesPlugin.BiblesTab',
            'Only show new chapter numbers'))
        self.LayoutStyleLabel.setText(
            translate('BiblesPlugin.BiblesTab', 'Layout style:'))
        self.DisplayStyleLabel.setText(
            translate('BiblesPlugin.BiblesTab', 'Display style:'))
        self.BibleThemeLabel.setText(
            translate('BiblesPlugin.BiblesTab', 'Bible theme:'))
        self.LayoutStyleComboBox.setItemText(0,
            translate('BiblesPlugin.BiblesTab', 'Verse Per Slide'))
        self.LayoutStyleComboBox.setItemText(1,
            translate('BiblesPlugin.BiblesTab', 'Verse Per Line'))
        self.LayoutStyleComboBox.setItemText(2,
            translate('BiblesPlugin.BiblesTab', 'Continuous'))
        self.DisplayStyleComboBox.setItemText(0,
            translate('BiblesPlugin.BiblesTab', 'No Brackets'))
        self.DisplayStyleComboBox.setItemText(1,
            translate('BiblesPlugin.BiblesTab', '( And )'))
        self.DisplayStyleComboBox.setItemText(2,
            translate('BiblesPlugin.BiblesTab', '{ And }'))
        self.DisplayStyleComboBox.setItemText(3,
            translate('BiblesPlugin.BiblesTab', '[ And ]'))
        self.ChangeNoteLabel.setText(translate('BiblesPlugin.BiblesTab',
            'Note:\nChanges do not affect verses already in the service.'))
        self.BibleDualCheckBox.setText(
            translate('BiblesPlugin.BiblesTab', 'Display dual Bible verses'))

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

    def onBibleDualCheckBox(self, check_state):
        self.dual_bibles = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.dual_bibles = True

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
        self.dual_bibles = settings.value(
            u'dual bibles', QtCore.QVariant(True)).toBool()
        self.NewChaptersCheckBox.setChecked(self.show_new_chapters)
        self.DisplayStyleComboBox.setCurrentIndex(self.display_style)
        self.LayoutStyleComboBox.setCurrentIndex(self.layout_style)
        self.BibleDualCheckBox.setChecked(self.dual_bibles)
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
        settings.setValue(u'dual bibles', QtCore.QVariant(self.dual_bibles))
        settings.setValue(u'bible theme', QtCore.QVariant(self.bible_theme))
        settings.endGroup()

    def updateThemeList(self, theme_list):
        """
        Called from ThemeManager when the Themes have changed
        """
        self.BibleThemeComboBox.clear()
        self.BibleThemeComboBox.addItem(u'')
        for theme in theme_list:
            self.BibleThemeComboBox.addItem(theme)
        index = self.BibleThemeComboBox.findText(
            unicode(self.bible_theme), QtCore.Qt.MatchExactly)
        if index == -1:
            # Not Found
            index = 0
            self.bible_theme = u''
        self.BibleThemeComboBox.setCurrentIndex(index)
