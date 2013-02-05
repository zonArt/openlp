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

from openlp.core.lib import SpellTextEdit, UiStrings, translate
from openlp.core.lib.ui import create_button, create_button_box

class Ui_CustomSlideEditDialog(object):
    def setupUi(self, customSlideEditDialog):
        customSlideEditDialog.setObjectName(u'customSlideEditDialog')
        customSlideEditDialog.resize(350, 300)
        self.dialogLayout = QtGui.QVBoxLayout(customSlideEditDialog)
        self.slideTextEdit = SpellTextEdit(self)
        self.slideTextEdit.setObjectName(u'slideTextEdit')
        self.dialogLayout.addWidget(self.slideTextEdit)
        self.splitButton = create_button(customSlideEditDialog, u'splitButton', icon=u':/general/general_add.png')
        self.insertButton = create_button(customSlideEditDialog, u'insertButton', icon=u':/general/general_add.png')
        self.button_box = create_button_box(customSlideEditDialog, u'button_box', [u'cancel', u'save'],
            [self.splitButton, self.insertButton])
        self.dialogLayout.addWidget(self.button_box)
        self.retranslateUi(customSlideEditDialog)

    def retranslateUi(self, customSlideEditDialog):
        customSlideEditDialog.setWindowTitle(translate('CustomPlugin.EditVerseForm', 'Edit Slide'))
        self.splitButton.setText(UiStrings().Split)
        self.splitButton.setToolTip(UiStrings().SplitToolTip)
        self.insertButton.setText(translate('CustomPlugin.EditCustomForm', 'Insert Slide'))
        self.insertButton.setToolTip(translate('CustomPlugin.EditCustomForm',
            'Split a slide into two by inserting a slide splitter.'))
