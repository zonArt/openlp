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
The layout of the theme
"""
from PyQt4 import QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import create_button_box


class Ui_ThemeLayoutDialog(object):
    """
    The layout of the theme
    """
    def setupUi(self, themeLayoutDialog):
        """
        Set up the UI
        """
        themeLayoutDialog.setObjectName(u'themeLayoutDialogDialog')
        #themeLayoutDialog.resize(300, 200)
        self.previewLayout = QtGui.QVBoxLayout(themeLayoutDialog)
        self.previewLayout.setObjectName(u'previewLayout')
        self.previewArea = QtGui.QWidget(themeLayoutDialog)
        self.previewArea.setObjectName(u'previewArea')
        self.previewAreaLayout = QtGui.QGridLayout(self.previewArea)
        self.previewAreaLayout.setMargin(0)
        self.previewAreaLayout.setColumnStretch(0, 1)
        self.previewAreaLayout.setRowStretch(0, 1)
        self.previewAreaLayout.setObjectName(u'previewAreaLayout')
        self.themeDisplayLabel = QtGui.QLabel(self.previewArea)
        self.themeDisplayLabel.setFrameShape(QtGui.QFrame.Box)
        self.themeDisplayLabel.setScaledContents(True)
        self.themeDisplayLabel.setObjectName(u'themeDisplayLabel')
        self.previewAreaLayout.addWidget(self.themeDisplayLabel)
        self.previewLayout.addWidget(self.previewArea)
        self.mainColourLabel = QtGui.QLabel(self.previewArea)
        self.mainColourLabel.setObjectName(u'mainColourLabel')
        self.previewLayout.addWidget(self.mainColourLabel)
        self.footerColourLabel = QtGui.QLabel(self.previewArea)
        self.footerColourLabel.setObjectName(u'footerColourLabel')
        self.previewLayout.addWidget(self.footerColourLabel)
        self.button_box = create_button_box(themeLayoutDialog, u'button_box', [u'ok'])
        self.previewLayout.addWidget(self.button_box)
        self.retranslateUi(themeLayoutDialog)

    def retranslateUi(self, themeLayoutDialog):
        """
        Translate the UI on the fly
        """
        themeLayoutDialog.setWindowTitle(translate('OpenLP.StartTimeForm', 'Theme Layout'))
        self.mainColourLabel.setText(translate('OpenLP.StartTimeForm', 'The blue box shows the main area.'))
        self.footerColourLabel.setText(translate('OpenLP.StartTimeForm', 'The red box shows the footer.'))
