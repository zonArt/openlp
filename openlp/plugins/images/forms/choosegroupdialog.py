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
    def setupUi(self, choose_group_dialog):
        choose_group_dialog.setObjectName(u'choose_group_dialog')
        choose_group_dialog.resize(440, 119)
        self.choose_group_layout = QtGui.QFormLayout(choose_group_dialog)
        self.choose_group_layout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.choose_group_layout.setMargin(8)
        self.choose_group_layout.setSpacing(8)
        self.choose_group_layout.setObjectName(u'choose_group_layout')
        self.group_question_label = QtGui.QLabel(choose_group_dialog)
        self.group_question_label.setWordWrap(True)
        self.group_question_label.setObjectName(u'group_question_label')
        self.choose_group_layout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.group_question_label)
        self.group_combobox = QtGui.QComboBox(choose_group_dialog)
        self.group_combobox.setObjectName(u'group_combobox')
        self.choose_group_layout.setWidget(2, QtGui.QFormLayout.FieldRole, self.group_combobox)
        self.group_button_box = create_button_box(choose_group_dialog, u'buttonBox', [u'ok'])
        self.choose_group_layout.setWidget(3, QtGui.QFormLayout.FieldRole, self.group_button_box)

        self.retranslateUi(choose_group_dialog)
        QtCore.QMetaObject.connectSlotsByName(choose_group_dialog)

    def retranslateUi(self, choose_group_dialog):
        choose_group_dialog.setWindowTitle(translate('ImagePlugin.ChooseGroupForm', 'Choose group'))
        self.group_question_label.setText(translate('ImagePlugin.ChooseGroupForm',
            'To which group do you want these images to be added?'))
