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

from openlp.core.lib import build_icon, Receiver, translate

log = logging.getLogger(__name__)

class UiStrings(object):
    """
    Provide standard strings for objects to use.
    """
    # These strings should need a good reason to be retranslated elsewhere.
    # Should some/more/less of these have an &amp; attached?
    Add = translate('OpenLP.Ui', '&Add')
    AddANew = unicode(translate('OpenLP.Ui', 'Add a new %s.'))
    AddSelectService = unicode(translate('OpenLP.Ui',
        'Add the selected %s to the service.'))
    Advanced = translate('OpenLP.Ui', 'Advanced')
    AllFiles = translate('OpenLP.Ui', 'All Files')
    Authors = translate('OpenLP.Ui', 'Authors')
    CreateANew = unicode(translate('OpenLP.Ui', 'Create a new %s.'))
    CopyToHtml = translate('OpenLP.Ui', 'Copy to Html')
    CopyToText = translate('OpenLP.Ui', 'Copy to Text')
    Delete = translate('OpenLP.Ui', '&Delete')
    DeleteSelect = unicode(translate('OpenLP.Ui', 'Delete the selected %s.'))
    DeleteType = unicode(translate('OpenLP.Ui', 'Delete %s'))
    Edit = translate('OpenLP.Ui', '&Edit')
    EditSelect = unicode(translate('OpenLP.Ui', 'Edit the selected %s.'))
    EditType = unicode(translate('OpenLP.Ui', 'Edit %s'))
    Error = translate('OpenLP.Ui', 'Error')
    ExportType = unicode(translate('OpenLP.Ui', 'Export %s'))
    Import = translate('OpenLP.Ui', 'Import')
    ImportType = unicode(translate('OpenLP.Ui', 'Import %s'))
    LengthTime = unicode(translate('OpenLP.Ui', 'Length %s'))
    Live = translate('OpenLP.Ui', 'Live')
    Load = translate('OpenLP.Ui', 'Load')
    LoadANew = unicode(translate('OpenLP.Ui', 'Load a new %s.'))
    New = translate('OpenLP.Ui', 'New')
    NewType = unicode(translate('OpenLP.Ui', 'New %s'))
    OLPV2 = translate('OpenLP.Ui', 'OpenLP 2.0')
    OpenType = unicode(translate('OpenLP.Ui', 'Open %s'))
    Preview = translate('OpenLP.Ui', 'Preview')
    PreviewSelect = unicode(translate('OpenLP.Ui', 'Preview the selected %s.'))
    ReplaceBG = translate('OpenLP.Ui', 'Replace Background')
    ReplaceLiveBG = translate('OpenLP.Ui', 'Replace Live Background')
    ResetBG = translate('OpenLP.Ui', 'Reset Background')
    ResetLiveBG = translate('OpenLP.Ui', 'Reset Live Background')
    SaveType = unicode(translate('OpenLP.Ui', 'Save %s'))
    SendSelectLive = unicode(translate('OpenLP.Ui',
        'Send the selected %s live.'))
    Service = translate('OpenLP.Ui', 'Service')
    StartTimeCode = unicode(translate('OpenLP.Ui', 'Start %s'))
    Theme = translate('OpenLP.Ui', 'Theme')
    Themes = translate('OpenLP.Ui', 'Themes')

