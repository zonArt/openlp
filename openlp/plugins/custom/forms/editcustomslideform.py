# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

import logging

from PyQt4 import QtCore, QtGui

from editcustomslidedialog import Ui_CustomSlideEditDialog

log = logging.getLogger(__name__)

class EditCustomSlideForm(QtGui.QDialog, Ui_CustomSlideEditDialog):
    """
    Class documentation goes here.
    """
    log.info(u'Custom Verse Editor loaded')
    def __init__(self, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        # Connecting signals and slots
        QtCore.QObject.connect(self.splitButton,
            QtCore.SIGNAL(u'pressed()'), self.onSplitButtonPressed)

    def setText(self, text):
        """
        Set the text for slideTextEdit.

        ``text``
            The text (unicode).
        """
        self.slideTextEdit.clear()
        if text:
            self.slideTextEdit.setPlainText(text)
        self.slideTextEdit.setFocus()

    def getText(self):
        """
        Returns a list with all slides.
        """
        return self.slideTextEdit.toPlainText().split(u'\n[---]\n')

    def onSplitButtonPressed(self):
        """
        Adds a slide split at the cursor.
        """
        if self.slideTextEdit.textCursor().columnNumber() != 0:
            self.slideTextEdit.insertPlainText(u'\n')
        self.slideTextEdit.insertPlainText(u'[---]\n' )
        self.slideTextEdit.setFocus()