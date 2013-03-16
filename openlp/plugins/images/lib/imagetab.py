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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab, Registry, Settings, UiStrings, translate

class ImageTab(SettingsTab):
    """
    ImageTab is the images settings tab in the settings dialog.
    """
    def __init__(self, parent, name, visible_title, icon_path):
        SettingsTab.__init__(self, parent, name, visible_title, icon_path)

    def setupUi(self):
        self.setObjectName(u'ImagesTab')
        SettingsTab.setupUi(self)
        self.background_color_group_box = QtGui.QGroupBox(self.left_column)
        self.background_color_group_box.setObjectName(u'FontGroupBox')
        self.form_layout = QtGui.QForm_layout(self.background_color_group_box)
        self.form_layout.setObjectName(u'Form_layout')
        self.color_layout = QtGui.QHBox_layout()
        self.background_color_label = QtGui.QLabel(self.background_color_group_box)
        self.background_color_label.setObjectName(u'BackgroundColor_label')
        self.color_layout.addWidget(self.background_color_label)
        self.background_color_button = QtGui.QPushButton(self.background_color_group_box)
        self.background_color_button.setObjectName(u'BackgroundColor_button')
        self.color_layout.addWidget(self.background_color_button)
        self.form_layout.addRow(self.color_layout)
        self.information_label = QtGui.QLabel(self.background_color_group_box)
        self.information_label.setObjectName(u'information_label')
        self.information_label.setWordWrap(True)
        self.form_layout.addRow(self.information_label)
        self.left_layout.addWidget(self.background_color_group_box)
        self.left_layout.addStretch()
        self.right_column.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.right_layout.addStretch()
        # Signals and slots
        self.background_color_button.clicked.connect(self.on_background_color_button_clicked)

    def retranslateUi(self):
        self.background_color_group_box.setTitle(UiStrings().BackgroundColor)
        self.background_color_label.setText(UiStrings().DefaultColor)
        self.information_label.setText(
            translate('ImagesPlugin.ImageTab', 'Visible background for images with aspect ratio different to screen.'))

    def on_background_color_button_licked(self):
        new_color = QtGui.QColorDialog.getColor(QtGui.QColor(self.bg_color), self)
        if new_color.isValid():
            self.bg_color = new_color.name()
            self.background_color_button.setStyleSheet(u'background-color: %s' % self.bg_color)

    def load(self):
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        self.bg_color = settings.value(u'background color')
        self.initial_color = self.bg_color
        settings.endGroup()
        self.background_color_button.setStyleSheet(u'background-color: %s' % self.bg_color)

    def save(self):
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'background color', self.bg_color)
        settings.endGroup()
        if self.initial_color != self.bg_color:
            self.settings_form.register_post_process(u'image_updated')
