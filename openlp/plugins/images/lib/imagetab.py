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

from openlp.core.lib import SettingsTab, Receiver, translate

class ImageTab(SettingsTab):
    """
    ImageTab is the Image settings tab in the settings dialog.
    """
    def __init__(self, title):
        SettingsTab.__init__(self, title)

    def setupUi(self):
        self.setObjectName(u'ImageTab')
        self.tabTitleVisible = translate('ImagePlugin.ImageTab', 'Images')
        self.ImageLayout = QtGui.QFormLayout(self)
        self.ImageLayout.setSpacing(8)
        self.ImageLayout.setMargin(8)
        self.ImageLayout.setObjectName(u'ImageLayout')
        self.ImageSettingsGroupBox = QtGui.QGroupBox(self)
        self.ImageSettingsGroupBox.setObjectName(u'ImageSettingsGroupBox')
        self.TimeoutLayout = QtGui.QHBoxLayout(self.ImageSettingsGroupBox)
        self.TimeoutLayout.setSpacing(8)
        self.TimeoutLayout.setMargin(8)
        self.TimeoutLayout.setObjectName(u'TimeoutLayout')
        self.TimeoutLabel = QtGui.QLabel(self.ImageSettingsGroupBox)
        self.TimeoutLabel.setObjectName(u'TimeoutLabel')
        self.TimeoutLayout.addWidget(self.TimeoutLabel)
        self.TimeoutSpinBox = QtGui.QSpinBox(self.ImageSettingsGroupBox)
        self.TimeoutSpinBox.setMinimum(1)
        self.TimeoutSpinBox.setMaximum(180)
        self.TimeoutSpinBox.setObjectName(u'TimeoutSpinBox')
        self.TimeoutLayout.addWidget(self.TimeoutSpinBox)
        self.TimeoutSpacer = QtGui.QSpacerItem(147, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.TimeoutLayout.addItem(self.TimeoutSpacer)
        self.ImageLayout.setWidget(
            0, QtGui.QFormLayout.LabelRole, self.ImageSettingsGroupBox)
        # Signals and slots
        QtCore.QObject.connect(self.TimeoutSpinBox,
            QtCore.SIGNAL(u'valueChanged(int)'), self.onTimeoutSpinBoxChanged)

    def retranslateUi(self):
        self.ImageSettingsGroupBox.setTitle(
            translate('ImagePlugin.ImageTab', 'Image Settings'))
        self.TimeoutLabel.setText(
            translate('ImagePlugin.ImageTab', 'Slide loop delay:'))
        self.TimeoutSpinBox.setSuffix(
            translate('ImagePlugin.ImageTab', 'sec'))

    def onTimeoutSpinBoxChanged(self):
        self.loop_delay = self.TimeoutSpinBox.value()

    def load(self):
        self.loop_delay = QtCore.QSettings().value(
            self.settingsSection + u'/loop delay',
            QtCore.QVariant(5)).toInt()[0]
        self.TimeoutSpinBox.setValue(self.loop_delay)

    def save(self):
        QtCore.QSettings().setValue(self.settingsSection + u'/loop delay',
            QtCore.QVariant(self.loop_delay))
        Receiver.send_message(u'slidecontroller_live_spin_delay',
            self.loop_delay)

    def postSetUp(self):
        Receiver.send_message(u'slidecontroller_live_spin_delay',
            self.loop_delay)

