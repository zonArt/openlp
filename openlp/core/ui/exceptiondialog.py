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
    def setupUi(self, exception_dialog):
        """
        Set up the UI.
        """
        exception_dialog.setObjectName(u'exception_dialog')
        self.exception_layout = QtGui.QVBoxLayout(exception_dialog)
        self.exception_layout.setObjectName(u'exception_layout')
        self.message_layout = QtGui.QHBoxLayout()
        self.message_layout.setObjectName(u'messageLayout')
        self.message_layout.addSpacing(12)
        self.bug_label = QtGui.QLabel(exception_dialog)
        self.bug_label.setPixmap(QtGui.QPixmap(u':/graphics/exception.png'))
        self.bug_label.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.bug_label.setObjectName(u'bug_label')
        self.message_layout.addWidget(self.bug_label)
        self.message_layout.addSpacing(12)
        self.message_label = QtGui.QLabel(exception_dialog)
        self.message_label.setWordWrap(True)
        self.message_label.setObjectName(u'message_label')
        self.message_layout.addWidget(self.message_label)
        self.exception_layout.addLayout(self.message_layout)
        self.description_explanation = QtGui.QLabel(exception_dialog)
        self.description_explanation.setObjectName(u'description_explanation')
        self.exception_layout.addWidget(self.description_explanation)
        self.description_text_edit = QtGui.QPlainTextEdit(exception_dialog)
        self.description_text_edit.setObjectName(u'description_text_edit')
        self.exception_layout.addWidget(self.description_text_edit)
        self.description_word_count = QtGui.QLabel(exception_dialog)
        self.description_word_count.setObjectName(u'description_word_count')
        self.exception_layout.addWidget(self.description_word_count)
        self.exception_text_edit = QtGui.QPlainTextEdit(exception_dialog)
        self.exception_text_edit.setReadOnly(True)
        self.exception_text_edit.setObjectName(u'exception_text_edit')
        self.exception_layout.addWidget(self.exception_text_edit)
        self.send_report_button = create_button(exception_dialog, u'send_report_button',
            icon=u':/general/general_email.png', click=self.onSendReportButtonClicked)
        self.save_report_button = create_button(exception_dialog, u'save_report_button',
            icon=u':/general/general_save.png', click=self.onSaveReportButtonClicked)
        self.attach_tile_button = create_button(exception_dialog, u'attach_tile_button',
            icon=u':/general/general_open.png', click=self.onAttachFileButtonClicked)
        self.button_box = create_button_box(exception_dialog, u'button_box',
            [u'close'], [self.send_report_button, self.save_report_button, self.attach_tile_button])
        self.exception_layout.addWidget(self.button_box)

        self.retranslateUi(exception_dialog)
        self.description_text_edit.textChanged.connect(self.onDescriptionUpdated)

    def retranslateUi(self, exception_dialog):
        """
        Translate the widgets on the fly.
        """
        exception_dialog.setWindowTitle(translate('OpenLP.ExceptionDialog', 'Error Occurred'))
        self.description_explanation.setText(translate('OpenLP.ExceptionDialog',
            'Please enter a description of what you were doing to cause this '
            'error \n(Minimum 20 characters)'))
        self.message_label.setText(translate('OpenLP.ExceptionDialog', 'Oops! '
            'OpenLP hit a problem, and couldn\'t recover. The text in the box '
            'below contains information that might be helpful to the OpenLP '
            'developers, so please e-mail it to bugs@openlp.org, along with a '
            'detailed description of what you were doing when the problem '
            'occurred.'))
        self.send_report_button.setText(translate('OpenLP.ExceptionDialog', 'Send E-Mail'))
        self.save_report_button.setText(translate('OpenLP.ExceptionDialog', 'Save to File'))
        self.attach_tile_button.setText(translate('OpenLP.ExceptionDialog', 'Attach File'))
