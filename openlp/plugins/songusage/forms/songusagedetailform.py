# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
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

import logging
import os

from PyQt4 import QtCore, QtGui
from sqlalchemy.sql import and_

from openlp.core.lib import SettingsManager, translate, Receiver, \
    check_directory_exists
from openlp.core.lib.settings import Settings
from openlp.plugins.songusage.lib.db import SongUsageItem
from songusagedetaildialog import Ui_SongUsageDetailDialog

log = logging.getLogger(__name__)

class SongUsageDetailForm(QtGui.QDialog, Ui_SongUsageDetailDialog):
    """
    Class documentation goes here.
    """
    log.info(u'SongUsage Detail Form Loaded')

    def __init__(self, plugin, parent):
        """
        Initialise the form
        """
        QtGui.QDialog.__init__(self, parent)
        self.plugin = plugin
        self.setupUi(self)

    def initialise(self):
        """
        We need to set up the screen
        """
        year = QtCore.QDate().currentDate().year()
        if QtCore.QDate().currentDate().month() < 9:
            year -= 1
        toDate = Settings().value(
            u'songusage/to date',
            QtCore.QVariant(QtCore.QDate(year, 8, 31))).toDate()
        fromDate = Settings().value(
            u'songusage/from date',
            QtCore.QVariant(QtCore.QDate(year - 1, 9, 1))).toDate()
        self.fromDate.setSelectedDate(fromDate)
        self.toDate.setSelectedDate(toDate)
        self.fileLineEdit.setText(
            SettingsManager.get_last_dir(self.plugin.settingsSection, 1))

    def defineOutputLocation(self):
        """
        Triggered when the Directory selection button is clicked
        """
        path = QtGui.QFileDialog.getExistingDirectory(self,
            translate('SongUsagePlugin.SongUsageDetailForm',
                'Output File Location'),
            SettingsManager.get_last_dir(self.plugin.settingsSection, 1))
        path = unicode(path)
        if path:
            SettingsManager.set_last_dir(self.plugin.settingsSection, path, 1)
            self.fileLineEdit.setText(path)

    def accept(self):
        """
        Ok was triggered so lets save the data and run the report
        """
        log.debug(u'accept')
        path = unicode(self.fileLineEdit.text())
        if path == u'':
            Receiver.send_message(u'openlp_error_message', {
                u'title': translate('SongUsagePlugin.SongUsageDetailForm',
                'Output Path Not Selected'),
                u'message': unicode(translate(
                'SongUsagePlugin.SongUsageDetailForm', 'You have not set a '
                'valid output location for your song usage report. Please '
                'select an existing path on your computer.'))})
            return
        check_directory_exists(path)
        filename = unicode(translate('SongUsagePlugin.SongUsageDetailForm',
            'usage_detail_%s_%s.txt')) % (
            self.fromDate.selectedDate().toString(u'ddMMyyyy'),
            self.toDate.selectedDate().toString(u'ddMMyyyy'))
        Settings().setValue(u'songusage/from date',
            QtCore.QVariant(self.fromDate.selectedDate()))
        Settings().setValue(u'songusage/to date',
            QtCore.QVariant(self.toDate.selectedDate()))
        usage = self.plugin.manager.get_all_objects(
            SongUsageItem, and_(
            SongUsageItem.usagedate >= self.fromDate.selectedDate().toPyDate(),
            SongUsageItem.usagedate < self.toDate.selectedDate().toPyDate()),
            [SongUsageItem.usagedate, SongUsageItem.usagetime])
        outname = os.path.join(path, filename)
        fileHandle = None
        try:
            fileHandle = open(outname, u'w')
            for instance in usage:
                record = u'\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",' \
                    u'\"%s\",\"%s\"\n' % (instance.usagedate,
                    instance.usagetime, instance.title, instance.copyright,
                    instance.ccl_number, instance.authors,
                    instance.plugin_name, instance.source)
                fileHandle.write(record.encode(u'utf-8'))
            Receiver.send_message(u'openlp_information_message', {
                u'title': translate('SongUsagePlugin.SongUsageDetailForm',
                'Report Creation'),
                u'message': unicode(translate(
                'SongUsagePlugin.SongUsageDetailForm', 'Report \n%s \n'
                'has been successfully created. ')) % outname})
        except IOError:
            log.exception(u'Failed to write out song usage records')
        finally:
            if fileHandle:
                fileHandle.close()
        self.close()
