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

class Ui_LanguageDialog(object):
    def setupUi(self, language_dialog):
        language_dialog.setObjectName('language_dialog')
        language_dialog.resize(400, 165)
        self.language_layout = QtGui.QVBoxLayout(language_dialog)
        self.language_layout.setSpacing(8)
        self.language_layout.setMargin(8)
        self.language_layout.setObjectName('language_layout')
        self.bible_label = QtGui.QLabel(language_dialog)
        self.bible_label.setObjectName('bible_label')
        self.language_layout.addWidget(self.bible_label)
        self.info_label = QtGui.QLabel(language_dialog)
        self.info_label.setWordWrap(True)
        self.info_label.setObjectName('info_label')
        self.language_layout.addWidget(self.info_label)
        self.language_h_box_layout = QtGui.QHBoxLayout()
        self.language_h_box_layout.setSpacing(8)
        self.language_h_box_layout.setObjectName('language_h_box_layout')
        self.language_label = QtGui.QLabel(language_dialog)
        self.language_label.setObjectName('language_label')
        self.language_h_box_layout.addWidget(self.language_label)
        self.language_combo_box = QtGui.QComboBox(language_dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.language_combo_box.sizePolicy().hasHeightForWidth())
        self.language_combo_box.setSizePolicy(sizePolicy)
        self.language_combo_box.setObjectName('language_combo_box')
        self.language_h_box_layout.addWidget(self.language_combo_box)
        self.language_layout.addLayout(self.language_h_box_layout)
        self.button_box = create_button_box(language_dialog, 'button_box', ['cancel', 'ok'])
        self.language_layout.addWidget(self.button_box)

        self.retranslateUi(language_dialog)

    def retranslateUi(self, language_dialog):
        language_dialog.setWindowTitle(translate('BiblesPlugin.LanguageDialog', 'Select Language'))
        self.bible_label.setText(translate('BiblesPlugin.LanguageDialog', ''))
        self.info_label.setText(translate('BiblesPlugin.LanguageDialog',
            'OpenLP is unable to determine the language of this translation of the Bible. Please select the language '
            'from the list below.'))
        self.language_label.setText(translate('BiblesPlugin.LanguageDialog', 'Language:'))
