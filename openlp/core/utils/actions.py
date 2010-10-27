# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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
The :mod:`~openlp.core.utils.actions` module provides action list classes used
by the shortcuts system.
"""

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

    def __iter__(self):
        return self

    def __next__(self):
        """
        Python 3 "next" method.
        """
        if self.index >= len(self.actions):
            raise StopIteration
        else:
            self.index += 1
            return self.actions[self.index - 1][1]

    def next(self):
        """
        Python 2 "next" method.
        """
        return self.__next__()

    def add(self, action, weight=0):
        self.actions.append((weight, action))
        self.actions.sort(key=lambda act: act[0])


class CategoryList(object):
    """
    The :class:`~openlp.core.utils.ActionListCategory` class encapsulates a
    category list for the :class:`~openlp.core.utils.ActionList` class and
    provides an iterator interface for walking through the list of actions in
    this category.
    """

    def __init__(self):
        self.index = 0
        self.categories = CategoryActionList()

    def __iter__(self):
        return self

    def __next__(self):
        """
        Python 3 "next" method for iterator.
        """
        if self.index >= len(self.categories):
            raise StopIteration
        else:
            self.index += 1
            return self.categories[self.index - 1]

    def next(self):
        """
        Python 2 "next" method for iterator.
        """
        return self.__next__()

    def add(self, name, weight=0):
        self.categories.append(ActionCategory(name, weight))
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

    def add_category(self, category, weight=0):
        """
        Add a category to the action list, ordered by ``weight``.

        ``category``
            The name of the category.

        ``weight``
            **Defaults to 0.** The weight of the category. The weight
            determines the sort order, with negative items appearing
            higher than positive items.
        """
        self.categories.add(category, weight)

    def has_category(self, category):
        for cat in self.categories:
            if cat[u'name'] == category:
                return True
        return False

    def add_action(self, action, category=u'Default', weight=0):
        if not self.has_category:
            self.add_category(category)
        for index, cat in enumerate(self.categories):
            if cat[u'name'] == category:
                self.categories[index][u'actions'].append((weight, action))
                return

