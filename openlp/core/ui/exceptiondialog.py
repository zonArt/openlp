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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, build_icon

class Ui_ExceptionDialog(object):
    def setupUi(self, exceptionDialog):
        exceptionDialog.setObjectName(u'exceptionDialog')
        self.exceptionLayout = QtGui.QVBoxLayout(exceptionDialog)
        self.exceptionLayout.setObjectName(u'exceptionLayout')
        self.messageLayout = QtGui.QHBoxLayout()
        self.messageLayout.setObjectName(u'messageLayout')
        self.messageLayout.addSpacing(12)
        self.bugLabel = QtGui.QLabel(exceptionDialog)
        self.bugLabel.setPixmap(QtGui.QPixmap(u':/graphics/exception.png'))
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
        self.exceptionButtonBox = QtGui.QDialogButtonBox(exceptionDialog)
        self.exceptionButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.exceptionButtonBox.setObjectName(u'exceptionButtonBox')
        self.exceptionLayout.addWidget(self.exceptionButtonBox)
        self.sendReportButton = QtGui.QPushButton(exceptionDialog)
        self.sendReportButton.setIcon(build_icon(
            u':/general/general_email.png'))
        self.sendReportButton.setObjectName(u'sendReportButton')
        self.exceptionButtonBox.addButton(self.sendReportButton,
            QtGui.QDialogButtonBox.ActionRole)
        self.saveReportButton = QtGui.QPushButton(exceptionDialog)
        self.saveReportButton.setIcon(build_icon(u':/general/general_save.png'))
        self.saveReportButton.setObjectName(u'saveReportButton')
        self.exceptionButtonBox.addButton(self.saveReportButton,
            QtGui.QDialogButtonBox.ActionRole)
        self.attachFileButton = QtGui.QPushButton(exceptionDialog)
        self.attachFileButton.setIcon(build_icon(u':/general/general_open.png'))
        self.attachFileButton.setObjectName(u'attachFileButton')
        self.exceptionButtonBox.addButton(self.attachFileButton,
            QtGui.QDialogButtonBox.ActionRole)

        self.retranslateUi(exceptionDialog)
        QtCore.QObject.connect(self.descriptionTextEdit,
            QtCore.SIGNAL(u'textChanged()'), self.onDescriptionUpdated)
        QtCore.QObject.connect(self.exceptionButtonBox,
            QtCore.SIGNAL(u'rejected()'), exceptionDialog.reject)
        QtCore.QObject.connect(self.sendReportButton,
            QtCore.SIGNAL(u'pressed()'), self.onSendReportButtonPressed)
        QtCore.QObject.connect(self.saveReportButton,
            QtCore.SIGNAL(u'pressed()'), self.onSaveReportButtonPressed)
        QtCore.QObject.connect(self.attachFileButton,
            QtCore.SIGNAL(u'pressed()'), self.onAttachFileButtonPressed)
        QtCore.QMetaObject.connectSlotsByName(exceptionDialog)

    def retranslateUi(self, exceptionDialog):
        exceptionDialog.setWindowTitle(
            translate('OpenLP.ExceptionDialog', 'Error Occurred'))
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
