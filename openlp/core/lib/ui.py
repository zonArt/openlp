# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
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
    __instance__ = None

    def __new__(cls):
        """
        Override the default object creation method to return a single instance.
        """
        if not cls.__instance__:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self):
        """
        These strings should need a good reason to be retranslated elsewhere.
        Should some/more/less of these have an &amp; attached?
        """
        self.About = translate('OpenLP.Ui', 'About')
        self.Add = translate('OpenLP.Ui', '&Add')
        self.Advanced = translate('OpenLP.Ui', 'Advanced')
        self.AllFiles = translate('OpenLP.Ui', 'All Files')
        self.Bottom = translate('OpenLP.Ui', 'Bottom')
        self.Browse = translate('OpenLP.Ui', 'Browse...')
        self.Cancel = translate('OpenLP.Ui', 'Cancel')
        self.CCLINumberLabel = translate('OpenLP.Ui', 'CCLI number:')
        self.CreateService = translate('OpenLP.Ui', 'Create a new service.')
        self.ConfirmDelete = translate('OpenLP.Ui', 'Confirm Delete')
        self.Continuous = translate('OpenLP.Ui', 'Continuous')
        self.Default = unicode(translate('OpenLP.Ui', 'Default'))
        self.Delete = translate('OpenLP.Ui', '&Delete')
        self.DisplayStyle = translate('OpenLP.Ui', 'Display style:')
        self.Duplicate = translate('OpenLP.Ui', 'Duplicate Error')
        self.Edit = translate('OpenLP.Ui', '&Edit')
        self.EmptyField = translate('OpenLP.Ui', 'Empty Field')
        self.Error = translate('OpenLP.Ui', 'Error')
        self.Export = translate('OpenLP.Ui', 'Export')
        self.File = translate('OpenLP.Ui', 'File')
        self.FontSizePtUnit = translate('OpenLP.Ui', 'pt',
            'Abbreviated font pointsize unit')
        self.Help = translate('OpenLP.Ui', 'Help')
        self.Hours = translate('OpenLP.Ui', 'h',
            'The abbreviated unit for hours')
        self.Image = translate('OpenLP.Ui', 'Image')
        self.Import = translate('OpenLP.Ui', 'Import')
        self.LayoutStyle = translate('OpenLP.Ui', 'Layout style:')
        self.Live = translate('OpenLP.Ui', 'Live')
        self.LiveBGError = translate('OpenLP.Ui', 'Live Background Error')
        self.LiveToolbar = translate('OpenLP.Ui', 'Live Toolbar')
        self.Load = translate('OpenLP.Ui', 'Load')
        self.Minutes = translate('OpenLP.Ui', 'm',
            'The abbreviated unit for minutes')
        self.Middle = translate('OpenLP.Ui', 'Middle')
        self.New = translate('OpenLP.Ui', 'New')
        self.NewService = translate('OpenLP.Ui', 'New Service')
        self.NewTheme = translate('OpenLP.Ui', 'New Theme')
        self.NFSs = translate('OpenLP.Ui', 'No File Selected', 'Singular')
        self.NFSp = translate('OpenLP.Ui', 'No Files Selected', 'Plural')
        self.NISs = translate('OpenLP.Ui', 'No Item Selected', 'Singular')
        self.NISp = translate('OpenLP.Ui', 'No Items Selected', 'Plural')
        self.OLPV1 = translate('OpenLP.Ui', 'openlp.org 1.x')
        self.OLPV2 = translate('OpenLP.Ui', 'OpenLP 2.0')
        self.OpenLPStart = translate('OpenLP.Ui', 'OpenLP is already running. '
            'Do you wish to continue?')
        self.OpenService = translate('OpenLP.Ui', 'Open service.')
        self.PlaySlidesInLoop = translate('OpenLP.Ui','Play Slides in Loop')
        self.PlaySlidesToEnd = translate('OpenLP.Ui','Play Slides to End')
        self.Preview = translate('OpenLP.Ui', 'Preview')
        self.PrintService = translate('OpenLP.Ui', 'Print Service')
        self.ReplaceBG = translate('OpenLP.Ui', 'Replace Background')
        self.ReplaceLiveBG = translate('OpenLP.Ui', 'Replace live background.')
        self.ResetBG = translate('OpenLP.Ui', 'Reset Background')
        self.ResetLiveBG = translate('OpenLP.Ui', 'Reset live background.')
        self.Seconds = translate('OpenLP.Ui', 's',
            'The abbreviated unit for seconds')
        self.SaveAndPreview = translate('OpenLP.Ui', 'Save && Preview')
        self.Search = translate('OpenLP.Ui', 'Search')
        self.SelectDelete = translate('OpenLP.Ui', 'You must select an item '
            'to delete.')
        self.SelectEdit = translate('OpenLP.Ui', 'You must select an item to '
            'edit.')
        self.Settings = translate('OpenLP.Ui', 'Settings')
        self.SaveService = translate('OpenLP.Ui', 'Save Service')
        self.Service = translate('OpenLP.Ui', 'Service')
        self.Split = translate('OpenLP.Ui', '&Split')
        self.SplitToolTip = translate('OpenLP.Ui', 'Split a slide into two '
            'only if it does not fit on the screen as one slide.')
        self.StartTimeCode = unicode(translate('OpenLP.Ui', 'Start %s'))
        self.StopPlaySlidesInLoop = translate('OpenLP.Ui',
            'Stop Play Slides in Loop')
        self.StopPlaySlidesToEnd = translate('OpenLP.Ui',
            'Stop Play Slides to End')
        self.Theme = translate('OpenLP.Ui', 'Theme', 'Singular')
        self.Themes = translate('OpenLP.Ui', 'Themes', 'Plural')
        self.Tools = translate('OpenLP.Ui', 'Tools')
        self.Top = translate('OpenLP.Ui', 'Top')
        self.UnsupportedFile = translate('OpenLP.Ui', 'Unsupported File')
        self.VersePerSlide = translate('OpenLP.Ui', 'Verse Per Slide')
        self.VersePerLine = translate('OpenLP.Ui', 'Verse Per Line')
        self.Version = translate('OpenLP.Ui', 'Version')
        self.View = translate('OpenLP.Ui', 'View')
        self.ViewMode = translate('OpenLP.Ui', 'View Mode')

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
    button_box.setStandardButtons(
        accept_button | QtGui.QDialogButtonBox.Cancel)
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
        return QtGui.QMessageBox.critical(parent, UiStrings().Error, message,
            QtGui.QMessageBox.StandardButtons(
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No))
    data = {u'message': message}
    data[u'title'] = title if title else UiStrings().Error
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
    delete_button.setText(UiStrings().Delete)
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

