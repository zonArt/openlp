# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

class Ui_PluginViewDialog(object):
    def setupUi(self, PluginViewDialog):
        PluginViewDialog.setObjectName(u'PluginViewDialog')
        PluginViewDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        PluginViewDialog.resize(554, 344)
        self.PluginLayout = QtGui.QVBoxLayout(PluginViewDialog)
        self.PluginLayout.setSpacing(8)
        self.PluginLayout.setMargin(8)
        self.PluginLayout.setObjectName(u'PluginLayout')
        self.ListLayout = QtGui.QHBoxLayout()
        self.ListLayout.setSpacing(8)
        self.ListLayout.setObjectName(u'ListLayout')
        self.PluginListWidget = QtGui.QListWidget(PluginViewDialog)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PluginListWidget.sizePolicy().hasHeightForWidth())
        self.PluginListWidget.setSizePolicy(sizePolicy)
        self.PluginListWidget.setMaximumSize(QtCore.QSize(192, 16777215))
        self.PluginListWidget.setObjectName(u'PluginListWidget')
        self.ListLayout.addWidget(self.PluginListWidget)
        self.PluginInfoGroupBox = QtGui.QGroupBox(PluginViewDialog)
        self.PluginInfoGroupBox.setAlignment(
            QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.PluginInfoGroupBox.setFlat(False)
        self.PluginInfoGroupBox.setObjectName(u'PluginInfoGroupBox')
        self.PluginInfoLayout = QtGui.QFormLayout(self.PluginInfoGroupBox)
        self.PluginInfoLayout.setMargin(8)
        self.PluginInfoLayout.setSpacing(8)
        self.PluginInfoLayout.setObjectName(u'PluginInfoLayout')
        self.VersionLabel = QtGui.QLabel(self.PluginInfoGroupBox)
        self.VersionLabel.setObjectName(u'VersionLabel')
        self.PluginInfoLayout.setWidget(
            1, QtGui.QFormLayout.LabelRole, self.VersionLabel)
        self.VersionNumberLabel = QtGui.QLabel(self.PluginInfoGroupBox)
        self.VersionNumberLabel.setObjectName(u'VersionNumberLabel')
        self.PluginInfoLayout.setWidget(
            1, QtGui.QFormLayout.FieldRole, self.VersionNumberLabel)
        self.AboutLabel = QtGui.QLabel(self.PluginInfoGroupBox)
        self.AboutLabel.setObjectName(u'AboutLabel')
        self.PluginInfoLayout.setWidget(
            2, QtGui.QFormLayout.LabelRole, self.AboutLabel)
        self.StatusLabel = QtGui.QLabel(self.PluginInfoGroupBox)
        self.StatusLabel.setObjectName(u'StatusLabel')
        self.PluginInfoLayout.setWidget(
            0, QtGui.QFormLayout.LabelRole, self.StatusLabel)
        self.StatusComboBox = QtGui.QComboBox(self.PluginInfoGroupBox)
        self.StatusComboBox.setObjectName(u'StatusComboBox')
        self.StatusComboBox.addItem(QtCore.QString())
        self.StatusComboBox.addItem(QtCore.QString())
        self.PluginInfoLayout.setWidget(
            0, QtGui.QFormLayout.FieldRole, self.StatusComboBox)
        self.AboutTextBrowser = QtGui.QTextBrowser(self.PluginInfoGroupBox)
        self.AboutTextBrowser.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse)
        self.AboutTextBrowser.setObjectName(u'AboutTextBrowser')
        self.PluginInfoLayout.setWidget(
            2, QtGui.QFormLayout.FieldRole, self.AboutTextBrowser)
        self.ListLayout.addWidget(self.PluginInfoGroupBox)
        self.PluginLayout.addLayout(self.ListLayout)
        self.PluginListButtonBox = QtGui.QDialogButtonBox(PluginViewDialog)
        self.PluginListButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.PluginListButtonBox.setObjectName(u'PluginListButtonBox')
        self.PluginLayout.addWidget(self.PluginListButtonBox)

        self.retranslateUi(PluginViewDialog)
        QtCore.QObject.connect(self.PluginListButtonBox,
            QtCore.SIGNAL(u'accepted()'), PluginViewDialog.close)
        QtCore.QMetaObject.connectSlotsByName(PluginViewDialog)

    def retranslateUi(self, PluginViewDialog):
        PluginViewDialog.setWindowTitle(self.trUtf8('Plugin List'))
        self.PluginInfoGroupBox.setTitle(self.trUtf8('Plugin Details'))
        self.VersionLabel.setText(self.trUtf8('Version:'))
        self.VersionNumberLabel.setText(self.trUtf8('TextLabel'))
        self.AboutLabel.setText(self.trUtf8('About:'))
        self.StatusLabel.setText(self.trUtf8('Status:'))
        self.StatusComboBox.setItemText(0, self.trUtf8('Active'))
        self.StatusComboBox.setItemText(1, self.trUtf8('Inactive'))
