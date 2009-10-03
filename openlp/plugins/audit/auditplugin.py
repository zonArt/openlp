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

from datetime import datetime
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin, Receiver, translate, str_to_bool, buildIcon
from openlp.plugins.audit.lib import AuditManager
from openlp.plugins.audit.forms import AuditDetailForm, AuditDeleteForm
from openlp.plugins.audit.lib.models import AuditItem

class AuditPlugin(Plugin):
    global log
    log = logging.getLogger(u'AuditPlugin')
    log.info(u'Audit Plugin loaded')

    def __init__(self, plugin_helpers):
        # Call the parent constructor
        Plugin.__init__(self, u'Audit', u'1.9.0', plugin_helpers)
        self.weight = -4
        # Create the plugin icon
        self.icon = buildIcon(u':/media/media_image.png')
        self.auditmanager = None
        self.auditActive = False

    def can_be_disabled(self):
        return True

    def add_tools_menu_item(self, tools_menu):
        """
        Give the Audit plugin the opportunity to add items to the
        **Tools** menu.

        ``tools_menu``
            The actual **Tools** menu item, so that your actions can
            use it as their parent.
        """
        self.toolsMenu = tools_menu
        self.AuditMenu = QtGui.QMenu(tools_menu)
        self.AuditMenu.setObjectName(u'AuditMenu')
        self.AuditMenu.setTitle(
            translate(u'AuditPlugin', u'&Audit'))
        #Audit Delete All
        self.AuditDeleteAll = QtGui.QAction(tools_menu)
        self.AuditDeleteAll.setText(
            translate(u'AuditPlugin', u'Au&dit Delete all'))
        self.AuditDeleteAll.setStatusTip(
            translate(u'AuditPlugin', u'Deleted all Audit records'))
        self.AuditDeleteAll.setObjectName(u'AuditDeleteAll')
        #Audit Delete
        self.AuditDelete = QtGui.QAction(tools_menu)
        self.AuditDelete.setText(
            translate(u'AuditPlugin', u'Audit &Delete'))
        self.AuditDelete.setStatusTip(
            translate(u'AuditPlugin', u'Delete all audit data to sepecified date'))
        self.AuditDelete.setObjectName(u'AuditDelete')
        #Audit Report
        self.AuditReport = QtGui.QAction(tools_menu)
        self.AuditReport.setText(
            translate(u'AuditPlugin', u'Au&dit &Report'))
        self.AuditReport.setStatusTip(
            translate(u'AuditPlugin', u'Generate Reports on Audit Data'))
        self.AuditReport.setObjectName(u'AuditReport')
        #Audit activation
        AuditIcon = buildIcon(u':/tools/tools_alert.png')
        self.AuditStatus = QtGui.QAction(tools_menu)
        self.AuditStatus.setIcon(AuditIcon)
        self.AuditStatus.setCheckable(True)
        self.AuditStatus.setChecked(False)
        self.AuditStatus.setText(translate(u'AuditPlugin', u'A&udit Status'))
        self.AuditStatus.setStatusTip(
            translate(u'AuditPlugin', u'Start/Stop live song auditing'))
        self.AuditStatus.setShortcut(translate(u'AuditPlugin', u'F4'))
        self.AuditStatus.setObjectName(u'AuditStatus')
        #Add Menus together
        self.toolsMenu.addAction(self.AuditMenu.menuAction())
        self.AuditMenu.addAction(self.AuditStatus)
        self.AuditMenu.addSeparator()
        self.AuditMenu.addAction(self.AuditDeleteAll)
        self.AuditMenu.addAction(self.AuditDelete)
        self.AuditMenu.addSeparator()
        self.AuditMenu.addAction(self.AuditReport)
        # Signals and slots
        QtCore.QObject.connect(self.AuditStatus,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.AuditStatus.setChecked)
        QtCore.QObject.connect(self.AuditStatus,
            QtCore.SIGNAL(u'triggered(bool)'),
            self.toggleAuditState)
        QtCore.QObject.connect(self.AuditDeleteAll,
            QtCore.SIGNAL(u'triggered()'), self.onAuditDeleteAll)
        QtCore.QObject.connect(self.AuditDelete,
            QtCore.SIGNAL(u'triggered()'), self.onAuditDelete)
        QtCore.QObject.connect(self.AuditReport,
            QtCore.SIGNAL(u'triggered()'), self.onAuditReport)
        self.AuditMenu.menuAction().setVisible(False)

    def initialise(self):
        log.info(u'Plugin Initialising')
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'audit_live'), self.onReceiveAudit)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'audit_changed'), self.onUpdateAudit)
        self.auditActive = str_to_bool(
            self.config.get_config(u'audit active', False))
        self.AuditStatus.setChecked(self.auditActive)
        if self.auditmanager is None:
            self.auditmanager = AuditManager(self.config)
        self.auditdeleteform = AuditDeleteForm(self.auditmanager)
        self.auditdetailform = AuditDetailForm(self.auditmanager)
        self.AuditMenu.menuAction().setVisible(True)

    def finalise(self):
        log.info(u'Plugin Finalise')
        self.AuditMenu.menuAction().setVisible(False)
        #stop any events being processed
        self.auditActive = False

    def toggleAuditState(self):
        self.auditActive = not self.auditActive
        self.config.set_config(u'audit active', self.auditActive)

    def onReceiveAudit(self, auditData):
        """
        Audit a live song from SlideController
        """
        if self.auditActive:
            audititem = AuditItem()
            audititem.auditdate = datetime.today()
            audititem.audittime = datetime.now().time()
            audititem.title = auditData[0]
            audititem.copyright = auditData[2]
            audititem.ccl_number = auditData[3]
            audititem.authors = u''
            for author in auditData[1]:
                audititem.authors += author + u' '
            self.auditmanager.insert_audit(audititem)

    def onUpdateAudit(self):
        """
        Someone may have changed to audit details
        Sort out the file and the auditing state
        """
        self.auditActive = str_to_bool(
            self.config.get_config(u'audit active', False))
        self.AuditStatus.setEnabled(True)

    def onAuditDeleteAll(self):
        ret = QtGui.QMessageBox.question(None,
            translate(u'mainWindow', u'Delete All Audit Events?'),
            translate(u'mainWindow', u'Are you sure you want to delete all Audit Data?'),
            QtGui.QMessageBox.StandardButtons(
                QtGui.QMessageBox.Ok |
                QtGui.QMessageBox.Cancel),
            QtGui.QMessageBox.Cancel)
        if ret == QtGui.QMessageBox.Ok:
            self.auditmanager.delete_all()

    def onAuditDelete(self):
        self.auditdeleteform.exec_()

    def onAuditReport(self):
        self.auditdetailform.exec_()

    def about(self):
        return u'<b>Audit Plugin</b> <br>This plugin records the use of songs and when they have been used during a live service'
