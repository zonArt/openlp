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
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QDialog, QButtonGroup, QDialogButtonBox, QGroupBox, QRadioButton, \
    QTabBar, QTabWidget, QVBoxLayout, QWidget

from openlp.core.common import translate
from openlp.core.lib import build_icon
from openlp.core.lib.projector.constants import PJLINK_DEFAULT_SOURCES


def source_group(inputs, source_text):
    """
    Return a dictionary where key is source[0] and values are inputs
    grouped by source[0].
    ex:
        dict{"1": "11 12 13 14 15",
             "2": "21 22 23 24 25",
             ... }

    :param inputs: List of inputs
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

    source_key: { group: { code: string,
                           code: string,
                           ...
                         }
                }

    :param group: Button group widget to add buttons to
    :param source_key: Dictionary of sources for radio buttons
    :param default: Default radio button to check
    """
    widget = QWidget()
    layout = QVBoxLayout()
    layout.setSpacing(10)
    widget.setLayout(layout)
    tempkey = list(source_key.keys())[0]  # Should only be 1 key
    sourcelist = list(source_key[tempkey])
    sourcelist.sort()
    for key in sourcelist:
        itemwidget = QRadioButton(source_key[tempkey][key])
        itemwidget.setAutoExclusive(True)
        if default == key:
            itemwidget.setChecked(True)
        group.addButton(itemwidget, int(key))
        layout.addWidget(itemwidget)
    layout.addStretch()
    return widget


class SourceSelectDialog(QDialog):
    """
    Class for handling selecting the source for the projector to use.
    """
    def __init__(self, parent, projectordb):
        """
        Build the source select dialog.

        :param projectordb: ProjectorDB session to use
        """
        log.debug('Initializing SourceSelectDialog()')
        self.projectordb = projectordb
        super(SourceSelectDialog, self).__init__(parent)
        self.setWindowTitle(translate('OpenLP.SourceSelectDialog', 'Select Projector Source'))
        self.setObjectName('source_select_dialog')
        self.setWindowIcon(build_icon(':/icon/openlp-log-32x32.png'))
        self.setMinimumWidth(300)
        self.setMinimumHeight(400)
        self.setModal(True)

        self.layout = QVBoxLayout()
        self.layout.setObjectName('source_select_dialog_layout')
        self.tabwidget = QTabWidget(self)
        self.tabwidget.setObjectName('source_select_dialog_tabwidget')
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
        self.button_group = QButtonGroup()
        keys = list(self.source_group.keys())
        keys.sort()
        for key in keys:
            self.tabwidget.addTab(Build_Tab(group=self.button_group,
                                            source_key={key: self.source_group[key]},
                                            default=self.projector.source), PJLINK_DEFAULT_SOURCES[key])
        button_box = QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                      QtGui.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accepted)
        button_box.rejected.connect(self.rejected)
        self.layout.addWidget(button_box)
        selected = super(SourceSelectDialog, self).exec_()

        def accepted(self):
            self.accept()
            return projector.set_input_source(self.button_group.checkedId())

        def rejected(self):
            self.reject()
            return 0