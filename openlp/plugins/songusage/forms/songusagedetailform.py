# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

from openlp.core.lib import SettingsManager, translate
from openlp.plugins.songusage.lib.db import SongUsageItem
from songusagedetaildialog import Ui_SongUsageDetailDialog

log = logging.getLogger(__name__)

class SongUsageDetailForm(QtGui.QDialog, Ui_SongUsageDetailDialog):
    """
    Class documentation goes here.
    """
    log.info(u'SongUsage Detail Form Loaded')

    def __init__(self, parent=None):
        """
        Initialise the form
        """
        QtGui.QDialog.__init__(self, None)
        self.parent = parent
        self.setupUi(self)

    def initialise(self):
        year = QtCore.QDate().currentDate().year()
        if QtCore.QDate().currentDate().month() < 9:
            year -= 1
        toDate = QtCore.QDate(year, 8, 31)
        fromDate = QtCore.QDate(year - 1, 9, 1)
        self.FromDate.setSelectedDate(fromDate)
        self.ToDate.setSelectedDate(toDate)
        self.FileLineEdit.setText(
            SettingsManager.get_last_dir(self.parent.settingsSection, 1))

    def defineOutputLocation(self):
        path = QtGui.QFileDialog.getExistingDirectory(self,
            translate('SongUsagePlugin.SongUsageDetailForm',
                'Output File Location'),
            SettingsManager.get_last_dir(self.parent.settingsSection, 1))
        path = unicode(path)
        if path != u'':
            SettingsManager.set_last_dir(self.parent.settingsSection, path, 1)
            self.FileLineEdit.setText(path)

    def accept(self):
        log.debug(u'Detailed report generated')
        filename = u'usage_detail_%s_%s.txt' % (
            self.FromDate.selectedDate().toString(u'ddMMyyyy'),
            self.ToDate.selectedDate().toString(u'ddMMyyyy'))
        usage = self.parent.songusagemanager.get_all_objects(
            SongUsageItem, and_(
            SongUsageItem.usagedate >= self.FromDate.selectedDate().toPyDate(),
            SongUsageItem.usagedate < self.ToDate.selectedDate().toPyDate()),
            [SongUsageItem.usagedate, SongUsageItem.usagetime])
        outname = os.path.join(unicode(self.FileLineEdit.text()), filename)
        file = None
        try:
            file = open(outname, u'w')
            for instance in usage:
                record = u'\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n' % (
                    instance.usagedate, instance.usagetime, instance.title,
                    instance.copyright, instance.ccl_number, instance.authors)
                file.write(record)
        except IOError:
            log.exception(u'Failed to write out song usage records')
        finally:
            if file:
                file.close()
