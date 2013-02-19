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
"""
The actual start time form.
"""
from PyQt4 import QtGui

from starttimedialog import Ui_StartTimeDialog

from openlp.core.lib import UiStrings, Registry, translate
from openlp.core.lib.ui import critical_error_message_box


class StartTimeForm(QtGui.QDialog, Ui_StartTimeDialog):
    """
    The start time dialog
    """
    def __init__(self):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, self.main_window)
        self.setupUi(self)

    def exec_(self):
        """
        Run the Dialog with correct heading.
        """
        hour, minutes, seconds = self._time_split(self.item[u'service_item'].start_time)
        self.hourSpinBox.setValue(hour)
        self.minuteSpinBox.setValue(minutes)
        self.secondSpinBox.setValue(seconds)
        hours, minutes, seconds = self._time_split(self.item[u'service_item'].media_length)
        self.hourFinishSpinBox.setValue(hours)
        self.minuteFinishSpinBox.setValue(minutes)
        self.secondFinishSpinBox.setValue(seconds)
        self.hourFinishLabel.setText(u'%s%s' % (unicode(hour), UiStrings().Hours))
        self.minuteFinishLabel.setText(u'%s%s' % (unicode(minutes), UiStrings().Minutes))
        self.secondFinishLabel.setText(u'%s%s' % (unicode(seconds), UiStrings().Seconds))
        return QtGui.QDialog.exec_(self)

    def accept(self):
        """
        When the dialog succeeds, this is run
        """
        start = self.hourSpinBox.value() * 3600 + \
            self.minuteSpinBox.value() * 60 + \
            self.secondSpinBox.value()
        end = self.hourFinishSpinBox.value() * 3600 + \
            self.minuteFinishSpinBox.value() * 60 + \
            self.secondFinishSpinBox.value()
        if end > self.item[u'service_item'].media_length:
            critical_error_message_box(title=translate('OpenLP.StartTimeForm', 'Time Validation Error'),
                message=translate('OpenLP.StartTimeForm', 'Finish time is set after the end of the media item'))
            return
        elif start > end:
            critical_error_message_box(title=translate('OpenLP.StartTimeForm', 'Time Validation Error'),
                message=translate('OpenLP.StartTimeForm', 'Start time is after the finish time of the media item'))
            return
        self.item[u'service_item'].start_time = start
        self.item[u'service_item'].end_time = end
        return QtGui.QDialog.accept(self)

    def _time_split(self, seconds):
        """
        Split time up into hours minutes and seconds from secongs
        """
        hours = seconds / 3600
        seconds -= 3600 * hours
        minutes = seconds / 60
        seconds -= 60 * minutes
        return hours, minutes, seconds

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, u'_main_window'):
            self._main_window = Registry().get(u'main_window')
        return self._main_window

    main_window = property(_get_main_window)
