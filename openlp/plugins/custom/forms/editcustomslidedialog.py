# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, SpellTextEdit, build_icon
from openlp.core.lib.ui import create_button_box, UiStrings

class Ui_CustomSlideEditDialog(object):
    def setupUi(self, customSlideEditDialog):
        customSlideEditDialog.setObjectName(u'customSlideEditDialog')
        customSlideEditDialog.resize(350, 300)
        self.dialogLayout = QtGui.QVBoxLayout(customSlideEditDialog)
        self.slideTextEdit = SpellTextEdit(self)
        self.slideTextEdit.setObjectName(u'slideTextEdit')
        self.dialogLayout.addWidget(self.slideTextEdit)
        self.splitButton = QtGui.QPushButton(customSlideEditDialog)
        self.splitButton.setIcon(build_icon(u':/general/general_add.png'))
        self.splitButton.setObjectName(u'splitButton')
        self.insertButton = QtGui.QPushButton(customSlideEditDialog)
        self.insertButton.setIcon(build_icon(u':/general/general_add.png'))
        self.insertButton.setObjectName(u'insertButton')
        self.buttonBox = create_button_box(customSlideEditDialog,
            [u'cancel', u'save'], [self.splitButton, self.insertButton])
        self.buttonBox.setObjectName(u'buttonBox')
        self.dialogLayout.addWidget(self.buttonBox)
        self.retranslateUi(customSlideEditDialog)
        QtCore.QMetaObject.connectSlotsByName(customSlideEditDialog)

    def retranslateUi(self, customSlideEditDialog):
        self.splitButton.setText(UiStrings().Split)
        self.splitButton.setToolTip(UiStrings().SplitToolTip)
        self.insertButton.setText(
            translate('CustomPlugin.EditCustomForm', 'Insert Slide'))
        self.insertButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Split a slide into two '
            'by inserting a slide splitter.'))
