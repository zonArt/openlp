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

from openlp.core.lib import Registry, Settings, SettingsTab, translate


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
        self.server_settings_group_box = QtGui.QGroupBox(self.left_column)
        self.server_settings_group_box.setObjectName(u'server_settings_group_box')
        self.server_settings_layout = QtGui.QFormLayout(self.server_settings_group_box)
        self.server_settings_layout.setObjectName(u'server_settings_layout')
        self.address_label = QtGui.QLabel(self.server_settings_group_box)
        self.address_label.setObjectName(u'address_label')
        self.address_edit = QtGui.QLineEdit(self.server_settings_group_box)
        self.address_edit.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.address_edit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(
            u'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'), self))
        self.address_edit.setObjectName(u'address_edit')
        self.server_settings_layout.addRow(self.address_label, self.address_edit)
        self.twelve_hour_check_box = QtGui.QCheckBox(self.server_settings_group_box)
        self.twelve_hour_check_box.setObjectName(u'twelve_hour_check_box')
        self.server_settings_layout.addRow(self.twelve_hour_check_box)
        self.port_label = QtGui.QLabel(self.server_settings_group_box)
        self.port_label.setObjectName(u'port_label')
        self.port_spin_box = QtGui.QSpinBox(self.server_settings_group_box)
        self.port_spin_box.setMaximum(32767)
        self.port_spin_box.setObjectName(u'port_spin_box')
        self.server_settings_layout.addRow(self.port_label, self.port_spin_box)
        self.remote_url_label = QtGui.QLabel(self.server_settings_group_box)
        self.remote_url_label.setObjectName(u'remote_url_label')
        self.remote_url = QtGui.QLabel(self.server_settings_group_box)
        self.remote_url.setObjectName(u'remote_url')
        self.remote_url.setOpenExternalLinks(True)
        self.server_settings_layout.addRow(self.remote_url_label, self.remote_url)
        self.stage_url_label = QtGui.QLabel(self.server_settings_group_box)
        self.stage_url_label.setObjectName(u'stage_url_label')
        self.stage_url = QtGui.QLabel(self.server_settings_group_box)
        self.stage_url.setObjectName(u'stage_url')
        self.stage_url.setOpenExternalLinks(True)
        self.server_settings_layout.addRow(self.stage_url_label, self.stage_url)
        self.left_layout.addWidget(self.server_settings_group_box)
        self.android_app_group_box = QtGui.QGroupBox(self.right_column)
        self.android_app_group_box.setObjectName(u'android_app_group_box')
        self.right_layout.addWidget(self.android_app_group_box)
        self.qr_layout = QtGui.QVBoxLayout(self.android_app_group_box)
        self.qr_layout.setObjectName(u'qr_layout')
        self.qr_code_label = QtGui.QLabel(self.android_app_group_box)
        self.qr_code_label.setPixmap(QtGui.QPixmap(u':/remotes/android_app_qr.png'))
        self.qr_code_label.setAlignment(QtCore.Qt.AlignCenter)
        self.qr_code_label.setObjectName(u'qr_code_label')
        self.qr_layout.addWidget(self.qr_code_label)
        self.qr_description_label = QtGui.QLabel(self.android_app_group_box)
        self.qr_description_label.setObjectName(u'qr_description_label')
        self.qr_description_label.setOpenExternalLinks(True)
        self.qr_description_label.setWordWrap(True)
        self.qr_layout.addWidget(self.qr_description_label)
        self.left_layout.addStretch()
        self.right_layout.addStretch()
        self.twelve_hour_check_box.stateChanged.connect(self.onTwelveHourCheckBoxChanged)
        self.address_edit.textChanged.connect(self.set_urls)
        self.port_spin_box.valueChanged.connect(self.set_urls)

    def retranslateUi(self):
        self.server_settings_group_box.setTitle(translate('RemotePlugin.RemoteTab', 'Server Settings'))
        self.address_label.setText(translate('RemotePlugin.RemoteTab', 'Serve on IP address:'))
        self.port_label.setText(translate('RemotePlugin.RemoteTab', 'Port number:'))
        self.remote_url_label.setText(translate('RemotePlugin.RemoteTab', 'Remote URL:'))
        self.stage_url_label.setText(translate('RemotePlugin.RemoteTab', 'Stage view URL:'))
        self.twelve_hour_check_box.setText(translate('RemotePlugin.RemoteTab', 'Display stage time in 12h format'))
        self.android_app_group_box.setTitle(translate('RemotePlugin.RemoteTab', 'Android App'))
        self.qr_description_label.setText(translate('RemotePlugin.RemoteTab',
            'Scan the QR code or click <a href="https://play.google.com/store/'
            'apps/details?id=org.openlp.android">download</a> to install the '
            'Android app from Google Play.'))

    def set_urls(self):
        ip_address = u'localhost'
        if self.address_edit.text() == ZERO_URL:
            interfaces = QtNetwork.QNetworkInterface.allInterfaces()
            for interface in interfaces:
                if not interface.isValid():
                    continue
                if not (interface.flags() & (QtNetwork.QNetworkInterface.IsUp | QtNetwork.QNetworkInterface.IsRunning)):
                    continue
                for address in interface.addressEntries():
                    ip = address.ip()
                    if ip.protocol() == 0 and ip != QtNetwork.QHostAddress.LocalHost:
                        ip_address = ip
                        break
        else:
            ip_address = self.address_edit.text()
        url = u'http://%s:%s/' % (ip_address, self.port_spin_box.value())
        self.remote_url.setText(u'<a href="%s">%s</a>' % (url, url))
        url += u'stage'
        self.stage_url.setText(u'<a href="%s">%s</a>' % (url, url))

    def load(self):
        self.port_spin_box.setValue(Settings().value(self.settingsSection + u'/port'))
        self.address_edit.setText(Settings().value(self.settingsSection + u'/ip address'))
        self.twelve_hour = Settings().value(self.settingsSection + u'/twelve hour')
        self.twelve_hour_check_box.setChecked(self.twelve_hour)
        self.set_urls()

    def save(self):
        changed = False
        if Settings().value(self.settingsSection + u'/ip address') != self.address_edit.text() or \
                Settings().value(self.settingsSection + u'/port') != self.port_spin_box.value():
            changed = True
        Settings().setValue(self.settingsSection + u'/port', self.port_spin_box.value())
        Settings().setValue(self.settingsSection + u'/ip address', self.address_edit.text())
        Settings().setValue(self.settingsSection + u'/twelve hour', self.twelve_hour)
        if changed:
            Registry().register_function(u'remotes_config_updated')

    def onTwelveHourCheckBoxChanged(self, check_state):
        self.twelve_hour = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.twelve_hour = True
