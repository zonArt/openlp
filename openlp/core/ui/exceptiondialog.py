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
The GUI widgets of the exception dialog.
"""

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import create_button, create_button_box


class Ui_ExceptionDialog(object):
    """
    The GUI widgets of the exception dialog.
    """
    def setupUi(self, exceptionDialog):
        """
        Set up the UI.
        """
        exceptionDialog.setObjectName(u'exceptionDialog')
        self.exceptionLayout = QtGui.QVBoxLayout(exceptionDialog)
        self.exceptionLayout.setObjectName(u'exceptionLayout')
        self.messageLayout = QtGui.QHBoxLayout()
        self.messageLayout.setObjectName(u'messageLayout')
        self.messageLayout.addSpacing(12)
        self.bugLabel = QtGui.QLabel(exceptionDialog)
        self.bugLabel.setPixmap(QtGui.QPixmap(u':/graphics/exception.png'))
        self.bugLabel.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.bugLabel.setObjectName(u'bugLabel')
        self.messageLayout.addWidget(self.bugLabel)
        self.messageLayout.addSpacing(12)
        self.messageLabel = QtGui.QLabel(exceptionDialog)
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setObjectName(u'messageLabel')
        self.messageLayout.addWidget(self.messageLabel)
        self.exceptionLayout.addLayout(self.messageLayout)
        self.descriptionExplanation = QtGui.QLabel(exceptionDialog)
        self.descriptionExplanation.setObjectName(u'descriptionExplanation')
        self.exceptionLayout.addWidget(self.descriptionExplanation)
        self.descriptionTextEdit = QtGui.QPlainTextEdit(exceptionDialog)
        self.descriptionTextEdit.setObjectName(u'descriptionTextEdit')
        self.exceptionLayout.addWidget(self.descriptionTextEdit)
        self.descriptionWordCount = QtGui.QLabel(exceptionDialog)
        self.descriptionWordCount.setObjectName(u'descriptionWordCount')
        self.exceptionLayout.addWidget(self.descriptionWordCount)
        self.exceptionTextEdit = QtGui.QPlainTextEdit(exceptionDialog)
        self.exceptionTextEdit.setReadOnly(True)
        self.exceptionTextEdit.setObjectName(u'exceptionTextEdit')
        self.exceptionLayout.addWidget(self.exceptionTextEdit)
        self.sendReportButton = create_button(exceptionDialog, u'sendReportButton',
            icon=u':/general/general_email.png', click=self.onSendReportButtonClicked)
        self.saveReportButton = create_button(exceptionDialog, u'saveReportButton',
            icon=u':/general/general_save.png', click=self.onSaveReportButtonClicked)
        self.attachFileButton = create_button(exceptionDialog, u'attachFileButton',
            icon=u':/general/general_open.png', click=self.onAttachFileButtonClicked)
        self.button_box = create_button_box(exceptionDialog, u'button_box',
            [u'close'], [self.sendReportButton, self.saveReportButton, self.attachFileButton])
        self.exceptionLayout.addWidget(self.button_box)

        self.retranslateUi(exceptionDialog)
        QtCore.QObject.connect(self.descriptionTextEdit,
            QtCore.SIGNAL(u'textChanged()'), self.onDescriptionUpdated)

    def retranslateUi(self, exceptionDialog):
        """
        Translate the widgets on the fly.
        """
        exceptionDialog.setWindowTitle(translate('OpenLP.ExceptionDialog', 'Error Occurred'))
        self.descriptionExplanation.setText(translate('OpenLP.ExceptionDialog',
            'Please enter a description of what you were doing to cause this '
            'error \n(Minimum 20 characters)'))
        self.messageLabel.setText(translate('OpenLP.ExceptionDialog', 'Oops! '
            'OpenLP hit a problem, and couldn\'t recover. The text in the box '
            'below contains information that might be helpful to the OpenLP '
            'developers, so please e-mail it to bugs@openlp.org, along with a '
            'detailed description of what you were doing when the problem '
            'occurred.'))
        self.sendReportButton.setText(translate('OpenLP.ExceptionDialog',
            'Send E-Mail'))
        self.saveReportButton.setText(translate('OpenLP.ExceptionDialog',
            'Save to File'))
        self.attachFileButton.setText(translate('OpenLP.ExceptionDialog',
            'Attach File'))
