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
"""
The :mod:`ui` module provides standard UI components for OpenLP.
"""
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import build_icon, translate

log = logging.getLogger(__name__)

def add_welcome_page(parent, image):
    """
    Generate an opening welcome page for a wizard using a provided image.

    ``image``
        A splash image for the wizard.
    """
    parent.welcomePage = QtGui.QWizardPage()
    parent.welcomePage.setPixmap(QtGui.QWizard.WatermarkPixmap,
        QtGui.QPixmap(image))
    parent.welcomePage.setObjectName(u'WelcomePage')
    parent.welcomeLayout = QtGui.QVBoxLayout(parent.welcomePage)
    parent.welcomeLayout.setObjectName(u'WelcomeLayout')
    parent.titleLabel = QtGui.QLabel(parent.welcomePage)
    parent.titleLabel.setObjectName(u'TitleLabel')
    parent.welcomeLayout.addWidget(parent.titleLabel)
    parent.welcomeLayout.addSpacing(40)
    parent.informationLabel = QtGui.QLabel(parent.welcomePage)
    parent.informationLabel.setWordWrap(True)
    parent.informationLabel.setObjectName(u'InformationLabel')
    parent.welcomeLayout.addWidget(parent.informationLabel)
    parent.welcomeLayout.addStretch()
    parent.addPage(parent.welcomePage)

def save_cancel_button_box(parent):
    """
    Return a standard dialog button box with save and cancel buttons.
    """
    button_box = QtGui.QDialogButtonBox(parent)
    button_box.setStandardButtons(
        QtGui.QDialogButtonBox.Save | QtGui.QDialogButtonBox.Cancel)
    button_box.setObjectName(u'%sButtonBox' % parent)
    QtCore.QObject.connect(button_box, QtCore.SIGNAL(u'accepted()'),
        parent.accept)
    QtCore.QObject.connect(button_box, QtCore.SIGNAL(u'rejected()'),
        parent.reject)
    return button_box

def critical_error_message_box(title=None, message=None, parent=None,
    question=False):
    """
    Provides a standard critical message box for errors that OpenLP displays
    to users.

    ``title``
        The title for the message box.

    ``message``
        The message to display to the user.

    ``parent``
        The parent UI element to attach the dialog to.

    ``question``
        Should this message box question the user.
    """
    error = translate('OpenLP.Ui', 'Error')
    if question:
        return QtGui.QMessageBox.critical(parent, error, message,
            QtGui.QMessageBox.StandardButtons(
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No))
    data = {u'message': message}
    data[u'title'] = title if title else error
    return Receiver.send_message(u'openlp_error_message', data)

def media_item_combo_box(parent, name):
    """
    Provide a standard combo box for media items.
    """
    combo = QtGui.QComboBox(parent)
    combo.setObjectName(name)
    combo.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
    combo.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    return combo

def delete_push_button(parent, icon=None):
    """
    Return a standard push button with delete label.
    """
    delete_button = QtGui.QPushButton(parent)
    delete_button.setObjectName(u'deleteButton')
    delete_icon = icon if icon else u':/general/general_delete.png'
    delete_button.setIcon(build_icon(delete_icon))
    delete_button.setText(translate('OpenLP.Ui', '&Delete'))
    delete_button.setToolTip(
        translate('OpenLP.Ui', 'Delete the selected item.'))
    QtCore.QObject.connect(delete_button,
        QtCore.SIGNAL(u'clicked()'), parent.onDeleteButtonClicked)
    return delete_button
