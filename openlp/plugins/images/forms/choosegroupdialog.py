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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import create_button_box

class Ui_ChooseGroupDialog(object):
    def setupUi(self, chooseGroupDialog):
        chooseGroupDialog.setObjectName(u'chooseGroupDialog')
        chooseGroupDialog.resize(440, 119)
        self.chooseGroupLayout = QtGui.QFormLayout(chooseGroupDialog)
        self.chooseGroupLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.chooseGroupLayout.setMargin(8)
        self.chooseGroupLayout.setSpacing(8)
        self.chooseGroupLayout.setObjectName(u'chooseGroupLayout')
        self.groupQuestionLabel = QtGui.QLabel(chooseGroupDialog)
        self.groupQuestionLabel.setWordWrap(True)
        self.groupQuestionLabel.setObjectName(u'groupQuestionLabel')
        self.chooseGroupLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.groupQuestionLabel)
        self.groupComboBox = QtGui.QComboBox(chooseGroupDialog)
        self.groupComboBox.setObjectName(u'groupComboBox')
        self.chooseGroupLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.groupComboBox)
        self.groupButtonBox = create_button_box(chooseGroupDialog, u'buttonBox', [u'ok'])
        self.chooseGroupLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.groupButtonBox)

        self.retranslateUi(chooseGroupDialog)
        QtCore.QMetaObject.connectSlotsByName(chooseGroupDialog)

    def retranslateUi(self, chooseGroupDialog):
        chooseGroupDialog.setWindowTitle(translate('ImagePlugin.ChooseGroupForm', 'Choose group'))
        self.groupQuestionLabel.setText(translate('ImagePlugin.ChooseGroupForm',
            'To which group do you want these images to be added?'))

