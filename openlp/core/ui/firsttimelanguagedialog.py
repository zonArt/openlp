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
The UI widgets of the language selection dialog.
"""
from PyQt4 import QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import create_button_box


class Ui_FirstTimeLanguageDialog(object):
    """
    The UI widgets of the language selection dialog.
    """
    def setupUi(self, languageDialog):
        """
        Set up the UI.
        """
        languageDialog.setObjectName(u'languageDialog')
        languageDialog.resize(300, 50)
        self.dialogLayout = QtGui.QVBoxLayout(languageDialog)
        self.dialogLayout.setContentsMargins(8, 8, 8, 8)
        self.dialogLayout.setSpacing(8)
        self.dialogLayout.setObjectName(u'dialog_layout')
        self.infoLabel = QtGui.QLabel(languageDialog)
        self.infoLabel.setObjectName(u'infoLabel')
        self.dialogLayout.addWidget(self.infoLabel)
        self.languageLayout = QtGui.QHBoxLayout()
        self.languageLayout.setObjectName(u'languageLayout')
        self.languageLabel = QtGui.QLabel(languageDialog)
        self.languageLabel.setObjectName(u'languageLabel')
        self.languageLayout.addWidget(self.languageLabel)
        self.languageComboBox = QtGui.QComboBox(languageDialog)
        self.languageComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.languageComboBox.setObjectName("languageComboBox")
        self.languageLayout.addWidget(self.languageComboBox)
        self.dialogLayout.addLayout(self.languageLayout)
        self.button_box = create_button_box(languageDialog, u'button_box', [u'cancel', u'ok'])
        self.dialogLayout.addWidget(self.button_box)
        self.retranslateUi(languageDialog)
        self.setMaximumHeight(self.sizeHint().height())

    def retranslateUi(self, languageDialog):
        """
        Translate the UI on the fly.
        """
        self.setWindowTitle(translate('OpenLP.FirstTimeLanguageForm', 'Select Translation'))
        self.infoLabel.setText(
            translate('OpenLP.FirstTimeLanguageForm', 'Choose the translation you\'d like to use in OpenLP.'))
        self.languageLabel.setText(translate('OpenLP.FirstTimeLanguageForm', 'Translation:'))
