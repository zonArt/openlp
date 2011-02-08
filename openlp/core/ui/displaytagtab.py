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
The :mod:`DisplayTagTab` provides an Tag Edit facility.  The Base set are
protected and included each time loaded.  Custom tags can be defined and saved.
The Custom Tag arrays are saved in a pickle so QSettings works on them.  Base
Tags cannot be changed.
"""
import cPickle

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab, translate, DisplayTags
from openlp.core.lib.ui import critical_error_message_box

class DisplayTagTab(SettingsTab):
    """
    The :class:`DisplayTagTab` manages the settings tab .
    """
    def __init__(self):
        """
        Initialise the settings tab
        """
        SettingsTab.__init__(self, u'Display Tags')

    def resizeEvent(self, event=None):
        pass

    def preLoad(self):
        """
        Initialise values before the Load takes place
        """
        # Create initial copy from master
        DisplayTags.reset_html_tags()
        user_expands = QtCore.QSettings().value(u'displayTags/html_tags',
            QtCore.QVariant(u'')).toString()
        # cPickle only accepts str not unicode strings
        user_expands_string = str(unicode(user_expands).encode(u'utf8'))
        if user_expands_string:
            user_tags = cPickle.loads(user_expands_string)
            # If we have some user ones added them as well
            for t in user_tags:
                DisplayTags.add_html_tag(t)
        self.selected = -1

    def setupUi(self):
        """
        Configure the UI elements for the tab.
        """
        self.setObjectName(u'DisplayTagTab')
        self.tabTitleVisible = \
            translate(u'OpenLP.DisplayTagTab', 'Display Tags')
        self.displayTagEdit = QtGui.QWidget(self)
        self.editGroupBox = QtGui.QGroupBox(self.displayTagEdit)
        self.editGroupBox.setGeometry(QtCore.QRect(10, 220, 650, 181))
        self.editGroupBox.setObjectName(u'editGroupBox')
        self.updatePushButton = QtGui.QPushButton(self.editGroupBox)
        self.updatePushButton.setGeometry(QtCore.QRect(550, 140, 71, 26))
        self.updatePushButton.setObjectName(u'updatePushButton')
        self.layoutWidget = QtGui.QWidget(self.editGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(5, 20, 571, 114))
        self.layoutWidget.setObjectName(u'layoutWidget')
        self.formLayout = QtGui.QFormLayout(self.layoutWidget)
        self.formLayout.setObjectName(u'formLayout')
        self.descriptionLabel = QtGui.QLabel(self.layoutWidget)
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.descriptionLabel.setObjectName(u'descriptionLabel')
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.descriptionLabel)
        self.descriptionLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.descriptionLineEdit.setObjectName(u'descriptionLineEdit')
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.descriptionLineEdit)
        self.tagLabel = QtGui.QLabel(self.layoutWidget)
        self.tagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tagLabel.setObjectName(u'tagLabel')
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.tagLabel)
        self.tagLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.tagLineEdit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.tagLineEdit.setMaxLength(5)
        self.tagLineEdit.setObjectName(u'tagLineEdit')
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.tagLineEdit)
        self.startTagLabel = QtGui.QLabel(self.layoutWidget)
        self.startTagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.startTagLabel.setObjectName(u'startTagLabel')
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.startTagLabel)
        self.startTagLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.startTagLineEdit.setObjectName(u'startTagLineEdit')
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.startTagLineEdit)
        self.endTagLabel = QtGui.QLabel(self.layoutWidget)
        self.endTagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.endTagLabel.setObjectName(u'endTagLabel')
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.endTagLabel)
        self.endTagLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.endTagLineEdit.setObjectName(u'endTagLineEdit')
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.endTagLineEdit)
        self.defaultPushButton = QtGui.QPushButton(self.displayTagEdit)
        self.defaultPushButton.setGeometry(QtCore.QRect(430, 188, 71, 26))
        self.defaultPushButton.setObjectName(u'updatePushButton')
        self.deletePushButton = QtGui.QPushButton(self.displayTagEdit)
        self.deletePushButton.setGeometry(QtCore.QRect(510, 188, 71, 26))
        self.deletePushButton.setObjectName(u'deletePushButton')
        self.newPushButton = QtGui.QPushButton(self.displayTagEdit)
        self.newPushButton.setGeometry(QtCore.QRect(600, 188, 71, 26))
        self.newPushButton.setObjectName(u'newPushButton')
        self.tagTableWidget = QtGui.QTableWidget(self.displayTagEdit)
        self.tagTableWidget.setGeometry(QtCore.QRect(10, 10, 650, 171))
        self.tagTableWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.tagTableWidget.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)
        self.tagTableWidget.setAlternatingRowColors(True)
        self.tagTableWidget.setSelectionMode(
            QtGui.QAbstractItemView.SingleSelection)
        self.tagTableWidget.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)
        self.tagTableWidget.setCornerButtonEnabled(False)
        self.tagTableWidget.setObjectName(u'tagTableWidget')
        self.tagTableWidget.setColumnCount(4)
        self.tagTableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tagTableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tagTableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tagTableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tagTableWidget.setHorizontalHeaderItem(3, item)
        self.editGroupBox.setTitle(
            translate('OpenLP.DisplayTagTab', 'Edit Selection'))
        self.updatePushButton.setText(
            translate('OpenLP.DisplayTagTab', 'Update'))
        self.descriptionLabel.setText(
            translate('OpenLP.DisplayTagTab', 'Description'))
        self.tagLabel.setText(translate('OpenLP.DisplayTagTab', 'Tag'))
        self.startTagLabel.setText(
            translate('OpenLP.DisplayTagTab', 'Start tag'))
        self.endTagLabel.setText(translate('OpenLP.DisplayTagTab', 'End tag'))
        self.deletePushButton.setText(
            translate('OpenLP.DisplayTagTab', 'Delete'))
        self.defaultPushButton.setText(
            translate('OpenLP.DisplayTagTab', 'Default'))
        self.newPushButton.setText(translate('OpenLP.DisplayTagTab', 'New'))
        self.tagTableWidget.horizontalHeaderItem(0)\
            .setText(translate('OpenLP.DisplayTagTab', 'Description'))
        self.tagTableWidget.horizontalHeaderItem(1)\
            .setText(translate('OpenLP.DisplayTagTab', 'Tag id'))
        self.tagTableWidget.horizontalHeaderItem(2)\
            .setText(translate('OpenLP.DisplayTagTab', 'Start Html'))
        self.tagTableWidget.horizontalHeaderItem(3)\
            .setText(translate('OpenLP.DisplayTagTab', 'End Html'))
        QtCore.QMetaObject.connectSlotsByName(self.displayTagEdit)
        self.tagTableWidget.setColumnWidth(0, 120)
        self.tagTableWidget.setColumnWidth(1, 40)
        self.tagTableWidget.setColumnWidth(2, 240)
        self.tagTableWidget.setColumnWidth(3, 200)
        QtCore.QObject.connect(self.tagTableWidget,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onRowSelected)
        QtCore.QObject.connect(self.defaultPushButton,
            QtCore.SIGNAL(u'pressed()'), self.onDefaultPushed)
        QtCore.QObject.connect(self.newPushButton,
            QtCore.SIGNAL(u'pressed()'), self.onNewPushed)
        QtCore.QObject.connect(self.updatePushButton,
            QtCore.SIGNAL(u'pressed()'), self.onUpdatePushed)
        QtCore.QObject.connect(self.deletePushButton,
            QtCore.SIGNAL(u'pressed()'), self.onDeletePushed)

    def load(self):
        """
        Load Display and set field state.
        """
        self.newPushButton.setEnabled(True)
        self.updatePushButton.setEnabled(False)
        self.deletePushButton.setEnabled(False)
        for linenumber, html in enumerate(DisplayTags.get_html_tags()):
            self.tagTableWidget.setRowCount(
                self.tagTableWidget.rowCount() + 1)
            self.tagTableWidget.setItem(linenumber, 0,
                QtGui.QTableWidgetItem(html[u'desc']))
            self.tagTableWidget.setItem(linenumber, 1,
                QtGui.QTableWidgetItem(self._strip(html[u'start tag'])))
            self.tagTableWidget.setItem(linenumber, 2,
                QtGui.QTableWidgetItem(html[u'start html']))
            self.tagTableWidget.setItem(linenumber, 3,
                QtGui.QTableWidgetItem(html[u'end html']))
            self.tagTableWidget.resizeRowsToContents()
        self.descriptionLineEdit.setText(u'')
        self.tagLineEdit.setText(u'')
        self.startTagLineEdit.setText(u'')
        self.endTagLineEdit.setText(u'')
        self.descriptionLineEdit.setEnabled(False)
        self.tagLineEdit.setEnabled(False)
        self.startTagLineEdit.setEnabled(False)
        self.endTagLineEdit.setEnabled(False)

    def save(self):
        """
        Save Custom tags in a pickle .
        """
        temp = []
        for tag in DisplayTags.get_html_tags():
            if not tag[u'protected']:
                temp.append(tag)
        if temp:
            ctemp = cPickle.dumps(temp)
            QtCore.QSettings().setValue(u'displayTags/html_tags',
                QtCore.QVariant(ctemp))
        else:
            QtCore.QSettings().setValue(u'displayTags/html_tags',
                QtCore.QVariant(u''))

    def cancel(self):
        """
        Reset Custom tags from Settings.
        """
        self.preLoad()
        self._resetTable()

    def onRowSelected(self):
        """
        Table Row selected so display items and set field state.
        """
        row = self.tagTableWidget.currentRow()
        html = DisplayTags.get_html_tags()[row]
        self.selected = row
        self.descriptionLineEdit.setText(html[u'desc'])
        self.tagLineEdit.setText(self._strip(html[u'start tag']))
        self.startTagLineEdit.setText(html[u'start html'])
        self.endTagLineEdit.setText(html[u'end html'])
        if html[u'protected']:
            self.descriptionLineEdit.setEnabled(False)
            self.tagLineEdit.setEnabled(False)
            self.startTagLineEdit.setEnabled(False)
            self.endTagLineEdit.setEnabled(False)
            self.updatePushButton.setEnabled(False)
            self.deletePushButton.setEnabled(False)
        else:
            self.descriptionLineEdit.setEnabled(True)
            self.tagLineEdit.setEnabled(True)
            self.startTagLineEdit.setEnabled(True)
            self.endTagLineEdit.setEnabled(True)
            self.updatePushButton.setEnabled(True)
            self.deletePushButton.setEnabled(True)

    def onNewPushed(self):
        """
        Add a new tag to list only if it is not a duplicate.
        """
        for html in DisplayTags.get_html_tags():
            if self._strip(html[u'start tag']) == u'n':
                critical_error_message_box(
                    translate('OpenLP.DisplayTagTab', 'Update Error'),
                    translate('OpenLP.DisplayTagTab',
                    'Tag "n" already defined.'))
                return
        # Add new tag to list
        tag = {u'desc': u'New Item', u'start tag': u'{n}',
            u'start html': u'<Html_here>', u'end tag': u'{/n}',
            u'end html': u'</and here>', u'protected': False}
        DisplayTags.add_html_tag(tag)
        self._resetTable()
        # Highlight new row
        self.tagTableWidget.selectRow(self.tagTableWidget.rowCount() - 1)

    def onDefaultPushed(self):
        """
        Remove all Custom Tags and reset to base set only.
        """
        DisplayTags.reset_html_tags()
        self._resetTable()

    def onDeletePushed(self):
        """
        Delete selected custom tag.
        """
        if self.selected != -1:
            DisplayTags.remove_html_tag(self.selected)
            self.selected = -1
        self._resetTable()

    def onUpdatePushed(self):
        """
        Update Custom Tag details if not duplicate.
        """
        html_expands = DisplayTags.get_html_tags()
        if self.selected != -1:
            html = html_expands[self.selected]
            tag = unicode(self.tagLineEdit.text())
            for linenumber, html1 in enumerate(html_expands):
                if self._strip(html1[u'start tag']) == tag and \
                    linenumber != self.selected:
                    critical_error_message_box(
                        translate('OpenLP.DisplayTagTab', 'Update Error'),
                        unicode(translate('OpenLP.DisplayTagTab',
                        'Tag %s already defined.')) % tag)
                    return
            html[u'desc'] = unicode(self.descriptionLineEdit.text())
            html[u'start html'] = unicode(self.startTagLineEdit.text())
            html[u'end html'] = unicode(self.endTagLineEdit.text())
            html[u'start tag'] = u'{%s}' % tag
            html[u'end tag'] = u'{/%s}' % tag
            self.selected = -1
        self._resetTable()

    def _resetTable(self):
        """
        Reset List for loading.
        """
        self.tagTableWidget.clearContents()
        self.tagTableWidget.setRowCount(0)
        self.load()

    def _strip(self, tag):
        """
        Remove tag wrappers for editing.
        """
        tag = tag.replace(u'{', u'')
        tag = tag.replace(u'}', u'')
        return tag
