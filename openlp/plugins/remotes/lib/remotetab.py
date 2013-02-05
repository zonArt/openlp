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

from PyQt4 import QtCore, QtGui, QtNetwork

from openlp.core.lib import Settings, SettingsTab, Receiver, translate


ZERO_URL = u'0.0.0.0'


class RemoteTab(SettingsTab):
    """
    RemoteTab is the Remotes settings tab in the settings dialog.
    """
    def __init__(self, parent, title, visible_title, icon_path):
        SettingsTab.__init__(self, parent, title, visible_title, icon_path)

    def setupUi(self):
        self.setObjectName(u'RemoteTab')
        SettingsTab.setupUi(self)
        self.serverSettingsGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.serverSettingsGroupBox.setObjectName(u'serverSettingsGroupBox')
        self.serverSettingsLayout = QtGui.QFormLayout(self.serverSettingsGroupBox)
        self.serverSettingsLayout.setObjectName(u'serverSettingsLayout')
        self.addressLabel = QtGui.QLabel(self.serverSettingsGroupBox)
        self.addressLabel.setObjectName(u'addressLabel')
        self.addressEdit = QtGui.QLineEdit(self.serverSettingsGroupBox)
        self.addressEdit.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.addressEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(
            u'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'), self))
        self.addressEdit.setObjectName(u'addressEdit')
        QtCore.QObject.connect(self.addressEdit, QtCore.SIGNAL(u'textChanged(const QString&)'), self.setUrls)
        self.serverSettingsLayout.addRow(self.addressLabel, self.addressEdit)
        self.twelveHourCheckBox = QtGui.QCheckBox(self.serverSettingsGroupBox)
        self.twelveHourCheckBox.setObjectName(u'twelveHourCheckBox')
        self.serverSettingsLayout.addRow(self.twelveHourCheckBox)
        self.portLabel = QtGui.QLabel(self.serverSettingsGroupBox)
        self.portLabel.setObjectName(u'portLabel')
        self.portSpinBox = QtGui.QSpinBox(self.serverSettingsGroupBox)
        self.portSpinBox.setMaximum(32767)
        self.portSpinBox.setObjectName(u'portSpinBox')
        QtCore.QObject.connect(self.portSpinBox, QtCore.SIGNAL(u'valueChanged(int)'), self.setUrls)
        self.serverSettingsLayout.addRow(self.portLabel, self.portSpinBox)
        self.remoteUrlLabel = QtGui.QLabel(self.serverSettingsGroupBox)
        self.remoteUrlLabel.setObjectName(u'remoteUrlLabel')
        self.remoteUrl = QtGui.QLabel(self.serverSettingsGroupBox)
        self.remoteUrl.setObjectName(u'remoteUrl')
        self.remoteUrl.setOpenExternalLinks(True)
        self.serverSettingsLayout.addRow(self.remoteUrlLabel, self.remoteUrl)
        self.stageUrlLabel = QtGui.QLabel(self.serverSettingsGroupBox)
        self.stageUrlLabel.setObjectName(u'stageUrlLabel')
        self.stageUrl = QtGui.QLabel(self.serverSettingsGroupBox)
        self.stageUrl.setObjectName(u'stageUrl')
        self.stageUrl.setOpenExternalLinks(True)
        self.serverSettingsLayout.addRow(self.stageUrlLabel, self.stageUrl)
        self.leftLayout.addWidget(self.serverSettingsGroupBox)
        self.androidAppGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.androidAppGroupBox.setObjectName(u'androidAppGroupBox')
        self.rightLayout.addWidget(self.androidAppGroupBox)
        self.qrLayout = QtGui.QVBoxLayout(self.androidAppGroupBox)
        self.qrLayout.setObjectName(u'qrLayout')
        self.qrCodeLabel = QtGui.QLabel(self.androidAppGroupBox)
        self.qrCodeLabel.setPixmap(QtGui.QPixmap(u':/remotes/android_app_qr.png'))
        self.qrCodeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.qrCodeLabel.setObjectName(u'qrCodeLabel')
        self.qrLayout.addWidget(self.qrCodeLabel)
        self.qrDescriptionLabel = QtGui.QLabel(self.androidAppGroupBox)
        self.qrDescriptionLabel.setObjectName(u'qrDescriptionLabel')
        self.qrDescriptionLabel.setOpenExternalLinks(True)
        self.qrDescriptionLabel.setWordWrap(True)
        self.qrLayout.addWidget(self.qrDescriptionLabel)
        self.leftLayout.addStretch()
        self.rightLayout.addStretch()
        QtCore.QObject.connect(self.twelveHourCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onTwelveHourCheckBoxChanged)

    def retranslateUi(self):
        self.serverSettingsGroupBox.setTitle(
            translate('RemotePlugin.RemoteTab', 'Server Settings'))
        self.addressLabel.setText(translate('RemotePlugin.RemoteTab', 'Serve on IP address:'))
        self.portLabel.setText(translate('RemotePlugin.RemoteTab', 'Port number:'))
        self.remoteUrlLabel.setText(translate('RemotePlugin.RemoteTab', 'Remote URL:'))
        self.stageUrlLabel.setText(translate('RemotePlugin.RemoteTab', 'Stage view URL:'))
        self.twelveHourCheckBox.setText(translate('RemotePlugin.RemoteTab', 'Display stage time in 12h format'))
        self.androidAppGroupBox.setTitle(translate('RemotePlugin.RemoteTab', 'Android App'))
        self.qrDescriptionLabel.setText(translate('RemotePlugin.RemoteTab',
            'Scan the QR code or click <a href="https://play.google.com/store/'
            'apps/details?id=org.openlp.android">download</a> to install the '
            'Android app from Google Play.'))

    def setUrls(self):
        ipAddress = u'localhost'
        if self.addressEdit.text() == ZERO_URL:
            ifaces = QtNetwork.QNetworkInterface.allInterfaces()
            for iface in ifaces:
                if not iface.isValid():
                    continue
                if not (iface.flags() & (QtNetwork.QNetworkInterface.IsUp | QtNetwork.QNetworkInterface.IsRunning)):
                    continue
                for addr in iface.addressEntries():
                    ip = addr.ip()
                    if ip.protocol() == 0 and ip != QtNetwork.QHostAddress.LocalHost:
                        ipAddress = ip
                        break
        else:
            ipAddress = self.addressEdit.text()
        url = u'http://%s:%s/' % (ipAddress, self.portSpinBox.value())
        self.remoteUrl.setText(u'<a href="%s">%s</a>' % (url, url))
        url += u'stage'
        self.stageUrl.setText(u'<a href="%s">%s</a>' % (url, url))

    def load(self):
        self.portSpinBox.setValue(Settings().value(self.settingsSection + u'/port'))
        self.addressEdit.setText(Settings().value(self.settingsSection + u'/ip address'))
        self.twelveHour = Settings().value(self.settingsSection + u'/twelve hour')
        self.twelveHourCheckBox.setChecked(self.twelveHour)
        self.setUrls()

    def save(self):
        changed = False
        if Settings().value(self.settingsSection + u'/ip address') != self.addressEdit.text() or \
                Settings().value(self.settingsSection + u'/port') != self.portSpinBox.value():
            changed = True
        Settings().setValue(self.settingsSection + u'/port', self.portSpinBox.value())
        Settings().setValue(self.settingsSection + u'/ip address', self.addressEdit.text())
        Settings().setValue(self.settingsSection + u'/twelve hour', self.twelveHour)
        if changed:
            Receiver.send_message(u'remotes_config_updated')

    def onTwelveHourCheckBoxChanged(self, check_state):
        self.twelveHour = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.twelveHour = True
