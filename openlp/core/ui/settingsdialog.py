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
The UI widgets of the settings dialog.
"""
from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, build_icon
from openlp.core.lib.ui import create_button_box


class Ui_SettingsDialog(object):
    """
    The UI widgets of the settings dialog.
    """
    def setupUi(self, settings_dialog):
        """
        Set up the UI
        """
        settings_dialog.setObjectName('settings_dialog')
        settings_dialog.resize(800, 500)
        settings_dialog.setWindowIcon(build_icon(':/system/system_settings.png'))
        self.dialog_layout = QtGui.QGridLayout(settings_dialog)
        self.dialog_layout.setObjectName('dialog_layout')
        self.dialog_layout.setMargin(8)
        self.setting_list_widget = QtGui.QListWidget(settings_dialog)
        self.setting_list_widget.setUniformItemSizes(True)
        self.setting_list_widget.setMinimumSize(QtCore.QSize(150, 0))
        self.setting_list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setting_list_widget.setObjectName('setting_list_widget')
        self.dialog_layout.addWidget(self.setting_list_widget, 0, 0, 1, 1)
        self.stacked_layout = QtGui.QStackedLayout()
        self.stacked_layout.setObjectName('stacked_layout')
        self.dialog_layout.addLayout(self.stacked_layout, 0, 1, 1, 1)
        self.button_box = create_button_box(settings_dialog, 'button_box', ['cancel', 'ok'])
        self.dialog_layout.addWidget(self.button_box, 1, 1, 1, 1)
        self.retranslateUi(settings_dialog)
        self.setting_list_widget.currentRowChanged.connect(self.tab_changed)

    def retranslateUi(self, settings_dialog):
        """
        Translate the UI on the fly
        """
        settings_dialog.setWindowTitle(translate('OpenLP.SettingsForm', 'Configure OpenLP'))
