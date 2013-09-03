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
Extend QTreeWidget to handle drag and drop functionality
"""
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Registry


class TreeWidgetWithDnD(QtGui.QTreeWidget):
    """
    Provide a tree widget to store objects and handle drag and drop events
    """
    def __init__(self, parent=None, name=''):
        """
        Initialise the tree widget
        """
        super(TreeWidgetWithDnD, self).__init__(parent)
        self.mimeDataText = name
        self.allow_internal_dnd = False
        self.header().close()
        self.default_indentation = self.indentation()
        self.setIndentation(0)
        self.setAnimated(True)
        assert(self.mimeDataText)

    def activateDnD(self):
        """
        Activate DnD of widget
        """
        self.setAcceptDrops(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        Registry().register_function(('%s_dnd' % self.mimeDataText), self.parent().load_file)
        Registry().register_function(('%s_dnd_internal' % self.mimeDataText), self.parent().dnd_move_internal)

    def mouseMoveEvent(self, event):
        """
        Drag and drop event does not care what data is selected as the recipient will use events to request the data
        move just tell it what plugin to call

        ``event``
            The event that occurred
        """
        if event.buttons() != QtCore.Qt.LeftButton:
            event.ignore()
            return
        if not self.selectedItems():
            event.ignore()
            return
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        drag.setMimeData(mimeData)
        mimeData.setText(self.mimeDataText)
        drag.start(QtCore.Qt.CopyAction)

    def dragEnterEvent(self, event):
        """
        Receive drag enter event, check if it is a file or internal object and allow it if it is.

        ``event``
            The event that occurred
        """
        if event.mimeData().hasUrls():
            event.accept()
        elif self.allow_internal_dnd:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """
        Receive drag move event, check if it is a file or internal object and allow it if it is.

        ``event``
            The event that occurred
        """
        QtGui.QTreeWidget.dragMoveEvent(self, event)
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        elif self.allow_internal_dnd:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Receive drop event, check if it is a file or internal object and process it if it is.

        ``event``
            Handle of the event pint passed
        """
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            files = []
            for url in event.mimeData().urls():
                local_file = url.toLocalFile()
                if os.path.isfile(local_file):
                    files.append(local_file)
                elif os.path.isdir(local_file):
                    listing = os.listdir(local_file)
                    for file_name in listing:
                        files.append(os.path.join(local_file, file_name))
            Registry().execute('%s_dnd' % self.mimeDataText, {'files': files, 'target': self.itemAt(event.pos())})
        elif self.allow_internal_dnd:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            Registry().execute('%s_dnd_internal' % self.mimeDataText, self.itemAt(event.pos()))
        else:
            event.ignore()

    # Convenience methods for emulating a QListWidget. This helps keeping MediaManagerItem simple.
    def addItem(self, item):
        self.addTopLevelItem(item)

    def count(self):
        return self.topLevelItemCount()

    def item(self, index):
        return self.topLevelItem(index)