def create_action(parent, name, **kwargs):
    """
    Return an action with the object name set and the given parameters.

    ``parent``
        A QtCore.QObject for the actions parent (required).

    ``name``
        A string which is set as object name (required).

    ``text``
        A string for the action text.

    ``icon``
        Either a QIcon, a resource string, or a file location string for the
        action icon.

    ``tooltip``
        A string for the action tool tip.

    ``statustip``
        A string for the action status tip.

    ``checked``
        A bool for the state. If ``None`` the Action is not checkable.

    ``enabled``
        False in case the action should be disabled.

    ``visible``
        False in case the action should be hidden.

    ``shortcuts``
        A QList<QKeySequence> (or a list of strings) which are set as shortcuts.

    ``context``
        A context for the shortcut execution (only will be set together with
        ``shortcuts``).

    ``category``
        A category the action should be listed in the shortcut dialog.

    ``triggers``
        A slot which is connected to the actions ``triggered()`` slot.
    """
    action = QtGui.QAction(parent)
    action.setObjectName(name)
    if kwargs.get(u'text'):
        action.setText(kwargs[u'text'])
    if kwargs.get(u'icon'):
        action.setIcon(build_icon(kwargs[u'icon']))
    if kwargs.get('tooltip'):
        action.setToolTip(kwargs['tooltip'])
    if kwargs.get('statustip'):
        action.setStatusTip(kwargs['statustip'])
    if kwargs.get('checked') is not None:
        action.setCheckable(True)
        action.setChecked(kwargs['checked'])
    if not kwargs.get('enabled'):
        action.setEnabled(False)
    if not kwargs.get('visible'):
        action.setVisible(False)
    if kwargs.get('shortcuts'):
        action.setShortcuts(kwargs['shortcuts'])
        action.setShortcutContext(kwargs.get('context',
            QtCore.Qt.WindowShortcut))
    if kwargs.get('category'):
        action_list = ActionList.get_instance()
        action_list.add_action(action, kwargs['category'])
    if kwargs.get('triggers'):
        QtCore.QObject.connect(action, QtCore.SIGNAL(u'triggered(bool)'),
            kwargs['triggers'])
    return action

def base_action(parent, name, category=None, **kwargs):
    return create_action(parent, name, category=None, **kwargs)

def checkable_action(parent, name, checked=None, category=None, **kwargs):
    return create_action(parent, name, checked=bool(checked), category=category,
        **kwargs)

def icon_action(parent, name, icon, checked=None, category=None, **kwargs):
    return create_action(parent, name, icon=icon, checked=checked,
        category=category, **kwargs)

def shortcut_action(parent, name, shortcuts, function, icon=None, checked=None,
    category=None, context=QtCore.Qt.WindowShortcut, **kwargs):
    return create_action(parent, name, icon=icon, checked=checked,
        shortcuts=shortcuts, context=context, category=category,
        triggers=function, **kwargs)

def context_menu_action(base, icon, text, slot, shortcuts=None, category=None,
    context=QtCore.Qt.WidgetShortcut, **kwargs):
    return create_action(parent=base, name=u'', icon=icon, text=text,
        triggers=slot, shortcuts=shortcuts, category=category, context=context,
        **kwargs)

def context_menu(base, icon, text):
    """
    Utility method to help build context menus.

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
    base.addAction(action)
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
    form.verticalComboBox.addItem(UiStrings().Top)
    form.verticalComboBox.addItem(UiStrings().Middle)
    form.verticalComboBox.addItem(UiStrings().Bottom)
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
