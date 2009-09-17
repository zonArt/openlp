# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin,  Receiver,  translate
from openlp.plugins.audit.lib import AuditTab

class AuditPlugin(Plugin):
    global log
    log = logging.getLogger(u'AuditPlugin')
    log.info(u'Audit Plugin loaded')

    def __init__(self, plugin_helpers):
        # Call the parent constructor
        Plugin.__init__(self, u'Audit', u'1.9.0', plugin_helpers)
        self.weight = -4
        # Create the plugin icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(u':/media/media_image.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.auditfile = None

    def check_pre_conditions(self):
        """
        Check to see if auditing is required
        """
        log.debug('check_pre_conditions')
        #Lets see if audit is required
        if int(self.config.get_config(u'startup', 0)) == QtCore.Qt.Checked:
            return True
        else:
            return False

    def add_tools_menu_item(self, tools_menu):
        """
        Give the Audit plugin the opportunity to add items to the
        **Tools** menu.

        ``tools_menu``
            The actual **Tools** menu item, so that your actions can
            use it as their parent.
        """
        self.ToolsAuditItem = QtGui.QAction(tools_menu)
        AuditIcon = QtGui.QIcon()
        AuditIcon.addPixmap(QtGui.QPixmap(u':/tools/tools_alert.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolsAuditItem.setIcon(AuditIcon)
        self.ToolsAuditItem.setObjectName(u'ToolsAuditItem')
        self.ToolsAuditItem.setCheckable(True)
        self.ToolsAuditItem.setChecked(True)
        tools_menu.addSeparator()
        tools_menu.addAction(self.ToolsAuditItem)

        self.ToolsAuditItem.setText(translate(u'AuditPlugin', u'A&udit'))
        self.ToolsAuditItem.setStatusTip(
            translate(u'AuditPlugin', u'Start/Stop live song auditing'))
        self.ToolsAuditItem.setShortcut(translate(u'AuditPlugin', u'F4'))
#
        # Translations...
#        # Signals and slots
#        QtCore.QObject.connect(self.MediaManagerDock,
#            QtCore.SIGNAL(u'visibilityChanged(bool)'),
#            self.ViewMediaManagerItem.setChecked)
#        QtCore.QObject.connect(self.ViewMediaManagerItem,
#            QtCore.SIGNAL(u'triggered(bool)'),
#            self.toggleMediaManager)

    def get_settings_tab(self):
        self.AuditTab = AuditTab()
        return self.AuditTab

    def initialise(self):
        log.info(u'Plugin Initialising')
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'audit_live'), self.onReceiveAudit)
        self.auditfile = open(u'openlp.aud', 'a')
        self.auditActive = False

    def onReceiveAudit(self, auditData):
        if self.auditActive:
            self.auditFile.write(u'%s,%s\n' % (date.today(), auditData))
            self.auditfile.flush()

    def finalise(self):
        log.debug(u'Finalise')
        if self.auditfile is not None:
            self.auditfile.close()
