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
    def setupUi(self, languageDialog):
        languageDialog.setObjectName(u'languageDialog')
        languageDialog.resize(400, 165)
        self.languageLayout = QtGui.QVBoxLayout(languageDialog)
        self.languageLayout.setSpacing(8)
        self.languageLayout.setMargin(8)
        self.languageLayout.setObjectName(u'languageLayout')
        self.bibleLabel = QtGui.QLabel(languageDialog)
        self.bibleLabel.setObjectName(u'bibleLabel')
        self.languageLayout.addWidget(self.bibleLabel)
        self.infoLabel = QtGui.QLabel(languageDialog)
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setObjectName(u'infoLabel')
        self.languageLayout.addWidget(self.infoLabel)
        self.languageHBoxLayout = QtGui.QHBoxLayout()
        self.languageHBoxLayout.setSpacing(8)
        self.languageHBoxLayout.setObjectName(u'languageHBoxLayout')
        self.languageLabel = QtGui.QLabel(languageDialog)
        self.languageLabel.setObjectName(u'languageLabel')
        self.languageHBoxLayout.addWidget(self.languageLabel)
        self.languageComboBox = QtGui.QComboBox(languageDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.languageComboBox.sizePolicy().hasHeightForWidth())
        self.languageComboBox.setSizePolicy(sizePolicy)
        self.languageComboBox.setObjectName(u'languageComboBox')
        self.languageHBoxLayout.addWidget(self.languageComboBox)
        self.languageLayout.addLayout(self.languageHBoxLayout)
        self.button_box = create_button_box(languageDialog, u'button_box', [u'cancel', u'ok'])
        self.languageLayout.addWidget(self.button_box)

        self.retranslateUi(languageDialog)

    def retranslateUi(self, languageDialog):
        languageDialog.setWindowTitle(translate('BiblesPlugin.LanguageDialog', 'Select Language'))
        self.bibleLabel.setText(translate('BiblesPlugin.LanguageDialog', ''))
        self.infoLabel.setText(translate('BiblesPlugin.LanguageDialog',
            'OpenLP is unable to determine the language of this translation of the Bible. Please select the language '
            'from the list below.'))
        self.languageLabel.setText(translate('BiblesPlugin.LanguageDialog', 'Language:'))
