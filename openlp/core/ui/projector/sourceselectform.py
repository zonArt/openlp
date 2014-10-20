# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Ken Roberts, Simon Scudder,               #
# Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon Tibble,             #
# Dave Warnock, Frode Woldsund, Martin Zibricky, Patrick Zimmermann           #
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
    :mod: `openlp.core.ui.projector.sourceselectform` module

    Provides the dialog window for selecting video source for projector.
"""
import logging
log = logging.getLogger(__name__)
log.debug('editform loaded')

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSize
from PyQt4.QtGui import QDialog, QButtonGroup, QDialogButtonBox, QGroupBox, QRadioButton, \
    QStyle, QStylePainter, QStyleOptionTab, QTabBar, QTabWidget, QVBoxLayout, QWidget

from openlp.core.common import translate, is_macosx
from openlp.core.lib import build_icon
from openlp.core.lib.projector.constants import PJLINK_DEFAULT_SOURCES


def source_group(inputs, source_text):
    """
    Return a dictionary where key is source[0] and values are inputs
    grouped by source[0].

    source_text = dict{"key1": "key1-text",
                       "key2": "key2-text",
                       ...}
    ex:
        dict{ key1[0]: { "key11": "key11-text",
                         "key12": "key12-text",
                         "key13": "key13-text",
                         ... }
              key2[0]: {"key21": "key21-text",
                        "key22": "key22-text",
                        ... }

    :param inputs: List of inputs
    :param source_text: Dictionary of {code: text} values to display
    :returns: dict
    """
    groupdict = {}
    keydict = {}
    checklist = inputs
    key = checklist[0][0]
    for item in checklist:
        if item[0] == key:
            groupdict[item] = source_text[item]
            continue
        else:
            keydict[key] = groupdict
            key = item[0]
            groupdict = {item: source_text[item]}
    keydict[key] = groupdict
    return keydict


def Build_Tab(group, source_key, default):
    """
    Create the radio button page for a tab.
    Dictionary will be a 1-key entry where key=tab to setup, val=list of inputs.

    source_key: {"groupkey1": {"key11": "key11-text",
                               "key12": "key12-text",
                               ...
                              },
                 "groupkey2": {"key21": "key21-text",
                               "key22": "key22-text",
                               ....
                              },
                 ...
                }

    :param group: Button group widget to add buttons to
    :param source_key: Dictionary of sources for radio buttons
    :param default: Default radio button to check
    """
    buttonchecked = False
    widget = QWidget()
    layout = QVBoxLayout()
    layout.setSpacing(10)
    widget.setLayout(layout)
    tempkey = list(source_key.keys())[0]  # Should only be 1 key
    sourcelist = list(source_key[tempkey])
    sourcelist.sort()
    button_count = len(sourcelist)
    for key in sourcelist:
        itemwidget = QRadioButton(source_key[tempkey][key])
        itemwidget.setAutoExclusive(True)
        if default == key:
            itemwidget.setChecked(True)
            buttonchecked = itemwidget.isChecked() or buttonchecked
        group.addButton(itemwidget, int(key))
        layout.addWidget(itemwidget)
    layout.addStretch()
    return (widget, button_count, buttonchecked)


class FingerTabBarWidget(QTabBar):
    """
    Realign west -orientation tabs to left-right text rather than south-north text
    Borrowed from
    http://www.kidstrythisathome.com/2013/03/fingertabs-horizontal-tabs-with-horizontal-text-in-pyqt/
    """
    def __init__(self, parent=None, *args, **kwargs):
        """
        Reset tab text orientation on initialization

        :param width: Remove default width parameter in kwargs
        :param height: Remove default height parameter in kwargs
        """
        self.tabSize = QSize(kwargs.pop('width', 100), kwargs.pop('height', 25))
        QTabBar.__init__(self, parent, *args, **kwargs)

    def paintEvent(self, event):
        """
        Repaint tab in left-right text orientation.

        :param event: Repaint event signal
        """
        painter = QStylePainter(self)
        option = QStyleOptionTab()

        for index in range(self.count()):
            self.initStyleOption(option, index)
            tabRect = self.tabRect(index)
            tabRect.moveLeft(10)
            painter.drawControl(QStyle.CE_TabBarTabShape, option)
            painter.drawText(tabRect, QtCore.Qt.AlignVCenter |
                             QtCore.Qt.TextDontClip,
                             self.tabText(index))
        painter.end()

    def tabSizeHint(self, index):
        """
        Return tabsize

        :param index: Tab index to fetch tabsize from
        :returns: instance tabSize
        """
        return self.tabSize


class FingerTabWidget(QTabWidget):
    """
    A QTabWidget equivalent which uses our FingerTabBarWidget

    Based on thread discussion
    http://www.riverbankcomputing.com/pipermail/pyqt/2005-December/011724.html
    """
    def __init__(self, parent, *args):
        """
        Initialize FingerTabWidget instance
        """
        QTabWidget.__init__(self, parent, *args)
        self.setTabBar(FingerTabBarWidget(self))


class SourceSelectTabs(QDialog):
    """
    Class for handling selecting the source for the projector to use.
    Uses tabbed interface.
    """
    def __init__(self, parent, projectordb):
        """
        Build the source select dialog using tabbed interface.

        :param projectordb: ProjectorDB session to use
        """
        log.debug('Initializing SourceSelectTabs()')
        self.projectordb = projectordb
        super(SourceSelectTabs, self).__init__(parent)
        self.setWindowTitle(translate('OpenLP.SourceSelectForm', 'Select Projector Source'))
        self.setObjectName('source_select_tabs')
        self.setWindowIcon(build_icon(':/icon/openlp-log-32x32.png'))
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setObjectName('source_select_tabs_layout')
        self.tabwidget = FingerTabWidget(self)
        self.tabwidget.setObjectName('source_select_tabs_tabwidget')
        self.tabwidget.setUsesScrollButtons(False)
        if is_macosx():
            self.tabwidget.setTabPosition(QTabWidget.North)
        else:
            self.tabwidget.setTabPosition(QTabWidget.West)
        self.layout.addWidget(self.tabwidget)
        self.setLayout(self.layout)

    def exec_(self, projector):
        """
        Override initial method so we can build the tabs.

        :param projector: Projector instance to build source list from
        """
        self.projector = projector
        self.source_text = self.projectordb.get_source_list(projector.manufacturer,
                                                            projector.model,
                                                            projector.source_available)
        self.source_group = source_group(projector.source_available, self.source_text)
        # self.source_group = {'4': {'41': 'Storage 1'}, '5': {"51": 'Network 1'}}
        self.button_group = QButtonGroup()
        keys = list(self.source_group.keys())
        keys.sort()
        for key in keys:
            (tab, button_count, buttonchecked) = Build_Tab(group=self.button_group,
                                                           source_key={key: self.source_group[key]},
                                                           default=self.projector.source)
            thistab = self.tabwidget.addTab(tab, PJLINK_DEFAULT_SOURCES[key])
            if buttonchecked:
                self.tabwidget.setCurrentIndex(thistab)
        self.button_box = QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                           QtGui.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept_me)
        self.button_box.rejected.connect(self.reject_me)
        self.layout.addWidget(self.button_box)
        selected = super(SourceSelectTabs, self).exec_()
        return selected

    @pyqtSlot()
    def accept_me(self):
        """
        Slot to accept 'OK' button
        """
        selected = self.button_group.checkedId()
        log.debug('SourceSelectTabs().accepted() Setting source to %s' % selected)
        self.done(selected)

    @pyqtSlot()
    def reject_me(self):
        """
        Slot to accept 'Cancel' button
        """
        log.debug('SourceSelectTabs() - Rejected')
        self.done(0)


class SourceSelectSingle(QDialog):
    """
    Class for handling selecting the source for the projector to use.
    Uses single dialog interface.
    """
    def __init__(self, parent, projectordb):
        """
        Build the source select dialog.

        :param projectordb: ProjectorDB session to use
        """
        log.debug('Initializing SourceSelectSingle()')
        self.projectordb = projectordb
        super(SourceSelectSingle, self).__init__(parent)
        self.setWindowTitle(translate('OpenLP.SourceSelectSingle', 'Select Projector Source'))
        self.setObjectName('source_select_single')
        self.setWindowIcon(build_icon(':/icon/openlp-log-32x32.png'))
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setObjectName('source_select_tabs_layout')
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        self.setMinimumWidth(350)
        self.button_group = QButtonGroup()
        self.button_group.setObjectName('source_select_single_buttongroup')

    def exec_(self, projector):
        """
        Override initial method so we can build the tabs.

        :param projector: Projector instance to build source list from
        """
        self.projector = projector
        self.source_text = self.projectordb.get_source_list(projector.manufacturer,
                                                            projector.model,
                                                            projector.source_available)
        keys = list(self.source_text.keys())
        keys.sort()
        key_count = len(keys)
        button_list = []
        for key in keys:
            button = QtGui.QRadioButton(self.source_text[key])
            button.setChecked(True if key == projector.source else False)
            self.layout.addWidget(button)
            self.button_group.addButton(button, int(key))
            button_list.append(key)
        self.button_box = QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                           QtGui.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept_me)
        self.button_box.rejected.connect(self.reject_me)
        self.layout.addWidget(self.button_box)
        self.setMinimumHeight(key_count*25)
        selected = super(SourceSelectSingle, self).exec_()
        return selected

        title = QtGui.QLabel(translate('OpenLP.SourceSelectSingle', 'Select the input source below'))
        self.layout.addWidget(title)
        self.radio_buttons = []
        source_list = self.projectordb.get_source_list(make=projector.link.manufacturer,
                                                       model=projector.link.model,
                                                       sources=projector.link.source_available)
        sort = []
        for item in source_list.keys():
            sort.append(item)
        sort.sort()
        current = QtGui.QLabel(translate('OpenLP.SourceSelectSingle', 'Current source is %s' %
                                         source_list[projector.link.source]))
        layout.addWidget(current)
        for item in sort:
            button = self._select_input_widget(parent=self,
                                               selected=projector.link.source,
                                               code=item,
                                               text=source_list[item])
            layout.addWidget(button)
        button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                            QtGui.QDialogButtonBox.Cancel)
        button_box.accepted.connect(box.accept_me)
        button_box.rejected.connect(box.reject_me)
        layout.addWidget(button_box)
        selected = super(SourceSelectSingle, self).exec_()
        return selected

    @pyqtSlot()
    def accept_me(self):
        """
        Slot to accept 'OK' button
        """
        selected = self.button_group.checkedId()
        log.debug('SourceSelectDialog().accepted() Setting source to %s' % selected)
        self.done(selected)

    @pyqtSlot()
    def reject_me(self):
        """
        Slot to accept 'Cancel' button
        """
        log.debug('SourceSelectDialog() - Rejected')
        self.done(0)
