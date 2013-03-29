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

import os.path

from PyQt4 import QtCore, QtGui, QtNetwork

from openlp.core.lib import Registry, Settings, SettingsTab, translate
from openlp.core.utils import AppLocation


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
        self.address_edit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(u'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),
            self))
        self.address_edit.setObjectName(u'address_edit')
        self.server_settings_layout.addRow(self.address_label, self.address_edit)
        self.twelve_hour_check_box = QtGui.QCheckBox(self.server_settings_group_box)
        self.twelve_hour_check_box.setObjectName(u'twelve_hour_check_box')
        self.server_settings_layout.addRow(self.twelve_hour_check_box)
        self.left_layout.addWidget(self.server_settings_group_box)
        self.http_settings_group_box = QtGui.QGroupBox(self.left_column)
        self.http_settings_group_box.setObjectName(u'http_settings_group_box')
        self.http_setting_layout = QtGui.QFormLayout(self.http_settings_group_box)
        self.http_setting_layout.setObjectName(u'http_setting_layout')
        self.port_label = QtGui.QLabel(self.http_settings_group_box)
        self.port_label.setObjectName(u'port_label')
        self.port_spin_box = QtGui.QSpinBox(self.http_settings_group_box)
        self.port_spin_box.setMaximum(32767)
        self.port_spin_box.setObjectName(u'port_spin_box')
        self.http_setting_layout.addRow(self.port_label, self.port_spin_box)
        self.remote_url_label = QtGui.QLabel(self.http_settings_group_box)
        self.remote_url_label.setObjectName(u'remote_url_label')
        self.remote_url = QtGui.QLabel(self.http_settings_group_box)
        self.remote_url.setObjectName(u'remote_url')
        self.remote_url.setOpenExternalLinks(True)
        self.http_setting_layout.addRow(self.remote_url_label, self.remote_url)
        self.stage_url_label = QtGui.QLabel(self.http_settings_group_box)
        self.stage_url_label.setObjectName(u'stage_url_label')
        self.stage_url = QtGui.QLabel(self.http_settings_group_box)
        self.stage_url.setObjectName(u'stage_url')
        self.stage_url.setOpenExternalLinks(True)
        self.http_setting_layout.addRow(self.stage_url_label, self.stage_url)
        self.left_layout.addWidget(self.http_settings_group_box)
        self.https_settings_group_box = QtGui.QGroupBox(self.left_column)
        self.https_settings_group_box.setCheckable(True)
        self.https_settings_group_box.setChecked(False)
        self.https_settings_group_box.setObjectName(u'https_settings_group_box')
        self.https_settings_layout = QtGui.QFormLayout(self.https_settings_group_box)
        self.https_settings_layout.setObjectName(u'https_settings_layout')
        self.https_error_label = QtGui.QLabel(self.https_settings_group_box)
        self.https_error_label.setVisible(False)
        self.https_error_label.setWordWrap(True)
        self.https_error_label.setObjectName(u'https_error_label')
        self.https_settings_layout.addRow(self.https_error_label)
        self.https_port_label = QtGui.QLabel(self.https_settings_group_box)
        self.https_port_label.setObjectName(u'https_port_label')
        self.https_port_spin_box = QtGui.QSpinBox(self.https_settings_group_box)
        self.https_port_spin_box.setMaximum(32767)
        self.https_port_spin_box.setObjectName(u'https_port_spin_box')
        self.https_settings_layout.addRow(self.https_port_label, self.https_port_spin_box)
        self.remote_https_url = QtGui.QLabel(self.https_settings_group_box)
        self.remote_https_url.setObjectName(u'remote_http_url')
        self.remote_https_url.setOpenExternalLinks(True)
        self.remote_https_url_label = QtGui.QLabel(self.https_settings_group_box)
        self.remote_https_url_label.setObjectName(u'remote_http_url_label')
        self.https_settings_layout.addRow(self.remote_https_url_label, self.remote_https_url)
        self.stage_https_url_label = QtGui.QLabel(self.http_settings_group_box)
        self.stage_https_url_label.setObjectName(u'stage_https_url_label')
        self.stage_https_url = QtGui.QLabel(self.https_settings_group_box)
        self.stage_https_url.setObjectName(u'stage_https_url')
        self.stage_https_url.setOpenExternalLinks(True)
        self.https_settings_layout.addRow(self.stage_https_url_label, self.stage_https_url)
        self.left_layout.addWidget(self.https_settings_group_box)
        self.user_login_group_box = QtGui.QGroupBox(self.left_column)
        self.user_login_group_box.setCheckable(True)
        self.user_login_group_box.setChecked(False)
        self.user_login_group_box.setObjectName(u'user_login_group_box')
        self.user_login_layout = QtGui.QFormLayout(self.user_login_group_box)
        self.user_login_layout.setObjectName(u'user_login_layout')
        self.user_id_label = QtGui.QLabel(self.user_login_group_box)
        self.user_id_label.setObjectName(u'user_id_label')
        self.user_id = QtGui.QLineEdit(self.user_login_group_box)
        self.user_id.setObjectName(u'user_id')
        self.user_login_layout.addRow(self.user_id_label, self.user_id)
        self.password_label = QtGui.QLabel(self.user_login_group_box)
        self.password_label.setObjectName(u'password_label')
        self.password = QtGui.QLineEdit(self.user_login_group_box)
        self.password.setObjectName(u'password')
        self.user_login_layout.addRow(self.password_label, self.password)
        self.left_layout.addWidget(self.user_login_group_box)
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
        self.twelve_hour_check_box.stateChanged.connect(self.on_twelve_hour_check_box_changed)
        self.address_edit.textChanged.connect(self.set_urls)
        self.port_spin_box.valueChanged.connect(self.set_urls)
        self.https_port_spin_box.valueChanged.connect(self.set_urls)
        self.https_settings_group_box.clicked.connect(self.https_changed)

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
        self.https_settings_group_box.setTitle(translate('RemotePlugin.RemoteTab', 'HTTPS Server'))
        self.https_error_label.setText(translate('RemotePlugin.RemoteTab',
            'Could not find an SSL certificate. The HTTPS server will not be available unless an SSL certificate '
            'is found. Please see the manual for more information.'))
        self.https_port_label.setText(self.port_label.text())
        self.remote_https_url_label.setText(self.remote_url_label.text())
        self.stage_https_url_label.setText(self.stage_url_label.text())
        self.user_login_group_box.setTitle(translate('RemotePlugin.RemoteTab', 'User Authentication'))
        self.user_id_label.setText(translate('RemotePlugin.RemoteTab', 'User id:'))
        self.password_label.setText(translate('RemotePlugin.RemoteTab', 'Password:'))

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
        http_url = u'http://%s:%s/' % (ip_address, self.port_spin_box.value())
        https_url = u'https://%s:%s/' % (ip_address, self.https_port_spin_box.value())
        self.remote_url.setText(u'<a href="%s">%s</a>' % (http_url, http_url))
        self.remote_https_url.setText(u'<a href="%s">%s</a>' % (https_url, https_url))
        http_url += u'stage'
        https_url += u'stage'
        self.stage_url.setText(u'<a href="%s">%s</a>' % (http_url, http_url))
        self.stage_https_url.setText(u'<a href="%s">%s</a>' % (https_url, https_url))

    def load(self):
        self.port_spin_box.setValue(Settings().value(self.settings_section + u'/port'))
        self.https_port_spin_box.setValue(Settings().value(self.settings_section + u'/https port'))
        self.address_edit.setText(Settings().value(self.settings_section + u'/ip address'))
        self.twelve_hour = Settings().value(self.settings_section + u'/twelve hour')
        self.twelve_hour_check_box.setChecked(self.twelve_hour)
        shared_data = AppLocation.get_directory(AppLocation.SharedData)
        if not os.path.exists(os.path.join(shared_data, u'openlp.crt')) or \
                not os.path.exists(os.path.join(shared_data, u'openlp.key')):
            self.https_settings_group_box.setChecked(False)
            self.https_settings_group_box.setEnabled(False)
            self.https_error_label.setVisible(True)
        else:
            self.https_settings_group_box.setChecked(Settings().value(self.settings_section + u'/https enabled'))
            self.https_settings_group_box.setEnabled(True)
            self.https_error_label.setVisible(False)
        self.user_login_group_box.setChecked(Settings().value(self.settings_section + u'/authentication enabled'))
        self.user_id.setText(Settings().value(self.settings_section + u'/user id'))
        self.password.setText(Settings().value(self.settings_section + u'/password'))
        self.set_urls()
        self.https_changed()

    def save(self):
        """
        Save the configuration and update the server configuration if necessary
        """
        if Settings().value(self.settings_section + u'/ip address') != self.address_edit.text() or \
                Settings().value(self.settings_section + u'/port') != self.port_spin_box.value() or \
                Settings().value(self.settings_section + u'/https port') != self.https_port_spin_box.value() or \
                Settings().value(self.settings_section + u'/https enabled') != \
                        self.https_settings_group_box.isChecked() or \
                Settings().value(self.settings_section + u'/authentication enabled') != \
                        self.user_login_group_box.isChecked() or \
                Settings().value(self.settings_section + u'/user id') != self.user_id.text() or \
                Settings().value(self.settings_section + u'/password') != self.password.text():
            self.settings_form.register_post_process(u'remotes_config_updated')
        Settings().setValue(self.settings_section + u'/port', self.port_spin_box.value())
        Settings().setValue(self.settings_section + u'/https port', self.https_port_spin_box.value())
        Settings().setValue(self.settings_section + u'/https enabled', self.https_settings_group_box.isChecked())
        Settings().setValue(self.settings_section + u'/ip address', self.address_edit.text())
        Settings().setValue(self.settings_section + u'/twelve hour', self.twelve_hour)
        Settings().setValue(self.settings_section + u'/authentication enabled', self.user_login_group_box.isChecked())
        Settings().setValue(self.settings_section + u'/user id', self.user_id.text())
        Settings().setValue(self.settings_section + u'/password', self.password.text())

    def on_twelve_hour_check_box_changed(self, check_state):
        self.twelve_hour = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.twelve_hour = True

    def https_changed(self):
        """
        Invert the HTTP group box based on Https group settings
        """
        self.http_settings_group_box.setEnabled(not self.https_settings_group_box.isChecked())

