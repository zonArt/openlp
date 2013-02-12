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
"""
The Themes configuration tab
"""
from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, Settings, SettingsTab, UiStrings, translate
from openlp.core.lib.theme import ThemeLevel
from openlp.core.lib.ui import find_and_set_in_combo_box


class ThemesTab(SettingsTab):
    """
    ThemesTab is the theme settings tab in the settings dialog.
    """
    def __init__(self, parent):
        """
        Constructor
        """
        generalTranslated = translate('OpenLP.ThemesTab', 'Themes')
        SettingsTab.__init__(self, parent, u'Themes', generalTranslated)
        self.iconPath = u':/themes/theme_new.png'

    def setupUi(self):
        """
        Set up the UI
        """
        self.setObjectName(u'ThemesTab')
        SettingsTab.setupUi(self)
        self.GlobalGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.GlobalGroupBox.setObjectName(u'GlobalGroupBox')
        self.GlobalGroupBoxLayout = QtGui.QVBoxLayout(self.GlobalGroupBox)
        self.GlobalGroupBoxLayout.setObjectName(u'GlobalGroupBoxLayout')
        self.DefaultComboBox = QtGui.QComboBox(self.GlobalGroupBox)
        self.DefaultComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.DefaultComboBox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.DefaultComboBox.setObjectName(u'DefaultComboBox')
        self.GlobalGroupBoxLayout.addWidget(self.DefaultComboBox)
        self.DefaultListView = QtGui.QLabel(self.GlobalGroupBox)
        self.DefaultListView.setObjectName(u'DefaultListView')
        self.GlobalGroupBoxLayout.addWidget(self.DefaultListView)
        self.leftLayout.addWidget(self.GlobalGroupBox)
        self.leftLayout.addStretch()
        self.LevelGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.LevelGroupBox.setObjectName(u'LevelGroupBox')
        self.LevelLayout = QtGui.QFormLayout(self.LevelGroupBox)
        self.LevelLayout.setLabelAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.LevelLayout.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.LevelLayout.setObjectName(u'LevelLayout')
        self.SongLevelRadioButton = QtGui.QRadioButton(self.LevelGroupBox)
        self.SongLevelRadioButton.setObjectName(u'SongLevelRadioButton')
        self.SongLevelLabel = QtGui.QLabel(self.LevelGroupBox)
        self.SongLevelLabel.setObjectName(u'SongLevelLabel')
        self.LevelLayout.addRow(self.SongLevelRadioButton, self.SongLevelLabel)
        self.ServiceLevelRadioButton = QtGui.QRadioButton(self.LevelGroupBox)
        self.ServiceLevelRadioButton.setObjectName(u'ServiceLevelRadioButton')
        self.ServiceLevelLabel = QtGui.QLabel(self.LevelGroupBox)
        self.ServiceLevelLabel.setObjectName(u'ServiceLevelLabel')
        self.LevelLayout.addRow(self.ServiceLevelRadioButton, self.ServiceLevelLabel)
        self.GlobalLevelRadioButton = QtGui.QRadioButton(self.LevelGroupBox)
        self.GlobalLevelRadioButton.setObjectName(u'GlobalLevelRadioButton')
        self.GlobalLevelLabel = QtGui.QLabel(self.LevelGroupBox)
        self.GlobalLevelLabel.setObjectName(u'GlobalLevelLabel')
        self.LevelLayout.addRow(self.GlobalLevelRadioButton, self.GlobalLevelLabel)
        label_top_margin = (self.SongLevelRadioButton.sizeHint().height() -
            self.SongLevelLabel.sizeHint().height()) / 2
        for label in [self.SongLevelLabel, self.ServiceLevelLabel, self.GlobalLevelLabel]:
            rect = label.rect()
            rect.setTop(rect.top() + label_top_margin)
            label.setFrameRect(rect)
            label.setWordWrap(True)
        self.rightLayout.addWidget(self.LevelGroupBox)
        self.rightLayout.addStretch()
        QtCore.QObject.connect(self.SongLevelRadioButton, QtCore.SIGNAL(u'clicked()'), self.onSongLevelButtonClicked)
        QtCore.QObject.connect(self.ServiceLevelRadioButton, QtCore.SIGNAL(u'clicked()'),
            self.onServiceLevelButtonClicked)
        QtCore.QObject.connect(self.GlobalLevelRadioButton, QtCore.SIGNAL(u'clicked()'),
            self.onGlobalLevelButtonClicked)
        QtCore.QObject.connect(self.DefaultComboBox, QtCore.SIGNAL(u'activated(int)'), self.onDefaultComboBoxChanged)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'theme_update_list'), self.updateThemeList)

    def retranslateUi(self):
        """
        Translate the UI on the fly
        """
        self.tabTitleVisible = UiStrings().Themes
        self.GlobalGroupBox.setTitle(translate('OpenLP.ThemesTab', 'Global Theme'))
        self.LevelGroupBox.setTitle(translate('OpenLP.ThemesTab', 'Theme Level'))
        self.SongLevelRadioButton.setText(translate('OpenLP.ThemesTab', 'S&ong Level'))
        self.SongLevelLabel.setText(translate('OpenLP.ThemesTab', 'Use the theme from each song '
            'in the database. If a song doesn\'t have a theme associated with '
            'it, then use the service\'s theme. If the service doesn\'t have '
            'a theme, then use the global theme.'))
        self.ServiceLevelRadioButton.setText(translate('OpenLP.ThemesTab', '&Service Level'))
        self.ServiceLevelLabel.setText(translate('OpenLP.ThemesTab', 'Use the theme from the service, '
            'overriding any of the individual songs\' themes. If the '
            'service doesn\'t have a theme, then use the global theme.'))
        self.GlobalLevelRadioButton.setText(translate('OpenLP.ThemesTab', '&Global Level'))
        self.GlobalLevelLabel.setText(translate('OpenLP.ThemesTab', 'Use the global theme, overriding '
            'any themes associated with either the service or the songs.'))

    def load(self):
        """
        Load the theme settings into the tab
        """
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        self.theme_level = settings.value(u'theme level')
        self.global_theme = settings.value(u'global theme')
        settings.endGroup()
        if self.theme_level == ThemeLevel.Global:
            self.GlobalLevelRadioButton.setChecked(True)
        elif self.theme_level == ThemeLevel.Service:
            self.ServiceLevelRadioButton.setChecked(True)
        else:
            self.SongLevelRadioButton.setChecked(True)

    def save(self):
        """
        Save the settings
        """
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'theme level', self.theme_level)
        settings.setValue(u'global theme', self.global_theme)
        settings.endGroup()
        self.renderer.set_global_theme(self.global_theme)
        self.renderer.set_theme_level(self.theme_level)
        Receiver.send_message(u'theme_update_global', self.global_theme)

    def postSetUp(self):
        """
        After setting things up...
        """
        Receiver.send_message(u'theme_update_global', self.global_theme)

    def onSongLevelButtonClicked(self):
        """
        Set the theme level
        """
        self.theme_level = ThemeLevel.Song

    def onServiceLevelButtonClicked(self):
        """
        Set the theme level
        """
        self.theme_level = ThemeLevel.Service

    def onGlobalLevelButtonClicked(self):
        """
        Set the theme level
        """
        self.theme_level = ThemeLevel.Global

    def onDefaultComboBoxChanged(self, value):
        """
        Set the global default theme
        """
        self.global_theme = self.DefaultComboBox.currentText()
        self.renderer.set_global_theme(self.global_theme)
        self.__previewGlobalTheme()

    def updateThemeList(self, theme_list):
        """
        Called from ThemeManager when the Themes have changed.

        ``theme_list``
            The list of available themes::

                [u'Bible Theme', u'Song Theme']
        """
        # Reload as may have been triggered by the ThemeManager.
        self.global_theme = Settings().value(self.settingsSection + u'/global theme')
        self.DefaultComboBox.clear()
        self.DefaultComboBox.addItems(theme_list)
        find_and_set_in_combo_box(self.DefaultComboBox, self.global_theme)
        self.renderer.set_global_theme(self.global_theme)
        self.renderer.set_theme_level(self.theme_level)
        if self.global_theme is not u'':
            self.__previewGlobalTheme()

    def __previewGlobalTheme(self):
        """
        Utility method to update the global theme preview image.
        """
        image = self.theme_manager.get_preview_image(self.global_theme)
        preview = QtGui.QPixmap(unicode(image))
        if not preview.isNull():
            preview = preview.scaled(300, 255, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.DefaultListView.setPixmap(preview)
