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
The :mod:`projector.projectorwizard` module handles the GUI Wizard for adding
    new projetor entries.
"""

import logging
log = logging.getLogger(__name__)
log.debug('projectorwizard loaded')

from ipaddress import IPv4Address, IPv6Address, AddressValueError

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot, pyqtSignal

from openlp.core.common import Registry, RegistryProperties, translate
from openlp.core.lib import build_icon

from openlp.core.common import verify_ip_address
from openlp.core.lib.projector.db import ProjectorDB, Projector
from openlp.core.lib.projector.pjlink1 import PJLink1
from openlp.core.lib.projector.constants import *

PAGE_COUNT = 4
(ConnectWelcome,
 ConnectHost,
 ConnectEdit,
 ConnectFinish) = range(PAGE_COUNT)

PAGE_NEXT = {ConnectWelcome: ConnectHost,
             ConnectHost: ConnectEdit,
             ConnectEdit: ConnectFinish,
             ConnectFinish: -1}


class ProjectorWizard(QtGui.QWizard, RegistryProperties):
    """
    Wizard for adding/editing projector entries.
    """
    def __init__(self, parent, projectordb):
        log.debug('__init__()')
        super().__init__(parent)
        self.db = projectordb
        self.projector = None
        self.setObjectName('projector_wizard')
        self.setWindowIcon(build_icon(u':/icon/openlp-logo.svg'))
        self.setModal(True)
        if is_macosx():
            self.setPixmap(QtGui.QWizard.BackgroundPixmap, QtGui.QPixmap(':/wizards/openlp-osx-wizard.png'))
        else:
            self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.setMinimumSize(650, 550)
        self.setOption(QtGui.QWizard.NoBackButtonOnStartPage)
        self.spacer = QtGui.QSpacerItem(10, 0,
                                        QtGui.QSizePolicy.Fixed,
                                        QtGui.QSizePolicy.Minimum)
        self.setOption(self.HaveHelpButton, True)
        self.welcome_page = ConnectWelcomePage(self, ConnectWelcome)
        self.host_page = ConnectHostPage(self, ConnectHost)
        self.edit_page = ConnectEditPage(self, ConnectEdit)
        self.finish_page = ConnectFinishPage(self, ConnectFinish)
        self.setPage(self.welcome_page.pageId, self.welcome_page)
        self.setPage(self.host_page.pageId, self.host_page)
        self.setPage(self.edit_page.pageId, self.edit_page)
        self.setPage(self.finish_page.pageId, self.finish_page)
        self.registerFields()
        self.retranslateUi()
        # Connect signals
        self.button(QtGui.QWizard.HelpButton).clicked.connect(self.showHelp)
        log.debug('ProjectorWizard() started')

    def exec_(self, projector=None):
        """
        Override function to determine whether we are called to add a new
        projector or edit an old projector.

        :param projector: Projector instance
        :returns: None
        """
        self.projector = projector
        if self.projector is None:
            log.debug('ProjectorWizard() Adding new projector')
            self.setWindowTitle(translate('OpenLP.ProjectorWizard',
                                          'New Projector Wizard'))
            self.setStartId(ConnectWelcome)
            self.restart()
        else:
            log.debug('ProjectorWizard() Editing existing projector')
            self.setWindowTitle(translate('OpenLP.ProjectorWizard',
                                          'Edit Projector Wizard'))
            self.setStartId(ConnectEdit)
            self.restart()
        saved = QtGui.QWizard.exec_(self)
        self.projector = None
        return saved

    def registerFields(self):
        """
        Register selected fields for use by all pages.
        """
        self.host_page.registerField('ip_number*', self.host_page.ip_number_text)
        self.edit_page.registerField('pjlink_port', self.host_page.pjlink_port_text)
        self.edit_page.registerField('pjlink_pin', self.host_page.pjlink_pin_text)
        self.edit_page.registerField('projector_name*', self.edit_page.name_text)
        self.edit_page.registerField('projector_location', self.edit_page.location_text)
        self.edit_page.registerField('projector_notes', self.edit_page.notes_text, 'plainText')
        self.edit_page.registerField('projector_make', self.host_page.manufacturer_text)
        self.edit_page.registerField('projector_model', self.host_page.model_text)

    @pyqtSlot()
    def showHelp(self):
        """
        Show the pop-up help message.
        """
        page = self.currentPage()
        try:
            help_page = page.help_
        except:
            help_page = self.no_help
        QtGui.QMessageBox.information(self, self.title_help, help_page)

    def retranslateUi(self):
        """
        Fixed-text strings used for translations
        """
        self.title_help = translate('OpenLP.ProjectorWizard', 'Projector Wizard Help')
        self.no_help = translate('OpenLP.ProjectorWizard',
                                 'Sorry - no help available for this page.')
        self.welcome_page.title_label.setText('<span style=\'font-size:14pt; font-weight:600;\'>%s</span>' %
                                              translate('OpenLP.ProjectorWizard',
                                                        'Welcome to the<br />Projector Wizard'))
        self.welcome_page.information_label.setText(translate('OpenLP.ProjectorWizard', 'This wizard will help you to '
                                                              'create and edit your Projector control. <br /><br />'
                                                              'Press "Next" button below to continue.'))
        self.host_page.setTitle(translate('OpenLP.ProjectorWizard', 'Host IP Number'))
        self.host_page.setSubTitle(translate('OpenLP.ProjectorWizard',
                                             'Enter the IP address, port, and PIN used to conenct to the projector. '
                                             'The port should only be changed if you know what you\'re doing, and '
                                             'the pin should only be entered if it\'s required.'
                                             '<br /><br />Once the IP address is checked and is '
                                             'not in the database, you can continue to the next page'))
        self.host_page.help_ = translate('OpenLP.ProjectorWizard',
                                         '<b>IP</b>: The IP address of the projector to connect to.<br />'
                                         '<b>Port</b>: The port number. Default is 4352.<br />'
                                         '<b>PIN</b>: If needed, enter the PIN access code for the projector.<br />'
                                         '<br />Once I verify the address is a valid IP and not in the database, you '
                                         'can then add the rest of the information on the next page.')
        self.host_page.ip_number_label.setText(translate('OpenLP.ProjectorWizard', 'IP Number: '))
        self.host_page.pjlink_port_label.setText(translate('OpenLP.ProjectorWizard', 'Port: '))
        self.host_page.pjlink_pin_label.setText(translate('OpenLP.ProjectorWizard', 'PIN: '))
        self.edit_page.setTitle(translate('OpenLP.ProjectorWizard', 'Add/Edit Projector Information'))
        self.edit_page.setSubTitle(translate('OpenLP.ProjectorWizard',
                                             'Enter the information below in the left panel for the projector.'))
        self.edit_page.help_ = translate('OpenLP.ProjectorWizard',
                                         'Please enter the following information:'
                                         '<br /><br /><b>PJLink Port</b>: The network port to use. Default is %s.'
                                         '<br /><br /><b>PJLink PIN</b>: The PJLink access PIN. Only required if '
                                         'PJLink PIN is set in projector. 4 characters max. <br /><br /><b>Name</b>: '
                                         'A unique name you want to give to this projector entry. 20 characters max. '
                                         '<br /><br /><b>Location</b>: The location of the projector. 30 characters '
                                         'max.<br /><br /><b>Notes</b>: Any notes you want to add about this '
                                         'projector. 200 characters max.<br /><br />The "Manufacturer" and "Model" '
                                         'information will only be available if the projector is connected to the '
                                         'network and can be accessed while running this wizard. '
                                         '(Currently not implemented)' % PJLINK_PORT)
        self.edit_page.ip_number_label.setText(translate('OpenLP.ProjectorWizard', 'IP Number: '))
        self.edit_page.pjlink_port_label.setText(translate('OpenLP.ProjectorWizard', 'PJLink port: '))
        self.edit_page.pjlink_pin_label.setText(translate('OpenLP.ProjectorWizard', 'PJLink PIN: '))
        self.edit_page.name_label.setText(translate('OpenLP.ProjectorWizard', 'Name: '))
        self.edit_page.location_label.setText(translate('OpenLP.ProjectorWizard', 'Location: '))
        self.edit_page.notes_label.setText(translate('OpenLP.ProjectorWizard', 'Notes: '))
        self.edit_page.projector_make_label.setText(translate('OpenLP.ProjectorWizard', 'Manufacturer: '))
        self.edit_page.projector_model_label.setText(translate('OpenLP.ProjectorWizard', 'Model: '))
        self.finish_page.title_label.setText('<span style=\'font-size:14pt; font-weight:600;\'>%s</span>' %
                                             translate('OpenLP.ProjectorWizard', 'Projector Added'))
        self.finish_page.information_label.setText(translate('OpenLP.ProjectorWizard',
                                                   '<br />Have fun with your new projector.'))


class ConnectBase(QtGui.QWizardPage):
    """
    Base class for the projector wizard pages.
    """
    def __init__(self, parent=None, page=None):
        super().__init__(parent)
        self.pageId = page

    def nextId(self):
        """
        Returns next page to show.
        """
        return PAGE_NEXT[self.pageId]

    def setVisible(self, visible):
        """
        Set buttons for bottom of page.
        """
        QtGui.QWizardPage.setVisible(self, visible)
        if visible:
            try:
                self.myCustomButton()
            except:
                try:
                    self.wizard().setButtonLayout(self.myButtons)
                except:
                    self.wizard().setButtonLayout([QtGui.QWizard.Stretch,
                                                   QtGui.QWizard.BackButton,
                                                   QtGui.QWizard.NextButton,
                                                   QtGui.QWizard.CancelButton])


class ConnectWelcomePage(ConnectBase):
    """
    Splash screen
    """
    def __init__(self, parent, page):
        super().__init__(parent, page)
        if is_macosx():
            self.setPixmap(QtGui.QWizard.BackgroundPixmap, QtGui.QPixmap(':/wizards/openlp-osx-wizard.png'))
        else:
            self.setPixmap(QtGui.QWizard.WatermarkPixmap,
                        QtGui.QPixmap(':/wizards/wizard_createprojector.png'))
        self.setObjectName('welcome_page')
        self.myButtons = [QtGui.QWizard.Stretch,
                          QtGui.QWizard.NextButton]
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setObjectName('layout')
        self.title_label = QtGui.QLabel(self)
        self.title_label.setObjectName('title_label')
        self.layout.addWidget(self.title_label)
        self.layout.addSpacing(40)
        self.information_label = QtGui.QLabel(self)
        self.information_label.setWordWrap(True)
        self.information_label.setObjectName('information_label')
        self.layout.addWidget(self.information_label)
        self.layout.addStretch()


class ConnectHostPage(ConnectBase):
    """
    Get initial information.
    """
    def __init__(self, parent, page):
        super().__init__(parent, page)
        self.setObjectName('host_page')
        self.myButtons = [QtGui.QWizard.HelpButton,
                          QtGui.QWizard.Stretch,
                          QtGui.QWizard.BackButton,
                          QtGui.QWizard.NextButton,
                          QtGui.QWizard.CancelButton]
        self.hostPageLayout = QtGui.QHBoxLayout(self)
        self.hostPageLayout.setObjectName('layout')
        # Projector DB information
        self.localAreaBox = QtGui.QGroupBox(self)
        self.localAreaBox.setObjectName('host_local_area_box')
        self.localAreaForm = QtGui.QFormLayout(self.localAreaBox)
        self.localAreaForm.setObjectName('host_local_area_form')
        self.ip_number_label = QtGui.QLabel(self.localAreaBox)
        self.ip_number_label.setObjectName('host_ip_number_label')
        self.ip_number_text = QtGui.QLineEdit(self.localAreaBox)
        self.ip_number_text.setObjectName('host_ip_number_text')
        self.localAreaForm.addRow(self.ip_number_label, self.ip_number_text)
        self.pjlink_port_label = QtGui.QLabel(self.localAreaBox)
        self.pjlink_port_label.setObjectName('host_pjlink_port_label')
        self.pjlink_port_text = QtGui.QLineEdit(self.localAreaBox)
        self.pjlink_port_text.setMaxLength(5)
        self.pjlink_port_text.setText(str(PJLINK_PORT))
        self.pjlink_port_text.setObjectName('host_pjlink_port_text')
        self.localAreaForm.addRow(self.pjlink_port_label, self.pjlink_port_text)
        self.pjlink_pin_label = QtGui.QLabel(self.localAreaBox)
        self.pjlink_pin_label.setObjectName('host_pjlink_pin_label')
        self.pjlink_pin_text = QtGui.QLineEdit(self.localAreaBox)
        self.pjlink_pin_text.setObjectName('host_pjlink_pin_text')
        self.localAreaForm.addRow(self.pjlink_pin_label, self.pjlink_pin_text)
        self.hostPageLayout.addWidget(self.localAreaBox)
        self.manufacturer_text = QtGui.QLineEdit(self)
        self.manufacturer_text.setVisible(False)
        self.model_text = QtGui.QLineEdit(self)
        self.model_text.setVisible(False)

    def validatePage(self):
        """
        Validate IP number/FQDN before continuing to next page.
        """
        adx = self.wizard().field('ip_number')
        port = self.wizard().field('pjlink_port')
        pin = self.wizard().field('pjlink_pin')
        log.debug('ip="%s" port="%s" pin="%s"' % (adx, port, pin))
        valid = verify_ip_address(adx)
        if valid:
            ip = self.wizard().db.get_projector_by_ip(adx)
            if ip is None:
                valid = True
            else:
                QtGui.QMessageBox.warning(self,
                                          translate('OpenLP.ProjectorWizard', 'Already Saved'),
                                          translate('OpenLP.ProjectorWizard',
                                                    'IP "%s"<br />is already in the database as ID %s.'
                                                    '<br /><br />Please Enter a different IP.' % (adx, ip.id)))
                valid = False
        else:
            QtGui.QMessageBox.warning(self,
                                      translate('OpenLP.ProjectorWizard', 'Invalid IP'),
                                      translate('OpenLP.ProjectorWizard',
                                                'IP "%s"<br>is not a valid IP address.'
                                                '<br /><br />Please enter a valid IP address.' % adx))
            valid = False
        """
        FIXME - Future plan to retrieve manufacture/model input source information. Not implemented yet.
        new = PJLink(host=adx, port=port, pin=pin if pin.strip() != '' else None)
        if new.connect():
            mfg = new.get_manufacturer()
            log.debug('Setting manufacturer_text to %s' % mfg)
            self.manufacturer_text.setText(mfg)
            model = new.get_model()
            log.debug('Setting model_text to %s' % model)
            self.model_text.setText(model)
        else:
            if new.status_error == E_AUTHENTICATION:
                QtGui.QMessageBox.warning(self,
                                          translate('OpenLP.ProjectorWizard', 'Requires Authorization'),
                                          translate('OpenLP.ProjectorWizard',
                                                    'Projector requires authorization and either PIN not set '
                                                    'or invalid PIN set.'
                                                    '<br />Enter a valid PIN before hitting "NEXT"')
                                          )
            elif new.status_error == E_NO_AUTHENTICATION:
                QtGui.QMessageBox.warning(self,
                                          translate('OpenLP.ProjectorWizard', 'No Authorization Required'),
                                          translate('OpenLP.ProjectorWizard',
                                                    'Projector does not require authorization and PIN set.'
                                                    '<br />Remove PIN entry before hitting "NEXT"')
                                          )
            valid = False
        new.disconnect()
        del(new)
        """
        return valid


class ConnectEditPage(ConnectBase):
    """
    Full information page.
    """
    newProjector = QtCore.pyqtSignal(str)
    editProjector = QtCore.pyqtSignal(object)

    def __init__(self, parent, page):
        super().__init__(parent, page)
        self.setObjectName('edit_page')
        self.editPageLayout = QtGui.QHBoxLayout(self)
        self.editPageLayout.setObjectName('layout')
        # Projector DB information
        self.localAreaBox = QtGui.QGroupBox(self)
        self.localAreaBox.setObjectName('edit_local_area_box')
        self.localAreaForm = QtGui.QFormLayout(self.localAreaBox)
        self.localAreaForm.setObjectName('edit_local_area_form')
        self.ip_number_label = QtGui.QLabel(self.localAreaBox)
        self.ip_number_label.setObjectName('edit_ip_number_label')
        self.ip_number_text = QtGui.QLineEdit(self.localAreaBox)
        self.ip_number_text.setObjectName('edit_ip_number_text')
        self.localAreaForm.addRow(self.ip_number_label, self.ip_number_text)
        self.pjlink_port_label = QtGui.QLabel(self.localAreaBox)
        self.pjlink_port_label.setObjectName('edit_pjlink_port_label')
        self.pjlink_port_text = QtGui.QLineEdit(self.localAreaBox)
        self.pjlink_port_text.setMaxLength(5)
        self.pjlink_port_text.setObjectName('edit_pjlink_port_text')
        self.localAreaForm.addRow(self.pjlink_port_label, self.pjlink_port_text)
        self.pjlink_pin_label = QtGui.QLabel(self.localAreaBox)
        self.pjlink_pin_label.setObjectName('pjlink_pin_label')
        self.pjlink_pin_text = QtGui.QLineEdit(self.localAreaBox)
        self.pjlink_pin_text.setObjectName('pjlink_pin_text')
        self.localAreaForm.addRow(self.pjlink_pin_label, self.pjlink_pin_text)
        self.name_label = QtGui.QLabel(self.localAreaBox)
        self.name_label.setObjectName('name_label')
        self.name_text = QtGui.QLineEdit(self.localAreaBox)
        self.name_text.setObjectName('name_label')
        self.name_text.setMaxLength(20)
        self.localAreaForm.addRow(self.name_label, self.name_text)
        self.location_label = QtGui.QLabel(self.localAreaBox)
        self.location_label.setObjectName('location_label')
        self.location_text = QtGui.QLineEdit(self.localAreaBox)
        self.location_text.setObjectName('location_text')
        self.location_text.setMaxLength(30)
        self.localAreaForm.addRow(self.location_label, self.location_text)
        self.notes_label = QtGui.QLabel(self.localAreaBox)
        self.notes_label.setObjectName('notes_label')
        self.notes_text = QtGui.QPlainTextEdit(self.localAreaBox)
        self.notes_text.setObjectName('notes_text')
        self.localAreaForm.addRow(self.notes_label, self.notes_text)
        self.editPageLayout.addWidget(self.localAreaBox)
        # Projector retrieved information
        self.remoteAreaBox = QtGui.QGroupBox(self)
        self.remoteAreaBox.setObjectName('edit_remote_area_box')
        self.remoteAreaForm = QtGui.QFormLayout(self.remoteAreaBox)
        self.remoteAreaForm.setObjectName('edit_remote_area_form')
        self.projector_make_label = QtGui.QLabel(self.remoteAreaBox)
        self.projector_make_label.setObjectName('projector_make_label')
        self.projector_make_text = QtGui.QLabel(self.remoteAreaBox)
        self.projector_make_text.setObjectName('projector_make_text')
        self.remoteAreaForm.addRow(self.projector_make_label, self.projector_make_text)
        self.projector_model_label = QtGui.QLabel(self.remoteAreaBox)
        self.projector_model_label.setObjectName('projector_model_text')
        self.projector_model_text = QtGui.QLabel(self.remoteAreaBox)
        self.projector_model_text.setObjectName('projector_model_text')
        self.remoteAreaForm.addRow(self.projector_model_label, self.projector_model_text)
        self.editPageLayout.addWidget(self.remoteAreaBox)

    def initializePage(self):
        """
        Fill in the blanks for information from previous page/projector to edit.
        """
        if self.wizard().projector is not None:
            log.debug('ConnectEditPage.initializePage()  Editing existing projector')
            self.ip_number_text.setText(self.wizard().projector.ip)
            self.pjlink_port_text.setText(str(self.wizard().projector.port))
            self.pjlink_pin_text.setText(self.wizard().projector.pin)
            self.name_text.setText(self.wizard().projector.name)
            self.location_text.setText(self.wizard().projector.location)
            self.notes_text.insertPlainText(self.wizard().projector.notes)
            self.myButtons = [QtGui.QWizard.HelpButton,
                              QtGui.QWizard.Stretch,
                              QtGui.QWizard.FinishButton,
                              QtGui.QWizard.CancelButton]
        else:
            log.debug('Retrieving information from host page')
            self.ip_number_text.setText(self.wizard().field('ip_number'))
            self.pjlink_port_text.setText(self.wizard().field('pjlink_port'))
            self.pjlink_pin_text.setText(self.wizard().field('pjlink_pin'))
            make = self.wizard().field('projector_make')
            model = self.wizard().field('projector_model')
            if make is None or make.strip() == '':
                self.projector_make_text.setText('Unavailable           ')
            else:
                self.projector_make_text.setText(make)
            if model is None or model.strip() == '':
                self.projector_model_text.setText('Unavailable           ')
            else:
                self.projector_model_text.setText(model)
            self.myButtons = [QtGui.QWizard.HelpButton,
                              QtGui.QWizard.Stretch,
                              QtGui.QWizard.BackButton,
                              QtGui.QWizard.NextButton,
                              QtGui.QWizard.CancelButton]

    def validatePage(self):
        """
        Last verification if editiing existing entry in case of IP change. Add entry to DB.
        """
        log.debug('ConnectEditPage().validatePage()')
        if self.wizard().projector is not None:
            ip = self.ip_number_text.text()
            port = self.pjlink_port_text.text()
            name = self.name_text.text()
            location = self.location_text.text()
            notes = self.notes_text.toPlainText()
            pin = self.pjlink_pin_text.text()
            log.debug('edit-page() Verifying info : ip="%s"' % ip)
            valid = verify_ip_address(ip)
            if not valid:
                QtGui.QMessageBox.warning(self,
                                          translate('OpenLP.ProjectorWizard', 'Invalid IP'),
                                          translate('OpenLP.ProjectorWizard',
                                                    'IP "%s"<br>is not a valid IP address.'
                                                    '<br /><br />Please enter a valid IP address.' % ip))
                return False
            log.debug('Saving edited projector %s' % ip)
            self.wizard().projector.ip = ip
            self.wizard().projector.port = port
            self.wizard().projector.name = name
            self.wizard().projector.location = location
            self.wizard().projector.notes = notes
            self.wizard().projector.pin = pin
            saved = self.wizard().db.update_projector(self.wizard().projector)
            if not saved:
                QtGui.QMessageBox.error(self, translate('OpenLP.ProjectorWizard', 'Database Error'),
                                        translate('OpenLP.ProjectorWizard', 'There was an error saving projector '
                                                  'information. See the log for the error'))
                return False
            self.editProjector.emit(self.wizard().projector)
        else:
            projector = Projector(ip=self.wizard().field('ip_number'),
                                  port=self.wizard().field('pjlink_port'),
                                  name=self.wizard().field('projector_name'),
                                  location=self.wizard().field('projector_location'),
                                  notes=self.wizard().field('projector_notes'),
                                  pin=self.wizard().field('pjlink_pin'))
            log.debug('Adding new projector %s' % projector.ip)
            if self.wizard().db.get_projector_by_ip(projector.ip) is None:
                saved = self.wizard().db.add_projector(projector)
                if not saved:
                    QtGui.QMessageBox.error(self, translate('OpenLP.ProjectorWizard', 'Database Error'),
                                            translate('OpenLP.ProjectorWizard', 'There was an error saving projector '
                                                      'information. See the log for the error'))
                    return False
                self.newProjector.emit('%s' % projector.ip)
        return True

    def nextId(self):
        """
        Returns the next page ID if new entry or end of wizard if editing entry.
        """
        if self.wizard().projector is None:
            return PAGE_NEXT[self.pageId]
        else:
            return -1


class ConnectFinishPage(ConnectBase):
    """
    Buh-Bye page
    """
    def __init__(self, parent, page):
        super().__init__(parent, page)
        self.setObjectName('connect_finish_page')
        if is_macosx():
            self.setPixmap(QtGui.QWizard.BackgroundPixmap, QtGui.QPixmap(':/wizards/openlp-osx-wizard.png'))
        else:
            self.setPixmap(QtGui.QWizard.WatermarkPixmap, QtGui.QPixmap(':/wizards/wizard_createprojector.png'))
        self.myButtons = [QtGui.QWizard.Stretch,
                          QtGui.QWizard.FinishButton]
        self.isFinalPage()
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setObjectName('layout')
        self.title_label = QtGui.QLabel(self)
        self.title_label.setObjectName('title_label')
        self.layout.addWidget(self.title_label)
        self.layout.addSpacing(40)
        self.information_label = QtGui.QLabel(self)
        self.information_label.setWordWrap(True)
        self.information_label.setObjectName('information_label')
        self.layout.addWidget(self.information_label)
        self.layout.addStretch()
