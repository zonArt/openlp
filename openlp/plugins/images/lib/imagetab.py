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

from PyQt4 import QtGui

from openlp.core.lib import Registry, SettingsTab, Settings, UiStrings, translate


class ImageTab(SettingsTab):
    """
    ImageTab is the images settings tab in the settings dialog.
    """
    def __init__(self, parent, name, visible_title, icon_path):
        super(ImageTab, self).__init__(parent, name, visible_title, icon_path)

    def setupUi(self):
        self.setObjectName('ImagesTab')
        super(ImageTab, self).setupUi()
        self.background_color_group_box = QtGui.QGroupBox(self.left_column)
        self.background_color_group_box.setObjectName('background_color_group_box')
        self.form_layout = QtGui.QFormLayout(self.background_color_group_box)
        self.form_layout.setObjectName('form_layout')
        self.color_layout = QtGui.QHBoxLayout()
        self.background_color_label = QtGui.QLabel(self.background_color_group_box)
        self.background_color_label.setObjectName('background_color_label')
        self.color_layout.addWidget(self.background_color_label)
        self.background_color_button = QtGui.QPushButton(self.background_color_group_box)
        self.background_color_button.setObjectName('background_color_button')
        self.color_layout.addWidget(self.background_color_button)
        self.form_layout.addRow(self.color_layout)
        self.information_label = QtGui.QLabel(self.background_color_group_box)
        self.information_label.setObjectName('information_label')
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

    def on_background_color_button_clicked(self):
        new_color = QtGui.QColorDialog.getColor(QtGui.QColor(self.background_color), self)
        if new_color.isValid():
            self.background_color = new_color.name()
            self.background_color_button.setStyleSheet('background-color: %s' % self.background_color)

    def load(self):
        settings = Settings()
        settings.beginGroup(self.settings_section)
        self.background_color = settings.value('background color')
        self.initial_color = self.background_color
        settings.endGroup()
        self.background_color_button.setStyleSheet('background-color: %s' % self.background_color)

    def save(self):
        settings = Settings()
        settings.beginGroup(self.settings_section)
        settings.setValue('background color', self.background_color)
        settings.endGroup()
        if self.initial_color != self.background_color:
            self.settings_form.register_post_process('images_config_updated')
