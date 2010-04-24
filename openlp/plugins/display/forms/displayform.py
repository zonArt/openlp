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

from PyQt4 import QtGui, QtCore

from openlp.plugins.alerts.lib.models import AlertItem

from displaydialog import Ui_DisplaysDialog

class DisplayForm(QtGui.QDialog, Ui_DisplaysDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent, screens):
        """
        Constructor
        """
        self.parent = parent
        self.screens = screens
        self.item_id = None
        QtGui.QDialog.__init__(self, None)
        self.setupUi(self)

    def initialise(self):
        self.Xpos.setText(unicode(self.screens.current[u'size'].x()))
        self.Ypos.setText(unicode(self.screens.current[u'size'].y()))
        self.Height.setText(unicode(self.screens.current[u'size'].height()))
        self.Width.setText(unicode(self.screens.current[u'size'].width()))
        self.XposEdit.setText(unicode(self.screens.override[u'size'].x()))
        self.YposEdit.setText(unicode(self.screens.override[u'size'].y()))
        self.HeightEdit.setText(unicode(self.screens.override[u'size'].height()))
        self.WidthEdit.setText(unicode(self.screens.override[u'size'].width()))

    def close(self):
        self.screens.override[u'size'] = QtCore.QRect(int(self.XposEdit.text()),\
            int(self.YposEdit.text()), int(self.WidthEdit.text()),\
            int(self.HeightEdit.text()))
        return QtGui.QDialog.close(self)
