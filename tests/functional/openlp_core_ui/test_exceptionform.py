# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
Package to test the openlp.core.ui.exeptionform package.
"""

import os
import socket
import tempfile
import urllib
from unittest import TestCase
from unittest.mock import mock_open

from PyQt5.QtCore import QUrlQuery

from openlp.core.common import Registry
from openlp.core.ui.firsttimeform import FirstTimeForm

from tests.functional import MagicMock, patch
from tests.helpers.testmixin import TestMixin

from openlp.core.ui import exceptionform

exceptionform.WEBKIT_VERSION = 'Webkit Test'
exceptionform.MIGRATE_VERSION = 'Migrate Test'
exceptionform.CHARDET_VERSION = 'CHARDET Test'
exceptionform.ENCHANT_VERSION = 'Enchant Test'
exceptionform.MAKO_VERSION = 'Mako Test'
exceptionform.ICU_VERSION = 'ICU Test'
exceptionform.VLC_VERSION = 'VLC Test'

MAIL_ITEM_TEXT = ('**OpenLP Bug Report**\nVersion: Trunk Test\n\n--- Details of the Exception. ---\n\n'
                  'Description Test\n\n --- Exception Traceback ---\nopenlp: Traceback Test\n'
                  '--- System information ---\nPlatform: Nose Test\n\n--- Library Versions ---\n'
                  'Python: Python Test\nQt5: Qt5 test\nPyQt5: PyQT5 Test\nQtWebkit: Webkit Test\n'
                  'SQLAlchemy: SqlAlchemy Test\nSQLAlchemy Migrate: Migrate Test\nBeautifulSoup: BeautifulSoup Test\n'
                  'lxml: ETree Test\nChardet: CHARDET Test\nPyEnchant: Enchant Test\nMako: Mako Test\n'
                  'pyICU: ICU Test\npyUNO bridge: UNO Bridge Test\nVLC: VLC Test\n\n')


class TestExceptionForm(TestMixin, TestCase):
    """
    Test functionality of exception form functions
    """
    def setUp(self):
        self.setup_application()
        self.app.setApplicationVersion('0.0')
        # Set up a fake "set_normal_cursor" method since we're not dealing with an actual OpenLP application object
        self.app.set_normal_cursor = lambda: None
        self.app.process_events = lambda: None
        Registry.create()
        Registry().register('application', self.app)
        self.tempfile = os.path.join(tempfile.gettempdir(), 'testfile')

    def tearDown(self):
        if os.path.isfile(self.tempfile):
            os.remove(self.tempfile)

    @patch("openlp.core.ui.exceptionform.get_application_version")
    @patch("openlp.core.ui.exceptionform.Ui_ExceptionDialog")
    @patch("openlp.core.ui.exceptionform.QtWidgets.QFileDialog")
    @patch("openlp.core.ui.exceptionform.QtCore.QUrl")
    @patch("openlp.core.ui.exceptionform.QtCore.QUrlQuery.addQueryItem")
    @patch("openlp.core.ui.exceptionform.QtGui.QDesktopServices.openUrl")
    @patch("openlp.core.ui.exceptionform.is_linux")
    @patch("openlp.core.ui.exceptionform.platform.python_version")
    @patch("openlp.core.ui.exceptionform.platform.platform")
    @patch("openlp.core.ui.exceptionform.Qt.qVersion")
    @patch("openlp.core.ui.exceptionform.Qt")
    @patch("openlp.core.ui.exceptionform.sqlalchemy")
    @patch("openlp.core.ui.exceptionform.bs4")
    @patch("openlp.core.ui.exceptionform.etree")
    def test_on_send_report_button_clicked(self,
                                           mocked_etree,
                                           mocked_bs4,
                                           mocked_sqlalchemy,
                                           mocked_pyqt,
                                           mocked_qversion,
                                           mocked_platform,
                                           mocked_python_version,
                                           mocked_is_linux,
                                           mocked_openlurl,
                                           mocked_qurlquery,
                                           mocked_qurl,
                                           mocked_file_dialog,
                                           mocked_ui_exception_dialog,
                                           mocked_application_version):
        """
        Test on_send_report_button_clicked creates the proper system information text
        """
        # GIVEN: Test environment
        mocked_etree.__version__ = 'ETree Test'
        mocked_bs4.__version__ = 'BeautifulSoup Test'
        mocked_sqlalchemy.__version__ = 'SqlAlchemy Test'
        mocked_pyqt.PYQT_VERSION_STR = 'PyQT5 Test'
        mocked_python_version.return_value = 'Python Test'
        mocked_platform.return_value = 'Nose Test'
        mocked_qversion.return_value = 'Qt5 test'
        mocked_is_linux.return_value = False
        mocked_application_version.return_value = 'Trunk Test'
        test_form = exceptionform.ExceptionForm()
        test_form.file_attachment = None
        with patch.object(test_form, '_pyuno_import') as mock_pyuno:
            with patch.object(test_form.exception_text_edit, 'toPlainText') as mock_traceback:
                with patch.object(test_form.description_text_edit, 'toPlainText') as mock_description:
                    mock_pyuno.return_value = 'UNO Bridge Test'
                    mock_traceback.return_value = 'openlp: Traceback Test'
                    mock_description.return_value = 'Description Test'

                    # WHEN: on_save_report_button_clicked called
                    test_form.on_send_report_button_clicked()

        # THEN: Verify strings were fomratted properly
        mocked_qurlquery.assert_called_with('body', MAIL_ITEM_TEXT)
