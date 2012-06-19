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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import UiStrings, create_button_box

class Ui_PluginViewDialog(object):
    def setupUi(self, pluginViewDialog):
        pluginViewDialog.setObjectName(u'pluginViewDialog')
        pluginViewDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.pluginLayout = QtGui.QVBoxLayout(pluginViewDialog)
        self.pluginLayout.setObjectName(u'pluginLayout')
        self.listLayout = QtGui.QHBoxLayout()
        self.listLayout.setObjectName(u'listLayout')
        self.pluginListWidget = QtGui.QListWidget(pluginViewDialog)
        self.pluginListWidget.setObjectName(u'pluginListWidget')
        self.listLayout.addWidget(self.pluginListWidget)
        self.pluginInfoGroupBox = QtGui.QGroupBox(pluginViewDialog)
        self.pluginInfoGroupBox.setObjectName(u'pluginInfoGroupBox')
        self.pluginInfoLayout = QtGui.QFormLayout(self.pluginInfoGroupBox)
        self.pluginInfoLayout.setObjectName(u'pluginInfoLayout')
        self.statusLabel = QtGui.QLabel(self.pluginInfoGroupBox)
        self.statusLabel.setObjectName(u'statusLabel')
        self.statusComboBox = QtGui.QComboBox(self.pluginInfoGroupBox)
        self.statusComboBox.addItems((u'', u''))
        self.statusComboBox.setObjectName(u'statusComboBox')
        self.pluginInfoLayout.addRow(self.statusLabel, self.statusComboBox)
        self.versionLabel = QtGui.QLabel(self.pluginInfoGroupBox)
        self.versionLabel.setObjectName(u'versionLabel')
        self.versionNumberLabel = QtGui.QLabel(self.pluginInfoGroupBox)
        self.versionNumberLabel.setObjectName(u'versionNumberLabel')
        self.pluginInfoLayout.addRow(self.versionLabel, self.versionNumberLabel)
        self.aboutLabel = QtGui.QLabel(self.pluginInfoGroupBox)
        self.aboutLabel.setObjectName(u'aboutLabel')
        self.aboutTextBrowser = QtGui.QTextBrowser(self.pluginInfoGroupBox)
        self.aboutTextBrowser.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse)
        self.aboutTextBrowser.setObjectName(u'aboutTextBrowser')
        self.pluginInfoLayout.addRow(self.aboutLabel, self.aboutTextBrowser)
        self.listLayout.addWidget(self.pluginInfoGroupBox)
        self.pluginLayout.addLayout(self.listLayout)
        self.buttonBox = create_button_box(pluginViewDialog, u'buttonBox',
            [u'ok'])
        self.pluginLayout.addWidget(self.buttonBox)
        self.retranslateUi(pluginViewDialog)

    def retranslateUi(self, pluginViewDialog):
        pluginViewDialog.setWindowTitle(
            translate('OpenLP.PluginForm', 'Plugin List'))
        self.pluginInfoGroupBox.setTitle(
            translate('OpenLP.PluginForm', 'Plugin Details'))
        self.versionLabel.setText(u'%s:' % UiStrings().Version)
        self.aboutLabel.setText(u'%s:' % UiStrings().About)
        self.statusLabel.setText(
            translate('OpenLP.PluginForm', 'Status:'))
        self.statusComboBox.setItemText(0,
            translate('OpenLP.PluginForm', 'Active'))
        self.statusComboBox.setItemText(1,
            translate('OpenLP.PluginForm', 'Inactive'))
