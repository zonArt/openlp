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
import logging

from PyQt4 import QtCore, QtGui

from openlp.core import translate
from openlp.core.lib import SettingsTab, EventManager, Event, EventType
from openlp.core.resources import *

class ThemesTab(SettingsTab):
    """
    ThemesTab is the theme settings tab in the settings dialog.
    """
    global log
    log=logging.getLogger(u'ThemesTab')    
    
    def __init__(self, eventmanager):
        log.debug(u'Initialise')
        self.eventmanager = eventmanager
        print eventmanager
        SettingsTab.__init__(self, u'Themes')        

    def setupUi(self):
        self.setObjectName(u'ThemesTab')
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
        self.DefaultListView = QtGui.QListView(self.GlobalGroupBox)
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

    def retranslateUi(self):
        self.GlobalGroupBox.setTitle(translate(u'ThemesTab', u'Global theme'))
        self.LevelGroupBox.setTitle(translate(u'ThemesTab', u'Theme level'))
        self.SongLevelRadioButton.setText(translate(u'ThemesTab', u'Song level'))
        self.SongLevelLabel.setText(translate(u'ThemesTab', u'Use the theme from each song in the database. If a song doesn\'t have a theme associated with it, then use the service\'s theme. If the service doesn\'t have a theme, then use the global theme.'))
        self.ServiceLevelRadioButton.setText(translate(u'ThemesTab', u'Service level'))
        self.ServiceLevelLabel.setText(translate(u'ThemesTab', u'Use the theme from the service , overriding any of the individual songs\' themes. If the service doesn\'t have a theme, then use the global theme.'))
        self.GlobalLevelRadioButton.setText(translate(u'ThemesTab', u'Global level'))
        self.GlobalLevelLabel.setText(translate(u'ThemesTab', u'Use the global theme, overriding any themes associated wither either the service or the songs.'))

    def load(self):
        log.debug(u'Load')        
        self.themelist = [u'African Sunset', u'Snowy Mountains', u'Wilderness', u'Wet and Windy London']
        
        for theme in self.themelist:
            self.DefaultComboBox.addItem(translate(u'ThemesTab', theme))
