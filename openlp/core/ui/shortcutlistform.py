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

import logging
import re

from PyQt4 import QtCore, QtGui

from openlp.core.utils import translate
from shortcutlistdialog import Ui_ShortcutListDialog, Ui_ShortcutDialog

REMOVE_AMPERSAND = re.compile(r'&{1}')

log = logging.getLogger(__name__)

class ShortcutListForm(QtGui.QDialog, Ui_ShortcutListDialog):
    """
    The shortcut list dialog
    """

    def __init__(self, parent):
        """
        Do some initialisation stuff
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.actionList = None
        self.captureShortcut = False
        self.currentItem = None
        self.newShortcut = None
        QtCore.QObject.connect(
            self.shortcutPushButton,
            QtCore.SIGNAL(u'toggled(bool)'),
            self.onShortcutPushButtonClicked
        )
        self.shortcutListTreeWidget.itemDoubleClicked.connect(self.shortcutEdit)

    def setNewShortcut(self, shortcut, alternate):
        if self.currentItem:
            self.actionList[self.currentItem].setShortcuts([shortcut, alternate])
            self.shortcutListTreeWidget.currentItem().setText(1, shortcut.toString())
            self.shortcutListTreeWidget.currentItem().setText(2, alternate.toString())

    def exec_(self, parent):
        self.actionList = parent.findChildren(QtGui.QAction)
        self.refreshActions()
        return QtGui.QDialog.exec_(self)

    def refreshActions(self):
        self.shortcutListTreeWidget.clear()
        catItemDict = dict()
        for num in range(len(self.actionList)):
            action = self.actionList[num]
            actionText = action.objectName() or action.parentWidget().objectName()
            shortcutText = u''
            shortcutAlternate = u''
            if len(action.shortcuts()) > 0:
                shortcutText = action.shortcuts()[0].toString()
                if len(action.shortcuts()) > 1:
                    shortcutAlternate = action.shortcuts()[1].toString()
            if action.isSeparator():
                continue
            if not shortcutText:
                continue
            categorie = action.data().toString() or 'Unknown'
            if not catItemDict.has_key(categorie):
                catItemDict[categorie] = QtGui.QTreeWidgetItem([categorie])
            actionItem = QtGui.QTreeWidgetItem([actionText, shortcutText, shortcutAlternate], num)
            actionItem.setIcon(0, action.icon())
            catItemDict[categorie].addChild(actionItem)
            catItemDict[categorie].setExpanded(True)
        for key in sorted(catItemDict.iterkeys()):
            self.shortcutListTreeWidget.addTopLevelItem(catItemDict[key])
            self.shortcutListTreeWidget.expandItem(catItemDict[key])
        self.shortcutListTreeWidget.sortItems(0, QtCore.Qt.AscendingOrder)

    def onShortcutPushButtonClicked(self, toggled):
        self.captureShortcut = toggled

    def shortcutEdit(self, item, column):
        self.currentItem = item.type()
        self.newShortcut = item.text(1)
        dialog = ShortcutDialog(self, u'Press new Shortcut', item.text(1), item.text(2))
        dialog.show()
        #self.shortcutListTreeWidget.currentItem().setText(column, u'Press new Shortcut')
        #self.captureShortcut = True
   
class ShortcutDialog(QtGui.QDialog, Ui_ShortcutDialog):
    """
    Class implementing a dialog for the configuration of a keyboard shortcut.
    
    """
    def __init__(self, parent = None, name = None, key=0, alternate=0):
        """
        Constructor
        
        @param parent The parent widget of this dialog. (QWidget)
        @param name The name of this dialog. (QString)
        @param modal Flag indicating a modal dialog. (boolean)
        """
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        if name:
            self.setObjectName(name)
        self.setupUi(self)
        self.setKeys(key, alternate)
        self.keyIndex = 0
        self.keys = [0, 0, 0, 0]
        self.noCheck = False
        self.objectType = None
        
        self.connect(self.primaryClearButton, QtCore.SIGNAL("clicked()"), self.__clear)
        self.connect(self.alternateClearButton, QtCore.SIGNAL("clicked()"), self.__clear)
        self.connect(self.primaryButton, QtCore.SIGNAL("clicked()"), self.__typeChanged)
        self.connect(self.alternateButton, QtCore.SIGNAL("clicked()"), self.__typeChanged)
        
        self.shortcutsGroup.installEventFilter(self)
        self.primaryButton.installEventFilter(self)
        self.alternateButton.installEventFilter(self)
        self.primaryClearButton.installEventFilter(self)
        self.alternateClearButton.installEventFilter(self)
        
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).installEventFilter(self)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).installEventFilter(self)

    def setKeys(self, key, alternateKey,  noCheck=None, objectType=None):
        """
        Public method to set the key to be configured.
        
        @param key key sequence to be changed (QKeySequence)
        @param alternateKey alternate key sequence to be changed (QKeySequence)
        @param noCheck flag indicating that no uniqueness check should
            be performed (boolean)
        @param objectType type of the object (string).
        """
        self.keyIndex = 0
        self.keys = [0, 0, 0, 0]
        self.keyLabel.setText(QtCore.QString(key))
        self.alternateKeyLabel.setText(QtCore.QString(alternateKey))
        self.primaryButton.setChecked(True)
        self.noCheck = noCheck
        self.objectType = objectType
        
    def on_buttonBox_accepted(self):
        """
        Private slot to handle the OK button press.
        """
        self.parent.setNewShortcut(QtGui.QKeySequence(self.keyLabel.text()),
                  QtGui.QKeySequence(self.alternateKeyLabel.text()))#, 
#                  self.noCheck, self.objectType)
        self.close()

    def __clear(self):
        """
        Private slot to handle the Clear button press.
        """
        self.keyIndex = 0
        self.keys = [0, 0, 0, 0]
        self.__setKeyLabelText("")
        
    def __typeChanged(self):
        """
        Private slot to handle the change of the shortcuts type.
        """
        self.keyIndex = 0
        self.keys = [0, 0, 0, 0]
        
    def __setKeyLabelText(self, txt):
        """
        Private method to set the text of a key label.
        
        @param txt text to be set (QString)
        """
        if self.primaryButton.isChecked():
            self.keyLabel.setText(txt)
        else:
            self.alternateKeyLabel.setText(txt)
        
    def eventFilter(self, watched, event):
        """
        Method called to filter the event queue.
        
        @param watched the QObject being watched
        @param event the event that occurred
        @return always False
        """
        if event.type() == QtCore.QEvent.KeyPress:
            self.keyPressEvent(event)
            return True
            
        return False
        
    def keyPressEvent(self, evt):
        """
        Private method to handle a key press event.
        
        @param evt the key event (QKeyEvent)
        """
        if evt.key() == QtCore.Qt.Key_Control:
            return
        if evt.key() == QtCore.Qt.Key_Meta:
            return
        if evt.key() == QtCore.Qt.Key_Shift:
            return
        if evt.key() == QtCore.Qt.Key_Alt:
            return
        if evt.key() == QtCore.Qt.Key_Menu:
            return
    
        if self.keyIndex == 4:
            self.keyIndex = 0
            self.keys = [0, 0, 0, 0]
    
        if evt.key() == QtCore.Qt.Key_Backtab and evt.modifiers() & QtCore.Qt.ShiftModifier:
            self.keys[self.keyIndex] = QtCore.Qt.Key_Tab
        else:
            self.keys[self.keyIndex] = evt.key()
        
        if evt.modifiers() & QtCore.Qt.ShiftModifier:
            self.keys[self.keyIndex] += QtCore.Qt.SHIFT
        if evt.modifiers() & QtCore.Qt.ControlModifier:
            self.keys[self.keyIndex] += QtCore.Qt.CTRL
        if evt.modifiers() & QtCore.Qt.AltModifier:
            self.keys[self.keyIndex] += QtCore.Qt.ALT
        if evt.modifiers() & QtCore.Qt.MetaModifier:
            self.keys[self.keyIndex] += QtCore.Qt.META
        
        self.keyIndex += 1
        
        if self.keyIndex == 1:
            self.__setKeyLabelText(QtCore.QString(QtGui.QKeySequence(self.keys[0])))
        elif self.keyIndex == 2:
            self.__setKeyLabelText(QtCore.QString(QtGui.QKeySequence(self.keys[0], self.keys[1])))
        elif self.keyIndex == 3:
            self.__setKeyLabelText(QtCore.QString(QtGui.QKeySequence(self.keys[0], self.keys[1],
                self.keys[2])))
        elif self.keyIndex == 4:
            self.__setKeyLabelText(QtCore.QString(QtGui.QKeySequence(self.keys[0], self.keys[1],
                self.keys[2], self.keys[3])))
