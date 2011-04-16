# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
from openlp.core.utils.actions import ActionList

log = logging.getLogger(__name__)

class UiStrings(object):
    """
    Provide standard strings for objects to use.
    """
    # These strings should need a good reason to be retranslated elsewhere.
    # Should some/more/less of these have an &amp; attached?
    About = translate('OpenLP.Ui', 'About')
    Add = translate('OpenLP.Ui', '&Add')
    Advanced = translate('OpenLP.Ui', 'Advanced')
    AllFiles = translate('OpenLP.Ui', 'All Files')
    Bottom = translate('OpenLP.Ui', 'Bottom')
    Browse = translate('OpenLP.Ui', 'Browse...')
    Cancel = translate('OpenLP.Ui', 'Cancel')
    CCLINumberLabel = translate('OpenLP.Ui', 'CCLI number:')
    CreateService = translate('OpenLP.Ui', 'Create a new service.')
    Continuous = translate('OpenLP.Ui', 'Continuous')
    Default = unicode(translate('OpenLP.Ui', 'Default'))
    Delete = translate('OpenLP.Ui', '&Delete')
    DisplayStyle = translate('OpenLP.Ui', 'Display style:')
    Edit = translate('OpenLP.Ui', '&Edit')
    EmptyField = translate('OpenLP.Ui', 'Empty Field')
    Error = translate('OpenLP.Ui', 'Error')
    Export = translate('OpenLP.Ui', 'Export')
    File = translate('OpenLP.Ui', 'File')
    FontSizePtUnit = translate('OpenLP.Ui', 'pt',
        'Abbreviated font pointsize unit')
    Help = translate('OpenLP.Ui', 'Help')
    Hours = translate('OpenLP.Ui', 'h', 'The abbreviated unit for hours')
    Image = translate('OpenLP.Ui', 'Image')
    Import = translate('OpenLP.Ui', 'Import')
    LayoutStyle = translate('OpenLP.Ui', 'Layout style:')
    LengthTime = unicode(translate('OpenLP.Ui', 'Length %s'))
    Live = translate('OpenLP.Ui', 'Live')
    LiveBGError = translate('OpenLP.Ui', 'Live Background Error')
    LivePanel = translate('OpenLP.Ui', 'Live Panel')
    LiveToolbar = translate('OpenLP.Ui', 'Live Toolbar')
    Load = translate('OpenLP.Ui', 'Load')
    Minutes = translate('OpenLP.Ui', 'm', 'The abbreviated unit for minutes')
    Middle = translate('OpenLP.Ui', 'Middle')
    New = translate('OpenLP.Ui', 'New')
    NewService = translate('OpenLP.Ui', 'New Service')
    NewTheme = translate('OpenLP.Ui', 'New Theme')
    NFSs = translate('OpenLP.Ui', 'No File Selected', 'Singular')
    NFSp = translate('OpenLP.Ui', 'No Files Selected', 'Plural')
    NISs = translate('OpenLP.Ui', 'No Item Selected', 'Singular')
    NISp = translate('OpenLP.Ui', 'No Items Selected', 'Plural')
    OLPV1 = translate('OpenLP.Ui', 'openlp.org 1.x')
    OLPV2 = translate('OpenLP.Ui', 'OpenLP 2.0')
    OpenLPStart = translate('OpenLP.Ui', 'OpenLP is already running. Do you '
        'wish to continue?')
    OpenService = translate('OpenLP.Ui', 'Open Service')
    Preview = translate('OpenLP.Ui', 'Preview')
    PreviewPanel = translate('OpenLP.Ui', 'Preview Panel')
    PrintServiceOrder = translate('OpenLP.Ui', 'Print Service Order')
    ReplaceBG = translate('OpenLP.Ui', 'Replace Background')
    ReplaceLiveBG = translate('OpenLP.Ui', 'Replace Live Background')
    ResetBG = translate('OpenLP.Ui', 'Reset Background')
    ResetLiveBG = translate('OpenLP.Ui', 'Reset Live Background')
    Seconds = translate('OpenLP.Ui', 's', 'The abbreviated unit for seconds')
    SaveAndPreview = translate('OpenLP.Ui', 'Save && Preview')
    Search = translate('OpenLP.Ui', 'Search')
    SelectDelete = translate('OpenLP.Ui', 'You must select an item to delete.')
    SelectEdit = translate('OpenLP.Ui', 'You must select an item to edit.')
    Settings = translate('OpenLP.Ui', 'Settings')
    SaveService = translate('OpenLP.Ui', 'Save Service')
    Service = translate('OpenLP.Ui', 'Service')
    StartTimeCode = unicode(translate('OpenLP.Ui', 'Start %s'))
    Theme = translate('OpenLP.Ui', 'Theme', 'Singular')
    Themes = translate('OpenLP.Ui', 'Themes', 'Plural')
    Tools = translate('OpenLP.Ui', 'Tools')
    Top = translate('OpenLP.Ui', 'Top')
    VersePerSlide = translate('OpenLP.Ui', 'Verse Per Slide')
    VersePerLine = translate('OpenLP.Ui', 'Verse Per Line')
    Version = translate('OpenLP.Ui', 'Version')
    View = translate('OpenLP.Ui', 'View')
    ViewMode = translate('OpenLP.Ui', 'View Model')

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
        The parent object. This should be a ``QWidget`` descendant.

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
    Creates a standard push button with a delete label and optional icon. The
    button is connected to the parent's ``onDeleteButtonClicked()`` method to
    handle the ``clicked()`` signal.

    ``parent``
        The parent object. This should be a ``QWidget`` descendant.

    ``icon``
        An icon to display on the button. This can be either a ``QIcon``, a
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
    down, for use with lists. The buttons use arrow icons and no text and are
    connected to the parent's ``onUpButtonClicked()`` and
    ``onDownButtonClicked()`` to handle their respective ``clicked()`` signals.

    ``parent``
        The parent object. This should be a ``QWidget`` descendant.
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

