# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode       #
# Woldsund                                                                    #
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

from openlp.core.lib import translate, DisplayTags
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui.displaytagdialog import Ui_DisplayTagDialog

class DisplayTagForm(QtGui.QDialog, Ui_DisplayTagDialog):
    """
    The :class:`DisplayTagTab` manages the settings tab .
    """
    def __init__(self, parent):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self._loadDisplayTags()
        QtCore.QObject.connect(self.tagTableWidget,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onRowSelected)
        QtCore.QObject.connect(self.defaultPushButton,
            QtCore.SIGNAL(u'pressed()'), self.onDefaultPushed)
        QtCore.QObject.connect(self.newPushButton,
            QtCore.SIGNAL(u'pressed()'), self.onNewPushed)
        QtCore.QObject.connect(self.savePushButton,
            QtCore.SIGNAL(u'pressed()'), self.onSavedPushed)
        QtCore.QObject.connect(self.deletePushButton,
            QtCore.SIGNAL(u'pressed()'), self.onDeletePushed)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'rejected()'),
            self.close)

    def exec_(self):
        """
        Load Display and set field state.
        """
        # Create initial copy from master
        self._loadDisplayTags()
        self._resetTable()
        self.selected = -1
        return QtGui.QDialog.exec_(self)

    def _loadDisplayTags(self):
        """
        Load the Tags from store so can be used in the system or used to
        update the display. If Cancel was selected this is needed to reset the
        dsiplay to the correct version.
        """
        # Initial Load of the Tags
        DisplayTags.reset_html_tags()
        user_expands = QtCore.QSettings().value(u'displayTags/html_tags',
            QtCore.QVariant(u'')).toString()
        # cPickle only accepts str not unicode strings
        user_expands_string = str(unicode(user_expands).encode(u'utf8'))
        if user_expands_string:
            user_tags = cPickle.loads(user_expands_string)
            # If we have some user ones added them as well
            DisplayTags.add_html_tags(user_tags)

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
            self.savePushButton.setEnabled(False)
            self.deletePushButton.setEnabled(False)
        else:
            self.descriptionLineEdit.setEnabled(True)
            self.tagLineEdit.setEnabled(True)
            self.startTagLineEdit.setEnabled(True)
            self.endTagLineEdit.setEnabled(True)
            self.savePushButton.setEnabled(True)
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
        tag = {
            u'desc': translate('OpenLP.DisplayTagTab', 'New Tag'),
            u'start tag': u'{n}',
            u'start html': translate('OpenLP.DisplayTagTab', '<Html_here>'),
            u'end tag': u'{/n}',
            u'end html': translate('OpenLP.DisplayTagTab', '</and here>'),
            u'protected': False
        }
        DisplayTags.add_html_tags([tag])
        self._resetTable()
        # Highlight new row
        self.tagTableWidget.selectRow(self.tagTableWidget.rowCount() - 1)
        self.onRowSelected()

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

    def onSavedPushed(self):
        """
        Update Custom Tag details if not duplicate and save the data.
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

    def _resetTable(self):
        """
        Reset List for loading.
        """
        self.tagTableWidget.clearContents()
        self.tagTableWidget.setRowCount(0)
        self.newPushButton.setEnabled(True)
        self.savePushButton.setEnabled(False)
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

    def _strip(self, tag):
        """
        Remove tag wrappers for editing.
        """
        tag = tag.replace(u'{', u'')
        tag = tag.replace(u'}', u'')
        return tag
