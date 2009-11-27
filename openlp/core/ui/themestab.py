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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab, Receiver, ThemeLevel

class ThemesTab(SettingsTab):
    """
    ThemesTab is the theme settings tab in the settings dialog.
    """
    def __init__(self, parent):
        self.parent = parent
        SettingsTab.__init__(self, u'Themes')

    def setupUi(self):
        self.setObjectName(u'ThemesTab')
        self.tabTitleVisible = self.trUtf8(u'Themes')
        self.ThemesTabLayout = QtGui.QHBoxLayout(self)
        self.ThemesTabLayout.setSpacing(8)
        self.ThemesTabLayout.setMargin(8)
        self.ThemesTabLayout.setObjectName(u'ThemesTabLayout')
        self.GlobalGroupBox = QtGui.QGroupBox(self)
        self.GlobalGroupBox.setObjectName(u'GlobalGroupBox')
        self.GlobalGroupBoxLayout = QtGui.QVBoxLayout(self.GlobalGroupBox)
        self.GlobalGroupBoxLayout.setSpacing(8)
        self.GlobalGroupBoxLayout.setMargin(8)
        self.GlobalGroupBoxLayout.setObjectName(u'GlobalGroupBoxLayout')
        self.DefaultComboBox = QtGui.QComboBox(self.GlobalGroupBox)
        self.DefaultComboBox.setObjectName(u'DefaultComboBox')
        self.GlobalGroupBoxLayout.addWidget(self.DefaultComboBox)
        self.DefaultListView = QtGui.QLabel(self.GlobalGroupBox)
        self.DefaultListView.setObjectName(u'DefaultListView')
        self.GlobalGroupBoxLayout.addWidget(self.DefaultListView)
        self.ThemesTabLayout.addWidget(self.GlobalGroupBox)
        self.LevelGroupBox = QtGui.QGroupBox(self)
        self.LevelGroupBox.setObjectName(u'LevelGroupBox')
        self.LevelLayout = QtGui.QFormLayout(self.LevelGroupBox)
        self.LevelLayout.setLabelAlignment(
            QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.LevelLayout.setFormAlignment(
            QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.LevelLayout.setMargin(8)
        self.LevelLayout.setSpacing(8)
        self.LevelLayout.setObjectName(u'LevelLayout')
        self.SongLevelRadioButton = QtGui.QRadioButton(self.LevelGroupBox)
        self.SongLevelRadioButton.setObjectName(u'SongLevelRadioButton')
        self.LevelLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.SongLevelRadioButton)
        self.SongLevelLabel = QtGui.QLabel(self.LevelGroupBox)
        self.SongLevelLabel.setWordWrap(True)
        self.SongLevelLabel.setObjectName(u'SongLevelLabel')
        self.LevelLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.SongLevelLabel)
        self.ServiceLevelRadioButton = QtGui.QRadioButton(self.LevelGroupBox)
        self.ServiceLevelRadioButton.setObjectName(u'ServiceLevelRadioButton')
        self.LevelLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.ServiceLevelRadioButton)
        self.ServiceLevelLabel = QtGui.QLabel(self.LevelGroupBox)
        self.ServiceLevelLabel.setWordWrap(True)
        self.ServiceLevelLabel.setObjectName(u'ServiceLevelLabel')
        self.LevelLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.ServiceLevelLabel)
        self.GlobalLevelRadioButton = QtGui.QRadioButton(self.LevelGroupBox)
        self.GlobalLevelRadioButton.setChecked(True)
        self.GlobalLevelRadioButton.setObjectName(u'GlobalLevelRadioButton')
        self.LevelLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.GlobalLevelRadioButton)
        self.GlobalLevelLabel = QtGui.QLabel(self.LevelGroupBox)
        self.GlobalLevelLabel.setWordWrap(True)
        self.GlobalLevelLabel.setObjectName(u'GlobalLevelLabel')
        self.LevelLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.GlobalLevelLabel)
        self.ThemesTabLayout.addWidget(self.LevelGroupBox)
        QtCore.QObject.connect(self.SongLevelRadioButton,
            QtCore.SIGNAL(u'pressed()'), self.onSongLevelButtonPressed)
        QtCore.QObject.connect(self.ServiceLevelRadioButton,
            QtCore.SIGNAL(u'pressed()'), self.onServiceLevelButtonPressed)
        QtCore.QObject.connect(self.GlobalLevelRadioButton,
            QtCore.SIGNAL(u'pressed()'), self.onGlobalLevelButtonPressed)
        QtCore.QObject.connect(self.DefaultComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onDefaultComboBoxChanged)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'update_themes'), self.updateThemeList)

    def retranslateUi(self):
        self.GlobalGroupBox.setTitle(self.trUtf8(u'Global theme'))
        self.LevelGroupBox.setTitle(self.trUtf8(u'Theme level'))
        self.SongLevelRadioButton.setText(self.trUtf8(u'Song level'))
        self.SongLevelLabel.setText(self.trUtf8(u'Use the theme from each song '
            u'in the database. If a song doesn\'t have a theme associated with '
            u'it, then use the service\'s theme. If the service doesn\'t have '
            u'a theme, then use the global theme.'))
        self.ServiceLevelRadioButton.setText(self.trUtf8(u'Service level'))
        self.ServiceLevelLabel.setText(self.trUtf8(u'Use the theme from the '
            u'service, overriding any of the individual songs\' themes. If the '
            u'service doesn\'t have a theme, then use the global theme.'))
        self.GlobalLevelRadioButton.setText(self.trUtf8(u'Global level'))
        self.GlobalLevelLabel.setText(self.trUtf8(u'Use the global theme, '
            u'overriding any themes associated with either the service or the '
            u'songs.'))

    def load(self):
        self.theme_level = int(self.config.get_config(u'theme level',
            ThemeLevel.Global))
        self.global_theme = self.config.get_config(u'global theme', u'')
        if self.theme_level == ThemeLevel.Global:
            self.GlobalLevelRadioButton.setChecked(True)
        elif self.theme_level == ThemeLevel.Service:
            self.ServiceLevelRadioButton.setChecked(True)
        else:
            self.SongLevelRadioButton.setChecked(True)

    def save(self):
        self.config.set_config(u'theme level', self.theme_level)
        self.config.set_config(u'global theme',self.global_theme)
        Receiver.send_message(u'update_global_theme', self.global_theme)

    def postSetUp(self):
        Receiver.send_message(u'update_global_theme', self.global_theme)

    def onSongLevelButtonPressed(self):
        self.global_style = u'Song'
        self.parent.RenderManager.set_global_theme(
            self.global_theme, self.theme_level)

    def onServiceLevelButtonPressed(self):
        self.global_style = u'Service'
        self.parent.RenderManager.set_global_theme(
            self.global_theme, self.theme_level)

    def onGlobalLevelButtonPressed(self):
        self.global_style = u'Global'
        self.parent.RenderManager.set_global_theme(
            self.global_theme, self.theme_level)

    def onDefaultComboBoxChanged(self, value):
        self.global_theme = unicode(self.DefaultComboBox.currentText())
        self.parent.RenderManager.set_global_theme(
            self.global_theme, self.theme_level)
        image = self.parent.ThemeManagerContents.getPreviewImage(
            self.global_theme)
        preview = QtGui.QPixmap(unicode(image))
        display = preview.scaled(300, 255, QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.DefaultListView.setPixmap(display)

    def updateThemeList(self, theme_list):
        """
        Called from ThemeManager when the Themes have changed
        """
        #reload as may have been triggered by the ThemeManager
        self.global_theme = self.config.get_config(u'global theme', u'')
        self.DefaultComboBox.clear()
        for theme in theme_list:
            self.DefaultComboBox.addItem(theme)
        id = self.DefaultComboBox.findText(
            self.global_theme, QtCore.Qt.MatchExactly)
        if id == -1:
            id = 0 # Not Found
            self.global_theme = u''
        self.DefaultComboBox.setCurrentIndex(id)
        self.parent.RenderManager.set_global_theme(
            self.global_theme, self.theme_level)
        if self.global_theme is not u'':
            image = self.parent.ThemeManagerContents.getPreviewImage(
                self.global_theme)
            preview = QtGui.QPixmap(unicode(image))
            display = preview.scaled(300, 255, QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation)
            self.DefaultListView.setPixmap(display)