def base_action(parent, name, category=None):
    """
    Return the most basic action with the object name set.

    ``category``
        The category the action should be listed in the shortcut dialog. If you
        not wish, that this action is added to the shortcut dialog, then do not
        state any.
    """
    action = QtGui.QAction(parent)
    action.setObjectName(name)
    if category is not None:
        action_list = ActionList.get_instance()
        action_list.add_action(action, category)
    return action

def checkable_action(parent, name, checked=None, category=None):
    """
    Return a standard action with the checkable attribute set.
    """
    action = base_action(parent, name, category)
    action.setCheckable(True)
    if checked is not None:
        action.setChecked(checked)
    return action

def icon_action(parent, name, icon, checked=None, category=None):
    """
    Return a standard action with an icon.
    """
    if checked is not None:
        action = checkable_action(parent, name, checked, category)
    else:
        action = base_action(parent, name, category)
    action.setIcon(build_icon(icon))
    return action

def shortcut_action(parent, name, shortcuts, function, icon=None, checked=None,
    category=None, context=QtCore.Qt.WindowShortcut):
    """
    Return a shortcut enabled action.
    """
    action = QtGui.QAction(parent)
    action.setObjectName(name)
    if icon is not None:
        action.setIcon(build_icon(icon))
    if checked is not None:
        action.setCheckable(True)
        action.setChecked(checked)
    action.setShortcuts(shortcuts)
    action.setShortcutContext(context)
    action_list = ActionList.get_instance()
    action_list.add_action(action, category)
    QtCore.QObject.connect(action, QtCore.SIGNAL(u'triggered()'), function)
    return action

def context_menu_action(base, icon, text, slot, shortcuts=None, category=None,
    context=QtCore.Qt.WindowShortcut):
    """
    Utility method to help build context menus for plugins

    ``base``
        The parent menu to add this menu item to

    ``icon``
        An icon for this action

    ``text``
        The text to display for this action

    ``slot``
        The code to run when this action is triggered

    ``shortcuts``
        The action's shortcuts.

    ``category``
        The category the shortcut should be listed in the shortcut dialog. If
        left to None, then the action will be hidden in the shortcut dialog.

    ``context``
        The context the shortcut is valid.
    """
    action = QtGui.QAction(text, base)
    if icon:
        action.setIcon(build_icon(icon))
    QtCore.QObject.connect(action, QtCore.SIGNAL(u'triggered()'), slot)
    if shortcuts is not None:
        action.setShortcuts(shortcuts)
        action.setShortcutContext(context)
        action_list = ActionList.get_instance()
        action_list.add_action(action)
    return action

def context_menu(base, icon, text):
    """
    Utility method to help build context menus for plugins

    ``base``
        The parent object to add this menu to

    ``icon``
        An icon for this menu

    ``text``
        The text to display for this menu
    """
    action = QtGui.QMenu(text, base)
    action.setIcon(build_icon(icon))
    return action

def context_menu_separator(base):
    """
    Add a separator to a context menu

    ``base``
        The menu object to add the separator to
    """
    action = QtGui.QAction(u'', base)
    action.setSeparator(True)
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
        The parent object. This should be a ``QWidget`` descendant.

    ``layout``
        A layout object to add the label and combo widgets to.
    """
    verticalLabel = QtGui.QLabel(parent)
    verticalLabel.setObjectName(u'VerticalLabel')
    verticalLabel.setText(translate('OpenLP.Ui', '&Vertical Align:'))
    form.verticalComboBox = QtGui.QComboBox(parent)
    form.verticalComboBox.setObjectName(u'VerticalComboBox')
    form.verticalComboBox.addItem(UiStrings.Top)
    form.verticalComboBox.addItem(UiStrings.Middle)
    form.verticalComboBox.addItem(UiStrings.Bottom)
    verticalLabel.setBuddy(form.verticalComboBox)
    layout.addRow(verticalLabel, form.verticalComboBox)

def find_and_set_in_combo_box(combo_box, value_to_find):
    """
    Find a string in a combo box and set it as the selected item if present

    ``combo_box``
        The combo box to check for selected items

    ``value_to_find``
        The value to find
    """
    index = combo_box.findText(value_to_find,
        QtCore.Qt.MatchExactly)
    if index == -1:
        # Not Found.
        index = 0
    combo_box.setCurrentIndex(index)
