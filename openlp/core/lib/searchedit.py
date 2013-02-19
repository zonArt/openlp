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

import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import build_icon
from openlp.core.lib.ui import create_widget_action

log = logging.getLogger(__name__)


class SearchEdit(QtGui.QLineEdit):
    """
    This is a specialised QLineEdit with a "clear" button inside for searches.
    """

    def __init__(self, parent):
        """
        Constructor.
        """
        QtGui.QLineEdit.__init__(self, parent)
        self._currentSearchType = -1
        self.clearButton = QtGui.QToolButton(self)
        self.clearButton.setIcon(build_icon(u':/system/clear_shortcut.png'))
        self.clearButton.setCursor(QtCore.Qt.ArrowCursor)
        self.clearButton.setStyleSheet(
            u'QToolButton { border: none; padding: 0px; }')
        self.clearButton.resize(18, 18)
        self.clearButton.hide()
        QtCore.QObject.connect(self.clearButton, QtCore.SIGNAL(u'clicked()'), self._onClearButtonClicked)
        QtCore.QObject.connect(self, QtCore.SIGNAL(u'textChanged(const QString&)'), self._onSearchEditTextChanged)
        self._updateStyleSheet()
        self.setAcceptDrops(False)

    def _updateStyleSheet(self):
        """
        Internal method to update the stylesheet depending on which widgets are
        available and visible.
        """
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        rightPadding = self.clearButton.width() + frameWidth
        if hasattr(self, u'menuButton'):
            leftPadding = self.menuButton.width()
            self.setStyleSheet(u'QLineEdit { padding-left: %spx; padding-right: %spx; } ' % (leftPadding, rightPadding))
        else:
            self.setStyleSheet(u'QLineEdit { padding-right: %spx; } ' % rightPadding)
        msz = self.minimumSizeHint()
        self.setMinimumSize(max(msz.width(), self.clearButton.width() + (frameWidth * 2) + 2),
            max(msz.height(), self.clearButton.height() + (frameWidth * 2) + 2))

    def resizeEvent(self, event):
        """
        Reimplemented method to react to resizing of the widget.

        ``event``
            The event that happened.
        """
        size = self.clearButton.size()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.clearButton.move(self.rect().right() - frameWidth - size.width(),
            (self.rect().bottom() + 1 - size.height()) / 2)
        if hasattr(self, u'menuButton'):
            size = self.menuButton.size()
            self.menuButton.move(self.rect().left() + frameWidth + 2, (self.rect().bottom() + 1 - size.height()) / 2)

    def currentSearchType(self):
        """
        Readonly property to return the current search type.
        """
        return self._currentSearchType

    def setCurrentSearchType(self, identifier):
        """
        Set a new current search type.

        ``identifier``
            The search type identifier (int).
        """
        menu = self.menuButton.menu()
        for action in menu.actions():
            if identifier == action.data():
                # setPlaceholderText has been implemented in Qt 4.7 and in at
                # least PyQt 4.9 (I am not sure, if it was implemented in
                # PyQt 4.8).
                try:
                    self.setPlaceholderText(action.placeholderText)
                except AttributeError:
                    pass
                self.menuButton.setDefaultAction(action)
                self._currentSearchType = identifier
                self.emit(QtCore.SIGNAL(u'searchTypeChanged(int)'), identifier)
                return True

    def setSearchTypes(self, items):
        """
        A list of tuples to be used in the search type menu. The first item in
        the list will be preselected as the default.

        ``items``
            The list of tuples to use. The tuples should contain an integer
            identifier, an icon (QIcon instance or string) and a title for the
            item in the menu. In short, they should look like this::

                (<identifier>, <icon>, <title>, <place holder text>)

            For instance::

                (1, <QIcon instance>, "Titles", "Search Song Titles...")

            Or::

                (2, ":/songs/authors.png", "Authors", "Search Authors...")
        """
        menu = QtGui.QMenu(self)
        first = None
        for identifier, icon, title, placeholder in items:
            action = create_widget_action(menu, text=title, icon=icon,
                data=identifier, triggers=self._onMenuActionTriggered)
            action.placeholderText = placeholder
            if first is None:
                first = action
                self._currentSearchType = identifier
        if not hasattr(self, u'menuButton'):
            self.menuButton = QtGui.QToolButton(self)
            self.menuButton.setIcon(build_icon(u':/system/clear_shortcut.png'))
            self.menuButton.setCursor(QtCore.Qt.ArrowCursor)
            self.menuButton.setPopupMode(QtGui.QToolButton.InstantPopup)
            self.menuButton.setStyleSheet(
                u'QToolButton { border: none; padding: 0px 10px 0px 0px; }')
            self.menuButton.resize(QtCore.QSize(28, 18))
        self.menuButton.setMenu(menu)
        self.menuButton.setDefaultAction(first)
        self.menuButton.show()
        self._updateStyleSheet()

    def _onSearchEditTextChanged(self, text):
        """
        Internally implemented slot to react to when the text in the line edit
        has changed so that we can show or hide the clear button.

        ``text``
            A :class:`~PyQt4.QtCore.QString` instance which represents the text
            in the line edit.
        """
        self.clearButton.setVisible(bool(text))

    def _onClearButtonClicked(self):
        """
        Internally implemented slot to react to the clear button being clicked
        to clear the line edit. Once it has cleared the line edit, it emits the
        ``cleared()`` signal so that an application can react to the clearing
        of the line edit.
        """
        self.clear()
        self.emit(QtCore.SIGNAL(u'cleared()'))

    def _onMenuActionTriggered(self):
        """
        Internally implemented slot to react to the select of one of the search
        types in the menu. Once it has set the correct action on the button,
        and set the current search type (using the list of identifiers provided
        by the developer), the ``searchTypeChanged(int)`` signal is emitted
        with the identifier.
        """
        sender = self.sender()
        for action in self.menuButton.menu().actions():
            action.setChecked(False)
        self.menuButton.setDefaultAction(sender)
        self._currentSearchType = sender.data()
        # setPlaceholderText has been implemented in Qt 4.7 and in at least
        # PyQt 4.9 (I am not sure, if it was implemented in PyQt 4.8).
        try:
            self.setPlaceholderText(self.menuButton.defaultAction().placeholderText)
        except AttributeError:
            pass
        self.emit(QtCore.SIGNAL(u'searchTypeChanged(int)'), self._currentSearchType)
