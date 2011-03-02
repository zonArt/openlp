# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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

import ConfigParser
import io
import logging

from PyQt4 import QtCore, QtGui

from firsttimewizard import Ui_FirstTimeWizard

from openlp.core.lib import translate, PluginStatus
from openlp.core.utils import get_web_page

log = logging.getLogger(__name__)

class FirstTimeForm(QtGui.QWizard, Ui_FirstTimeWizard):
    """
    This is the Theme Import Wizard, which allows easy creation and editing of
    OpenLP themes.
    """
    log.info(u'ThemeWizardForm loaded')

    def __init__(self, parent=None):
        # check to see if we have web access
        self.config = ConfigParser.ConfigParser()
        self.webAccess = get_web_page(u'http://openlp.org/files/frw/download.cfg')
        if self.webAccess:
            files = self.webAccess.read()
            self.config.readfp(io.BytesIO(files))
        QtGui.QWizard.__init__(self, parent)
        self.setupUi(self)
        #self.registerFields()

    def exec_(self, edit=False):
        """
        Run the wizard.
        """
        self.setDefaults()
        return QtGui.QWizard.exec_(self)

    def setDefaults(self):
        """
        Set up display at start of theme edit.
        """
        self.restart()
        # Sort out internet access for downloads
        if self.webAccess:
            self.internetGroupBox.setVisible(True)
            self.noInternetLabel.setVisible(False)
            treewidgetitem = QtGui.QTreeWidgetItem(self.selectionTreeWidget)
            treewidgetitem.setText(0, u'Songs')
            self.__loadChild(treewidgetitem, u'songs', u'languages', u'songs')
            treewidgetitem = QtGui.QTreeWidgetItem(self.selectionTreeWidget)
            treewidgetitem.setText(0, u'Bibles')
            self.__loadChild(treewidgetitem, u'bibles', u'translations', u'bible')
            treewidgetitem = QtGui.QTreeWidgetItem(self.selectionTreeWidget)
            treewidgetitem.setText(0, u'Themes')
            self.__loadChild(treewidgetitem, u'themes', u'files', 'theme')
        else:
            self.internetGroupBox.setVisible(False)
            self.noInternetLabel.setVisible(True)

    def __loadChild(self, tree, list, tag, root):
        files = self.config.get(list, tag)
        files = files.split(u',')
        for file in files:
            if file:
                child = QtGui.QTreeWidgetItem(tree)
                child.setText(0, self.config.get(u'%s_%s' %(root, file), u'title'))
                child.setData(0, QtCore.Qt.UserRole,
                    QtCore.QVariant(self.config.get(u'%s_%s' %(root, file), u'filename')))
                child.setCheckState(0, QtCore.Qt.Unchecked)
                child.setFlags(QtCore.Qt.ItemIsUserCheckable |
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def initializePage(self, id):
        """
        Set up the pages for Initial run through dialog
        """
        wizardPage = self.page(id)
        if wizardPage == self.DefaultsPage:
            listIterator = QtGui.QTreeWidgetItemIterator(self.selectionTreeWidget)
            while listIterator.value():
                parent = listIterator.value().parent()
                if parent and listIterator.value().checkState(0) == QtCore.Qt.Checked:
                    if unicode(parent.text(0)) == u'Themes':
                        self.themeSelectionComboBox.addItem(listIterator.value().text(0))
                listIterator += 1

    def accept(self):
        self.__pluginStatus(self.songsCheckBox, u'songs/status')
        self.__pluginStatus(self.bibleCheckBox, u'bibles/status')
        self.__pluginStatus(self.presentationCheckBox, u'presentations/status')
        self.__pluginStatus(self.imageCheckBox, u'images/status')
        self.__pluginStatus(self.mediaCheckBox, u'media/status')
        self.__pluginStatus(self.remoteCheckBox, u'remotes/status')
        self.__pluginStatus(self.customCheckBox, u'custom/status')
        self.__pluginStatus(self.songUsageCheckBox, u'songusage/status')
        self.__pluginStatus(self.alertCheckBox, u'alerts/status')

        listIterator = QtGui.QTreeWidgetItemIterator(self.selectionTreeWidget)
        while listIterator.value():
            type = listIterator.value().parent()
            if listIterator.value().parent():
                if listIterator.value().checkState(0) == QtCore.Qt.Checked:
                    # Install
                    print type,  listIterator.value().data(0, QtCore.Qt.UserRole).toString()
                    #if type == u'Themes':
                        #self.themeSelectionComboBox.addItem(listIterator.value().text())
            listIterator += 1
        return QtGui.QWizard.accept(self)

    def __pluginStatus(self, field, tag):
        status = PluginStatus.Active if field.checkState() \
            == QtCore.Qt.Checked else PluginStatus.Inactive
        QtCore.QSettings().setValue(tag, QtCore.QVariant(status))
