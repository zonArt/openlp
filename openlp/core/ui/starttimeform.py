# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
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

from PyQt4 import QtGui

from starttimedialog import Ui_StartTimeDialog

from openlp.core.lib import translate
from openlp.core.lib.ui import UiStrings, critical_error_message_box

class StartTimeForm(QtGui.QDialog, Ui_StartTimeDialog):
    """
    The exception dialog
    """
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

    def exec_(self):
        """
        Run the Dialog with correct heading.
        """
        hour, minutes, seconds = self._time_split(
            self.item[u'service_item'].start_time)
        self.hourSpinBox.setValue(hour)
        self.minuteSpinBox.setValue(minutes)
        self.secondSpinBox.setValue(seconds)
        hours, minutes, seconds = self._time_split(
            self.item[u'service_item'].media_length)
        self.hourFinishSpinBox.setValue(hours)
        self.minuteFinishSpinBox.setValue(minutes)
        self.secondFinishSpinBox.setValue(seconds)
        self.hourFinishLabel.setText(u'%s%s' % (unicode(hour), UiStrings().Hours))
        self.minuteFinishLabel.setText(u'%s%s' %
            (unicode(minutes), UiStrings().Minutes))
        self.secondFinishLabel.setText(u'%s%s' %
            (unicode(seconds), UiStrings().Seconds))
        return QtGui.QDialog.exec_(self)

    def accept(self):
        start = self.hourSpinBox.value() * 3600 + \
            self.minuteSpinBox.value() * 60 + \
            self.secondSpinBox.value()
        end = self.hourFinishSpinBox.value() * 3600 + \
            self.minuteFinishSpinBox.value() * 60 + \
            self.secondFinishSpinBox.value()
        if end > self.item[u'service_item'].media_length:
            critical_error_message_box(
                title=translate('OpenLP.StartTimeForm',
                'Time Validation Error'),
                message=translate('OpenLP.StartTimeForm',
                'End time is set after the end of the media item'))
            return
        elif start > end:
            critical_error_message_box(
                title=translate('OpenLP.StartTimeForm',
                'Time Validation Error'),
                message=translate('OpenLP.StartTimeForm',
                'Start time is after the End Time of the media item'))
            return
        self.item[u'service_item'].start_time = start
        self.item[u'service_item'].end_time = end
        return QtGui.QDialog.accept(self)

    def _time_split(self, seconds):
        hours = seconds / 3600
        seconds -= 3600 * hours
        minutes = seconds / 60
        seconds -= 60 * minutes
        return hours, minutes, seconds