def add_welcome_page(parent, image):
    """
    Generate an opening welcome page for a wizard using a provided image.

    ``parent``
        A ``QWizard`` object to add the welcome page to.

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

def create_accept_reject_button_box(parent, okay=False):
    """
    Creates a standard dialog button box with two buttons. The buttons default
    to save and cancel but the ``okay`` parameter can be used to make the
    buttons okay and cancel instead.
    The button box is connected to the parent's ``accept()`` and ``reject()``
    methods to handle the default ``accepted()`` and ``rejected()`` signals.

    ``parent``
        The parent object.  This should be a ``QWidget`` descendant.

    ``okay``
        If true creates an okay/cancel combination instead of save/cancel.
    """
    button_box = QtGui.QDialogButtonBox(parent)
    accept_button = QtGui.QDialogButtonBox.Save
    if okay:
        accept_button = QtGui.QDialogButtonBox.Ok
    button_box.setStandardButtons(accept_button | QtGui.QDialogButtonBox.Cancel)
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
    if question:
        return QtGui.QMessageBox.critical(parent, UiStrings.Error, message,
            QtGui.QMessageBox.StandardButtons(
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No))
    data = {u'message': message}
    data[u'title'] = title if title else UiStrings.Error
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

def create_delete_push_button(parent, icon=None):
    """
    Creates a standard push button with a delete label and optional icon.  The
    button is connected to the parent's ``onDeleteButtonClicked()`` method to
    handle the ``clicked()`` signal.

    ``parent``
        The parent object.  This should be a ``QWidget`` descendant.

    ``icon``
        An icon to display on the button.  This can be either a ``QIcon``, a
        resource path or a file name.
    """
    delete_button = QtGui.QPushButton(parent)
    delete_button.setObjectName(u'deleteButton')
    delete_icon = icon if icon else u':/general/general_delete.png'
    delete_button.setIcon(build_icon(delete_icon))
    delete_button.setText(UiStrings.Delete)
    delete_button.setToolTip(
        translate('OpenLP.Ui', 'Delete the selected item.'))
    QtCore.QObject.connect(delete_button,
        QtCore.SIGNAL(u'clicked()'), parent.onDeleteButtonClicked)
    return delete_button

def create_up_down_push_button_set(parent):
    """
    Creates a standard set of two push buttons, one for up and the other for
    down, for use with lists.  The buttons use arrow icons and no text and are
    connected to the parent's ``onUpButtonClicked()`` and
    ``onDownButtonClicked()`` to handle their respective ``clicked()`` signals.

    ``parent``
        The parent object.  This should be a ``QWidget`` descendant.
    """
    up_button = QtGui.QPushButton(parent)
    up_button.setIcon(build_icon(u':/services/service_up.png'))
    up_button.setObjectName(u'upButton')
    up_button.setToolTip(
        translate('OpenLP.Ui', 'Move selection up one position.'))
    down_button = QtGui.QPushButton(parent)
    down_button.setIcon(build_icon(u':/services/service_down.png'))
    down_button.setObjectName(u'downButton')
    down_button.setToolTip(
        translate('OpenLP.Ui', 'Move selection down one position.'))
    QtCore.QObject.connect(up_button,
        QtCore.SIGNAL(u'clicked()'), parent.onUpButtonClicked)
    QtCore.QObject.connect(down_button,
        QtCore.SIGNAL(u'clicked()'), parent.onDownButtonClicked)
    return up_button, down_button

def base_action(parent, name):
    """
    Return the most basic action with the object name set.
    """
    action = QtGui.QAction(parent)
    action.setObjectName(name)
    return action

def checkable_action(parent, name, checked=None):
    """
    Return a standard action with the checkable attribute set.
    """
    action = base_action(parent, name)
    action.setCheckable(True)
    if checked is not None:
        action.setChecked(checked)
    return action

def icon_action(parent, name, icon, checked=None):
    """
    Return a standard action with an icon.
    """
    if checked is not None:
        action = checkable_action(parent, name, checked)
    else:
        action = base_action(parent, name)
    action.setIcon(build_icon(icon))
    return action

def shortcut_action(parent, text, shortcuts, function):
    """
    Return a shortcut enabled action.
    """
    action = QtGui.QAction(text, parent)
    action.setShortcuts(shortcuts)
    action.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)
    QtCore.QObject.connect(action, QtCore.SIGNAL(u'triggered()'), function)
    return action

def add_widget_completer(cache, widget):
    """
    Adds a text autocompleter to a widget.

    ``cache``
        The list of items to use as suggestions.

    ``widget``
        The object to use the completer.
    """
    completer = QtGui.QCompleter(cache)
    completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    widget.setCompleter(completer)

def create_valign_combo(form, parent, layout):
    """
    Creates a standard label and combo box for asking users to select a
    vertical alignment.

    ``form``
        The UI screen that the label and combo will appear on.

    ``parent``
        The parent object.  This should be a ``QWidget`` descendant.

    ``layout``
        A layout object to add the label and combo widgets to.
    """
    verticalLabel = QtGui.QLabel(parent)
    verticalLabel.setObjectName(u'VerticalLabel')
    verticalLabel.setText(translate('OpenLP.Ui', '&Vertical Align:'))
    form.verticalComboBox = QtGui.QComboBox(parent)
    form.verticalComboBox.setObjectName(u'VerticalComboBox')
    form.verticalComboBox.addItem(translate('OpenLP.Ui', 'Top'))
    form.verticalComboBox.addItem(translate('OpenLP.Ui', 'Middle'))
    form.verticalComboBox.addItem(translate('OpenLP.Ui', 'Bottom'))
    verticalLabel.setBuddy(form.verticalComboBox)
    layout.addRow(verticalLabel, form.verticalComboBox)
