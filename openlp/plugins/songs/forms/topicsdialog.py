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

from PyQt4 import QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import create_button_box

class Ui_TopicsDialog(object):
    def setupUi(self, topicsDialog):
        topicsDialog.setObjectName(u'topicsDialog')
        topicsDialog.resize(300, 10)
        self.dialogLayout = QtGui.QVBoxLayout(topicsDialog)
        self.dialogLayout.setObjectName(u'dialog_layout')
        self.nameLayout = QtGui.QFormLayout()
        self.nameLayout.setObjectName(u'nameLayout')
        self.nameLabel = QtGui.QLabel(topicsDialog)
        self.nameLabel.setObjectName(u'nameLabel')
        self.nameEdit = QtGui.QLineEdit(topicsDialog)
        self.nameEdit.setObjectName(u'nameEdit')
        self.nameLabel.setBuddy(self.nameEdit)
        self.nameLayout.addRow(self.nameLabel, self.nameEdit)
        self.dialogLayout.addLayout(self.nameLayout)
        self.button_box = create_button_box(topicsDialog, u'button_box', [u'cancel', u'save'])
        self.dialogLayout.addWidget(self.button_box)
        self.retranslateUi(topicsDialog)
        topicsDialog.setMaximumHeight(topicsDialog.sizeHint().height())

    def retranslateUi(self, topicsDialog):
        topicsDialog.setWindowTitle(translate('SongsPlugin.TopicsForm', 'Topic Maintenance'))
        self.nameLabel.setText(translate('SongsPlugin.TopicsForm', 'Topic name:'))
