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
The :mod:`~openlp.core.utils.actions` module provides action list classes used
by the shortcuts system.
"""
from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate

class ActionCategory(object):
    """
    The :class:`~openlp.core.utils.ActionCategory` class encapsulates a
    category for the :class:`~openlp.core.utils.CategoryList` class.
    """
    def __init__(self, name, weight=0):
        self.name = name
        self.weight = weight
        self.actions = CategoryActionList()


class CategoryActionList(object):
    """
    The :class:`~openlp.core.utils.CategoryActionList` class provides a sorted
    list of actions within a category.
    """
    def __init__(self):
        self.index = 0
        self.actions = []

    def __getitem__(self, key):
        for weight, action in self.actions:
            if action.text() == key:
                return action
        raise KeyError(u'Action "%s" does not exist.' % key)

    def __contains__(self, item):
        return self.has_key(item)

    def __len__(self):
        return len(self.actions)

    def __iter__(self):
        return self

    def __next__(self):
        """
        Python 3 "next" method.
        """
        if self.index >= len(self.actions):
            self.index = 0
            raise StopIteration
        else:
            self.index += 1
            return self.actions[self.index - 1][1]

    def next(self):
        """
        Python 2 "next" method.
        """
        return self.__next__()

    def has_key(self, key):
        for weight, action in self.actions:
            if action.text() == key:
                return True
        return False

    def append(self, name):
        weight = 0
        if len(self.actions) > 0:
            weight = self.actions[-1][0] + 1
        self.add(name, weight)

    def add(self, action, weight=0):
        self.actions.append((weight, action))
        self.actions.sort(key=lambda act: act[0])

    def remove(self, remove_action):
        for action in self.actions:
            if action[1] == remove_action:
                self.actions.remove(action)
                return


class CategoryList(object):
    """
    The :class:`~openlp.core.utils.CategoryList` class encapsulates a category
    list for the :class:`~openlp.core.utils.ActionList` class and provides an
    iterator interface for walking through the list of actions in this category.
    """

    def __init__(self):
        self.index = 0
        self.categories = []

    def __getitem__(self, key):
        for category in self.categories:
            if category.name == key:
                return category
        raise KeyError(u'Category "%s" does not exist.' % key)

    def __contains__(self, item):
        return self.has_key(item)

    def __len__(self):
        return len(self.categories)

    def __iter__(self):
        return self

    def __next__(self):
        """
        Python 3 "next" method for iterator.
        """
        if self.index >= len(self.categories):
            self.index = 0
            raise StopIteration
        else:
            self.index += 1
            return self.categories[self.index - 1]

    def next(self):
        """
        Python 2 "next" method for iterator.
        """
        return self.__next__()

    def has_key(self, key):
        for category in self.categories:
            if category.name == key:
                return True
        return False

    def append(self, name, actions=None):
        weight = 0
        if len(self.categories) > 0:
            weight = self.categories[-1].weight + 1
        if actions:
            self.add(name, weight, actions)
        else:
            self.add(name, weight)

    def add(self, name, weight=0, actions=None):
        category = ActionCategory(name, weight)
        if actions:
            for action in actions:
                if isinstance(action, tuple):
                    category.actions.add(action[0], action[1])
                else:
                    category.actions.append(action)
        self.categories.append(category)
        self.categories.sort(key=lambda cat: cat.weight)


class ActionList(object):
    """
    The :class:`~openlp.core.utils.ActionList` class contains a list of menu
    actions and categories associated with those actions. Each category also
    has a weight by which it is sorted when iterating through the list of
    actions or categories.
    """
    def __init__(self):
        self.categories = CategoryList()

    def add_action(self, action, category, weight=None):
        if category not in self.categories:
            self.categories.append(category)
        action.defaultShortcuts = action.shortcuts()
        if weight is None:
            self.categories[category].actions.append(action)
        else:
            self.categories[category].actions.add(action, weight)
        # Load the shortcut from the config.
        settings = QtCore.QSettings()
        settings.beginGroup(u'shortcuts')
        shortcuts = settings.value(action.objectName(),
            QtCore.QVariant(action.shortcuts())).toStringList()
        action.setShortcuts(
            [QtGui.QKeySequence(shortcut) for shortcut in shortcuts])
        settings.endGroup()

    def remove_action(self, action, category):
        if category not in self.categories:
            return
        self.categories[category].actions.remove(action)

actionList = ActionList()
