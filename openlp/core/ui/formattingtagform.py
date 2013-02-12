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
The :mod:`formattingtagform` provides an Tag Edit facility. The Base set are protected and included each time loaded.
Custom tags can be defined and saved. The Custom Tag arrays are saved in a pickle so QSettings works on them. Base Tags
cannot be changed.
"""
from PyQt4 import QtCore, QtGui

from openlp.core.lib import FormattingTags, translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui.formattingtagdialog import Ui_FormattingTagDialog


class FormattingTagForm(QtGui.QDialog, Ui_FormattingTagDialog):
    """
    The :class:`FormattingTagForm` manages the settings tab .
    """
    def __init__(self, parent):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.tagTableWidget, QtCore.SIGNAL(u'itemSelectionChanged()'), self.onRowSelected)
        QtCore.QObject.connect(self.newPushButton, QtCore.SIGNAL(u'clicked()'), self.onNewClicked)
        QtCore.QObject.connect(self.savePushButton, QtCore.SIGNAL(u'clicked()'), self.onSavedClicked)
        QtCore.QObject.connect(self.deletePushButton, QtCore.SIGNAL(u'clicked()'), self.onDeleteClicked)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(u'rejected()'), self.close)
        QtCore.QObject.connect(self.descriptionLineEdit, QtCore.SIGNAL(u'textEdited(QString)'), self.onTextEdited)
        QtCore.QObject.connect(self.tagLineEdit, QtCore.SIGNAL(u'textEdited(QString)'), self.onTextEdited)
        QtCore.QObject.connect(self.startTagLineEdit, QtCore.SIGNAL(u'textEdited(QString)'), self.onTextEdited)
        QtCore.QObject.connect(self.endTagLineEdit, QtCore.SIGNAL(u'textEdited(QString)'), self.onTextEdited)
        # Forces reloading of tags from openlp configuration.
        FormattingTags.load_tags()

    def exec_(self):
        """
        Load Display and set field state.
        """
        # Create initial copy from master
        self._reloadTable()
        self.selected = -1
        return QtGui.QDialog.exec_(self)

    def onRowSelected(self):
        """
        Table Row selected so display items and set field state.
        """
        self.savePushButton.setEnabled(False)
        self.selected = self.tagTableWidget.currentRow()
        html = FormattingTags.get_html_tags()[self.selected]
        self.descriptionLineEdit.setText(html[u'desc'])
        self.tagLineEdit.setText(self._strip(html[u'start tag']))
        self.startTagLineEdit.setText(html[u'start html'])
        self.endTagLineEdit.setText(html[u'end html'])
        if html[u'protected']:
            self.descriptionLineEdit.setEnabled(False)
            self.tagLineEdit.setEnabled(False)
            self.startTagLineEdit.setEnabled(False)
            self.endTagLineEdit.setEnabled(False)
            self.deletePushButton.setEnabled(False)
        else:
            self.descriptionLineEdit.setEnabled(True)
            self.tagLineEdit.setEnabled(True)
            self.startTagLineEdit.setEnabled(True)
            self.endTagLineEdit.setEnabled(True)
            self.deletePushButton.setEnabled(True)

    def onTextEdited(self, text):
        """
        Enable the ``savePushButton`` when any of the selected tag's properties
        has been changed.
        """
        self.savePushButton.setEnabled(True)

    def onNewClicked(self):
        """
        Add a new tag to list only if it is not a duplicate.
        """
        for html in FormattingTags.get_html_tags():
            if self._strip(html[u'start tag']) == u'n':
                critical_error_message_box(
                    translate('OpenLP.FormattingTagForm', 'Update Error'),
                    translate('OpenLP.FormattingTagForm', 'Tag "n" already defined.'))
                return
        # Add new tag to list
        tag = {
            u'desc': translate('OpenLP.FormattingTagForm', 'New Tag'),
            u'start tag': u'{n}',
            u'start html': translate('OpenLP.FormattingTagForm', '<HTML here>'),
            u'end tag': u'{/n}',
            u'end html': translate('OpenLP.FormattingTagForm', '</and here>'),
            u'protected': False,
            u'temporary': False
        }
        FormattingTags.add_html_tags([tag])
        FormattingTags.save_html_tags()
        self._reloadTable()
        # Highlight new row
        self.tagTableWidget.selectRow(self.tagTableWidget.rowCount() - 1)
        self.onRowSelected()
        self.tagTableWidget.scrollToBottom()
        #self.savePushButton.setEnabled(False)

    def onDeleteClicked(self):
        """
        Delete selected custom tag.
        """
        if self.selected != -1:
            FormattingTags.remove_html_tag(self.selected)
            # As the first items are protected we should not have to take care
            # of negative indexes causing tracebacks.
            self.tagTableWidget.selectRow(self.selected - 1)
            self.selected = -1
            FormattingTags.save_html_tags()
            self._reloadTable()

    def onSavedClicked(self):
        """
        Update Custom Tag details if not duplicate and save the data.
        """
        html_expands = FormattingTags.get_html_tags()
        if self.selected != -1:
            html = html_expands[self.selected]
            tag = self.tagLineEdit.text()
            for linenumber, html1 in enumerate(html_expands):
                if self._strip(html1[u'start tag']) == tag and linenumber != self.selected:
                    critical_error_message_box(
                        translate('OpenLP.FormattingTagForm', 'Update Error'),
                        translate('OpenLP.FormattingTagForm', 'Tag %s already defined.') % tag)
                    return
            html[u'desc'] = self.descriptionLineEdit.text()
            html[u'start html'] = self.startTagLineEdit.text()
            html[u'end html'] = self.endTagLineEdit.text()
            html[u'start tag'] = u'{%s}' % tag
            html[u'end tag'] = u'{/%s}' % tag
            # Keep temporary tags when the user changes one.
            html[u'temporary'] = False
            self.selected = -1
        FormattingTags.save_html_tags()
        self._reloadTable()

    def _reloadTable(self):
        """
        Reset List for loading.
        """
        self.tagTableWidget.clearContents()
        self.tagTableWidget.setRowCount(0)
        self.newPushButton.setEnabled(True)
        self.savePushButton.setEnabled(False)
        self.deletePushButton.setEnabled(False)
        for linenumber, html in enumerate(FormattingTags.get_html_tags()):
            self.tagTableWidget.setRowCount(self.tagTableWidget.rowCount() + 1)
            self.tagTableWidget.setItem(linenumber, 0, QtGui.QTableWidgetItem(html[u'desc']))
            self.tagTableWidget.setItem(linenumber, 1, QtGui.QTableWidgetItem(self._strip(html[u'start tag'])))
            self.tagTableWidget.setItem(linenumber, 2, QtGui.QTableWidgetItem(html[u'start html']))
            self.tagTableWidget.setItem(linenumber, 3, QtGui.QTableWidgetItem(html[u'end html']))
            # Permanent (persistent) tags do not have this key.
            if u'temporary' not in html:
                html[u'temporary'] = False
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
