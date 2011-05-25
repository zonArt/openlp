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
The bible import functions for OpenLP
"""
import logging
import os.path
import re

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, SettingsManager, translate
from openlp.core.lib.db import delete_database
from openlp.core.lib.ui import UiStrings, critical_error_message_box
from openlp.core.ui.wizard import OpenLPWizard, WizardStrings
from openlp.core.utils import AppLocation, delete_file
from openlp.plugins.bibles.lib.db import BibleDB, BibleMeta, OldBibleDB,\
    BiblesResourcesDB, clean_filename
from openlp.plugins.bibles.lib.http import BSExtract, BGExtract, CWExtract

log = logging.getLogger(__name__)


class BibleUpgradeForm(OpenLPWizard):
    """
    This is the Bible Upgrade Wizard, which allows easy importing of Bibles
    into OpenLP from older OpenLP2 database versions.
    """
    log.info(u'BibleUpgradeForm loaded')

    def __init__(self, parent, manager, bibleplugin):
        """
        Instantiate the wizard, and run any extra setup we need to.

        ``parent``
            The QWidget-derived parent of the wizard.

        ``manager``
            The Bible manager.

        ``bibleplugin``
            The Bible plugin.
        """
        self.manager = manager
        self.mediaItem = bibleplugin.mediaItem
        self.suffix = u'.sqlite'
        self.settingsSection = u'bibles'
        self.path = AppLocation.get_section_data_path(
            self.settingsSection)
        self.files = self.manager.old_bible_databases
        self.success = {}
        self.newbibles = {}
        OpenLPWizard.__init__(self, parent, bibleplugin, u'bibleUpgradeWizard',
            u':/wizards/wizard_importbible.bmp')

    def setupUi(self, image):
        """
        Set up the UI for the bible wizard.
        """
        OpenLPWizard.setupUi(self, image)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_stop_wizard'), self.stop_import)

    def stop_import(self):
        """
        Stops the import of the Bible.
        """
        log.debug(u'Stopping import')
        self.stop_import_flag = True

    def onCheckBoxIndexChanged(self, index):
        """
        Show/ Hide warnings if CheckBox state has changed
        """
        for number, filename in enumerate(self.files):
            if not self.checkBox[number].checkState() == QtCore.Qt.Checked:
                self.verticalWidget[number].hide()
                self.formWidget[number].hide()
            else:
                version_name = unicode(self.versionNameEdit[number].text())
                if self.manager.exists(version_name):
                    self.verticalWidget[number].show()
                    self.formWidget[number].show()

    def reject(self):
        """
        Stop the wizard on cancel button, close button or ESC key.
        """
        log.debug(u'Wizard cancelled by user')
        if self.currentPage() == self.progressPage:
            Receiver.send_message(u'openlp_stop_wizard')
            for bible in self.newbibles.itervalues():
                delete_database(self.path, clean_filename(
                    bible.get_name())) 
        self.done(QtGui.QDialog.Rejected)

    def onCurrentIdChanged(self, pageId):
        """
        Perform necessary functions depending on which wizard page is active.
        """
        if self.page(pageId) == self.progressPage:
            self.preWizard()
            self.performWizard()
            self.postWizard()
        elif self.page(pageId) == self.selectPage and self.maxBibles == 0:
            self.next()

    def onFinishButton(self):
        """
        Some cleanup while finishing
        """
        for number, filename in enumerate(self.files):
            if self.success[number]:
                delete_file(os.path.join(self.path, filename))

    def customInit(self):
        """
        Perform any custom initialisation for bible upgrading.
        """
        self.manager.set_process_dialog(self)
        self.restart()

    def customSignals(self):
        """
        Set up the signals used in the bible importer.
        """
        QtCore.QObject.connect(self.finishButton,
            QtCore.SIGNAL(u'clicked()'), self.onFinishButton)

    def addCustomPages(self):
        """
        Add the bible import specific wizard pages.
        """
        self.selectPage = QtGui.QWizardPage()
        self.selectPage.setObjectName(u'SelectPage')
        self.pageLayout = QtGui.QVBoxLayout(self.selectPage)
        self.pageLayout.setObjectName(u'pageLayout')
        self.scrollArea = QtGui.QScrollArea(self.selectPage)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(u'scrollArea')
        self.scrollArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollAreaContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaContents.setObjectName(u'scrollAreaContents')
        self.formLayout = QtGui.QVBoxLayout(self.scrollAreaContents)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName(u'formLayout')
        self.addScrollArea()
        self.pageLayout.addWidget(self.scrollArea)
        self.addPage(self.selectPage)

    def addScrollArea(self):
        """
        Add the content to the scrollArea.
        """
        self.checkBox = {}
        self.versionNameEdit = {}
        self.versionNameLabel = {}
        self.versionInfoLabel = {}
        self.versionInfoPixmap = {}
        self.verticalWidget = {}
        self.horizontalLayout = {}
        self.formWidget = {}
        self.formLayoutAttention = {}
        for number, filename in enumerate(self.files):
            bible = OldBibleDB(self.mediaItem, path=self.path, file=filename)
            self.checkBox[number] = QtGui.QCheckBox(self.scrollAreaContents)
            checkBoxName = u'checkBox[%d]' % number
            self.checkBox[number].setObjectName(checkBoxName)
            self.checkBox[number].setText(bible.get_name())
            self.checkBox[number].setCheckState(QtCore.Qt.Checked)
            self.formLayout.addWidget(self.checkBox[number])
            self.verticalWidget[number] = QtGui.QWidget(self.scrollAreaContents)
            verticalWidgetName = u'verticalWidget[%d]' % number
            self.verticalWidget[number].setObjectName(verticalWidgetName)
            self.horizontalLayout[number] = QtGui.QHBoxLayout(
                self.verticalWidget[number])
            self.horizontalLayout[number].setContentsMargins(25, 0, 0, 0)
            horizontalLayoutName = u'horizontalLayout[%d]' % number
            self.horizontalLayout[number].setObjectName(horizontalLayoutName)
            self.versionInfoPixmap[number] = QtGui.QLabel(
                self.verticalWidget[number])
            versionInfoPixmapName = u'versionInfoPixmap[%d]' % number
            self.versionInfoPixmap[number].setObjectName(versionInfoPixmapName)
            self.versionInfoPixmap[number].setPixmap(QtGui.QPixmap(
                u':/bibles/bibles_upgrade_alert.png'))
            self.versionInfoPixmap[number].setAlignment(QtCore.Qt.AlignRight)
            self.horizontalLayout[number].addWidget(
                self.versionInfoPixmap[number])
            self.versionInfoLabel[number] = QtGui.QLabel(
                self.verticalWidget[number])
            versionInfoLabelName = u'versionInfoLabel[%d]' % number
            self.versionInfoLabel[number].setObjectName(versionInfoLabelName)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, 
                QtGui.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                self.versionInfoLabel[number].sizePolicy().hasHeightForWidth())
            self.versionInfoLabel[number].setSizePolicy(sizePolicy)
            self.horizontalLayout[number].addWidget(
                self.versionInfoLabel[number])
            self.formLayout.addWidget(self.verticalWidget[number])
            self.formWidget[number] = QtGui.QWidget(self.scrollAreaContents)
            formWidgetName = u'formWidget[%d]' % number
            self.formWidget[number].setObjectName(formWidgetName)
            self.formLayoutAttention[number] = QtGui.QFormLayout(
                self.formWidget[number])
            self.formLayoutAttention[number].setContentsMargins(25, 0, 0, 5)
            formLayoutAttentionName = u'formLayoutAttention[%d]' % number
            self.formLayoutAttention[number].setObjectName(
                formLayoutAttentionName)
            self.versionNameLabel[number] = QtGui.QLabel(
                self.formWidget[number])
            self.versionNameLabel[number].setObjectName(u'VersionNameLabel')
            self.formLayoutAttention[number].setWidget(0, 
                QtGui.QFormLayout.LabelRole, self.versionNameLabel[number])
            self.versionNameEdit[number] = QtGui.QLineEdit(
                self.formWidget[number])
            self.versionNameEdit[number].setObjectName(u'VersionNameEdit')
            self.formLayoutAttention[number].setWidget(0, 
                QtGui.QFormLayout.FieldRole, self.versionNameEdit[number])
            self.versionNameEdit[number].setText(bible.get_name())
            self.formLayout.addWidget(self.formWidget[number])
            #Set up the Signal for the checkbox
            QtCore.QObject.connect(self.checkBox[number],
                QtCore.SIGNAL(u'stateChanged(int)'),
                self.onCheckBoxIndexChanged)
        self.spacerItem = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.formLayout.addItem(self.spacerItem)
        self.scrollArea.setWidget(self.scrollAreaContents)

    def clearScrollArea(self):
        """
        Remove the content from the scrollArea.
        """
        for number, filename in enumerate(self.files):
            self.formLayout.removeWidget(self.checkBox[number])
            self.checkBox[number].setParent(None)
            self.horizontalLayout[number].removeWidget(
                self.versionInfoPixmap[number])
            self.versionInfoPixmap[number].setParent(None)
            self.horizontalLayout[number].removeWidget(
                self.versionInfoLabel[number])
            self.versionInfoLabel[number].setParent(None)
            self.formLayout.removeWidget(self.verticalWidget[number])
            self.verticalWidget[number].setParent(None)
            self.formLayoutAttention[number].removeWidget(
                self.versionNameLabel[number])
            self.versionNameLabel[number].setParent(None)
            self.formLayoutAttention[number].removeWidget(
                self.versionNameEdit[number])
            self.formLayoutAttention[number].deleteLater()
            self.versionNameEdit[number].setParent(None)
            self.formLayout.removeWidget(self.formWidget[number])
            self.formWidget[number].setParent(None)
        self.formLayout.removeItem(self.spacerItem)  

    def retranslateUi(self):
        """
        Allow for localisation of the bible import wizard.
        """
        self.setWindowTitle(translate('BiblesPlugin.UpgradeWizardForm', 
            'Bible Upgrade Wizard'))
        self.titleLabel.setText(WizardStrings.HeaderStyle %
            translate('OpenLP.Ui', 'Welcome to the Bible Upgrade Wizard'))
        self.informationLabel.setText(
            translate('BiblesPlugin.UpgradeWizardForm',
            'This wizard will help you to upgrade your existing Bibles from a '
            'prior version of OpenLP 2. Click the next button below to start '
            'the process by selecting the Bibles to upgrade.'))
        self.selectPage.setTitle(
            translate('BiblesPlugin.UpgradeWizardForm',
            'Select Bibles'))
        self.selectPage.setSubTitle(
            translate('BiblesPlugin.UpgradeWizardForm',
            'Please select the Bibles to upgrade'))
        for number, bible in enumerate(self.files):
            self.versionNameLabel[number].setText(
                translate('BiblesPlugin.UpgradeWizardForm', 'Version name:'))
            self.versionInfoLabel[number].setText(
                translate('BiblesPlugin.UpgradeWizardForm', 'This '
                'Bible still exists. Please change the name or uncheck it.'))
        self.progressPage.setTitle(WizardStrings.Importing)
        self.progressPage.setSubTitle(
            translate('BiblesPlugin.UpgradeWizardForm',
            'Please wait while your Bibles are upgraded.'))
        self.progressLabel.setText(WizardStrings.Ready)
        self.progressBar.setFormat(u'%p%')

    def validateCurrentPage(self):
        """
        Validate the current page before moving on to the next page.
        """
        if self.currentPage() == self.welcomePage:
            return True
        elif self.currentPage() == self.selectPage:
            for number, filename in enumerate(self.files):
                if not self.checkBox[number].checkState() == QtCore.Qt.Checked:
                    continue
                version_name = unicode(self.versionNameEdit[number].text())
                oldbible = OldBibleDB(self.mediaItem, path=self.path, 
                    file=filename)
                oldname = oldbible.get_name()
                if not version_name:
                    critical_error_message_box(UiStrings().EmptyField,
                        translate('BiblesPlugin.UpgradeWizardForm',
                        'You need to specify a version name for your Bible.'))
                    self.versionNameEdit[number].setFocus()
                    return False
                elif self.manager.exists(version_name):
                    critical_error_message_box(
                        translate('BiblesPlugin.UpgradeWizardForm', 
                            'Bible Exists'),
                        translate('BiblesPlugin.UpgradeWizardForm',
                        'This Bible already exists. Please upgrade '
                        'a different Bible, delete the existing one or '
                        'uncheck.'))
                    self.versionNameEdit[number].setFocus()
                    return False
                elif os.path.exists(os.path.join(self.path, clean_filename(
                    version_name))) and version_name == oldname:
                    newfilename = u'old_database_%s' % filename
                    if not os.path.exists(os.path.join(self.path, 
                        newfilename)):
                        os.rename(os.path.join(self.path, filename), 
                            os.path.join(self.path, newfilename))
                        self.files[number] = newfilename
                        continue
                    else:
                        critical_error_message_box(
                            translate('BiblesPlugin.UpgradeWizardForm', 
                            'Bible Exists'),
                            translate('BiblesPlugin.UpgradeWizardForm',
                            'This Bible already exists. Please upgrade '
                            'a different Bible, delete the existing one or '
                            'uncheck.'))
                        self.verticalWidget[number].show()
                        self.formWidget[number].show()
                        self.versionNameEdit[number].setFocus()
                        return False
                elif os.path.exists(os.path.join(self.path, 
                    clean_filename(version_name))):
                    critical_error_message_box(
                        translate('BiblesPlugin.UpgradeWizardForm', 
                        'Bible Exists'),
                        translate('BiblesPlugin.UpgradeWizardForm',
                        'This Bible already exists. Please upgrade '
                        'a different Bible, delete the existing one or '
                        'uncheck.'))
                    self.versionNameEdit[number].setFocus()
                    return False
            return True
        if self.currentPage() == self.progressPage:
            return True

    def setDefaults(self):
        """
        Set default values for the wizard pages.
        """
        log.debug(u'BibleUpgrade setDefaults')
        settings = QtCore.QSettings()
        settings.beginGroup(self.plugin.settingsSection)
        self.stop_import_flag = False
        self.success.clear()
        self.newbibles.clear()
        self.clearScrollArea()
        self.files = self.manager.old_bible_databases
        self.addScrollArea()
        self.retranslateUi()
        self.maxBibles = len(self.files)
        for number, filename in enumerate(self.files):
            self.checkBox[number].setCheckState(QtCore.Qt.Checked)
            oldbible = OldBibleDB(self.mediaItem, path=self.path, 
                file=filename)
            oldname = oldbible.get_name()
            if self.manager.exists(oldname):
                self.verticalWidget[number].show()
                self.formWidget[number].show()
            else:
                self.verticalWidget[number].hide()
                self.formWidget[number].hide()
        self.progressBar.show()
        self.restart()
        self.finishButton.setVisible(False)
        self.cancelButton.setVisible(True)
        settings.endGroup()

    def preWizard(self):
        """
        Prepare the UI for the upgrade.
        """
        OpenLPWizard.preWizard(self)
        self.progressLabel.setText(translate(
            'BiblesPlugin.UpgradeWizardForm',
            'Starting upgrading bible(s)...'))
        Receiver.send_message(u'openlp_process_events')

    def performWizard(self):
        """
        Perform the actual upgrade.
        """
        include_webbible = False
        proxy_server = None
        if self.maxBibles == 0:
            self.progressLabel.setText(
                translate('BiblesPlugin.UpgradeWizardForm', 'There are no '
                'Bibles available to upgrade.'))
            self.progressBar.hide()
            return
        self.maxBibles = 0
        for number, file in enumerate(self.files):
            if self.checkBox[number].checkState() == QtCore.Qt.Checked:
                self.maxBibles += 1
        number = 0
        for biblenumber, filename in enumerate(self.files):
            if self.stop_import_flag:
                break
            bible_failed = False
            self.success[biblenumber] = False
            if not self.checkBox[biblenumber].checkState() == QtCore.Qt.Checked:
                continue
            self.progressBar.reset()
            oldbible = OldBibleDB(self.mediaItem, path=self.path, 
                file=filename)
            name = oldbible.get_name()
            if name is None:
                delete_file(os.path.join(self.path, filename))
                self.incrementProgressBar(unicode(translate(
                    'BiblesPlugin.UpgradeWizardForm', 
                    'Upgrading Bible %s of %s: "%s"\nFailed')) % 
                    (number+1, self.maxBibles, name), 
                    self.progressBar.maximum() - self.progressBar.value())
                number += 1
                continue
            self.progressLabel.setText(unicode(translate(
                'BiblesPlugin.UpgradeWizardForm', 
                'Upgrading Bible %s of %s: "%s"\nImporting ...')) % 
                (number + 1, self.maxBibles, name))
            if os.path.exists(os.path.join(self.path, filename)):
                name = unicode(self.versionNameEdit[biblenumber].text())
            self.newbibles[number] = BibleDB(self.mediaItem, path=self.path,
                name=name)
            metadata = oldbible.get_metadata()
            webbible = False
            meta_data = {}
            for meta in metadata:
                meta_data[meta[u'key']] = meta[u'value']
                if not meta[u'key'] == u'Version':
                    self.newbibles[number].create_meta(meta[u'key'],
                        meta[u'value'])
                else:
                    self.newbibles[number].create_meta(meta[u'key'], name)
                if meta[u'key'] == u'download source':
                    webbible = True
                    include_webbible = True
                if meta.has_key(u'proxy server'):
                    proxy_server = meta[u'proxy server']
            if webbible:
                if meta_data[u'download source'].lower() == u'crosswalk':
                    handler = CWExtract(proxy_server)
                elif meta_data[u'download source'].lower() == u'biblegateway':
                    handler = BGExtract(proxy_server)
                elif meta_data[u'download source'].lower() == u'bibleserver':
                    handler = BSExtract(proxy_server)
                books = handler.get_books_from_http(meta_data[u'download name'])
                if not books:
                    log.exception(u'Importing books from %s - download '\
                        u'name: "%s" failed' % (
                        meta_data[u'download source'], 
                        meta_data[u'download name']))
                    delete_database(self.path, 
                        clean_filename(self.newbibles[number].get_name())) 
                    del self.newbibles[number]
                    critical_error_message_box(
                        translate('BiblesPlugin.UpgradeWizardForm', 
                        'Download Error'),
                        translate('BiblesPlugin.UpgradeWizardForm', 
                        'To upgrade your Web Bibles an Internet connection is '
                        'required. If you have a working Internet connection '
                        'and this error still occurs, please report a bug.'))
                    self.incrementProgressBar(unicode(translate(
                        'BiblesPlugin.UpgradeWizardForm', 
                        'Upgrading Bible %s of %s: "%s"\nFailed')) % 
                        (number+1, self.maxBibles, name), 
                        self.progressBar.maximum()-self.progressBar.value())
                    number += 1
                    continue
                bible = BiblesResourcesDB.get_webbible(
                    meta_data[u'download name'], 
                    meta_data[u'download source'].lower())
                if bible[u'language_id']:
                    language_id = bible[u'language_id']
                    self.newbibles[number].create_meta(u'language_id',
                        language_id)
                else:
                    language_id = self.newbibles[number].get_language()
                if not language_id:
                    log.exception(u'Upgrading from "%s" '\
                        'failed' % filename)
                    delete_database(self.path, 
                        clean_filename(self.newbibles[number].get_name()))
                    del self.newbibles[number]
                    self.incrementProgressBar(unicode(translate(
                        'BiblesPlugin.UpgradeWizardForm', 
                        'Upgrading Bible %s of %s: "%s"\nFailed')) % 
                        (number+1, self.maxBibles, name),
                        self.progressBar.maximum()-self.progressBar.value())
                    number += 1
                    continue
                self.progressBar.setMaximum(len(books))
                for book in books:
                    if self.stop_import_flag:
                        break
                    self.incrementProgressBar(unicode(translate(
                        'BiblesPlugin.UpgradeWizardForm', 
                        'Upgrading Bible %s of %s: "%s"\n'
                        'Importing %s ...')) % 
                        (number+1, self.maxBibles, name, book))
                    book_ref_id = self.newbibles[number].\
                        get_book_ref_id_by_name(book, len(books), language_id)
                    if not book_ref_id:
                        log.exception(u'Importing books from %s - download '\
                            u'name: "%s" aborted by user' % (
                            meta_data[u'download source'], 
                            meta_data[u'download name']))
                        delete_database(self.path, 
                            clean_filename(self.newbibles[number].get_name()))
                        del self.newbibles[number]
                        bible_failed = True
                        break
                    book_details = BiblesResourcesDB.get_book_by_id(book_ref_id)
                    self.newbibles[number].create_book(book, book_ref_id, 
                        book_details[u'testament_id'])
            else:
                language_id = self.newbibles[number].get_object(BibleMeta,
                    u'language_id')
                if not language_id:
                    language_id = self.newbibles[number].get_language()
                if not language_id:
                    log.exception(u'Importing books from "%s" '\
                        'failed' % name)
                    delete_database(self.path, 
                        clean_filename(self.newbibles[number].get_name()))
                    del self.newbibles[number]
                    self.incrementProgressBar(unicode(translate(
                        'BiblesPlugin.UpgradeWizardForm', 
                        'Upgrading Bible %s of %s: "%s"\nFailed')) % 
                        (number+1, self.maxBibles, name), 
                        self.progressBar.maximum()-self.progressBar.value())
                    number += 1
                    continue
                books = oldbible.get_books()
                self.progressBar.setMaximum(len(books))
                for book in books:
                    if self.stop_import_flag:
                        break
                    self.incrementProgressBar(unicode(translate(
                        'BiblesPlugin.UpgradeWizardForm', 
                        'Upgrading Bible %s of %s: "%s"\n'
                        'Importing %s ...')) % 
                        (number+1, self.maxBibles, name, book[u'name']))
                    book_ref_id = self.newbibles[number].\
                        get_book_ref_id_by_name(book[u'name'], len(books), 
                        language_id)
                    if not book_ref_id:
                        log.exception(u'Importing books from %s " '\
                            'failed - aborted by user' % name)
                        delete_database(self.path, 
                            clean_filename(self.newbibles[number].get_name()))
                        del self.newbibles[number]
                        bible_failed = True
                        break
                    book_details = BiblesResourcesDB.get_book_by_id(book_ref_id)
                    db_book = self.newbibles[number].create_book(book[u'name'],
                        book_ref_id, book_details[u'testament_id'])
                    verses = oldbible.get_verses(book[u'id'])
                    if not verses:
                        log.exception(u'No verses found to import for book '
                            u'"%s"', book[u'name'])
                        self.newbibles[number].delete_book(db_book)
                        continue
                    for verse in verses:
                        self.newbibles[number].create_verse(db_book.id, 
                            int(verse[u'chapter']), 
                            int(verse[u'verse']), unicode(verse[u'text']))
                        Receiver.send_message(u'openlp_process_events')
                self.newbibles[number].session.commit()
            if not bible_failed:
                self.incrementProgressBar(unicode(translate(
                    'BiblesPlugin.UpgradeWizardForm', 
                    'Upgrading Bible %s of %s: "%s"\n'
                    'Done')) % 
                    (number+1, self.maxBibles, name))
                self.success[biblenumber] = True
            else:
                self.incrementProgressBar(unicode(translate(
                    'BiblesPlugin.UpgradeWizardForm', 
                    'Upgrading Bible %s of %s: "%s"\nFailed')) % 
                    (number+1, self.maxBibles, name), 
                    self.progressBar.maximum()-self.progressBar.value())
            number += 1
        self.mediaItem.reloadBibles()
        successful_import = 0
        failed_import = 0
        for number, success in self.success.iteritems():
            if success == True:
                successful_import += 1
            elif success == False and self.checkBox[number].checkState() == \
                QtCore.Qt.Checked:
                failed_import += 1
        if failed_import > 0:
            failed_import_text = unicode(translate(
                'BiblesPlugin.UpgradeWizardForm', 
                ' - %s upgrade fail')) % failed_import
        else:
            failed_import_text = u''
        if successful_import > 0:
            if include_webbible:
                self.progressLabel.setText(unicode(
                    translate('BiblesPlugin.UpgradeWizardForm', 'Upgrade %s '
                    'Bible(s) successful%s.\nPlease note, that verses from '
                    'Web Bibles will be downloaded\non demand and so an '
                    'Internet connection is required.')) % 
                    (successful_import, failed_import_text))
            else:
                self.progressLabel.setText(unicode(
                    translate('BiblesPlugin.UpgradeWizardForm', 'Upgrade %s '
                    'Bible(s) successful.%s')) % (successful_import, 
                    failed_import_text))
        else:
            self.progressLabel.setText(
                    translate('BiblesPlugin.UpgradeWizardForm', 'Upgrade '
                    'failed.'))
