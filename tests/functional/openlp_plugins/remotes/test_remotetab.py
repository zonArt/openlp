"""
This module contains tests for the lib submodule of the Remotes plugin.
"""
import os

from unittest import TestCase
from tempfile import mkstemp
from mock import patch

from openlp.core.lib import Settings
from openlp.plugins.remotes.lib.remotetab import RemoteTab

from PyQt4 import QtGui

__default_settings__ = {
    u'remotes/twelve hour': True,
    u'remotes/port': 4316,
    u'remotes/https port': 4317,
    u'remotes/https enabled': False,
    u'remotes/user id': u'openlp',
    u'remotes/password': u'password',
    u'remotes/authentication enabled': False,
    u'remotes/ip address': u'0.0.0.0'
}

ZERO_URL = u'0.0.0.0'

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'..', u'..', u'..', u'resources'))


class TestRemoteTab(TestCase):
    """
    Test the functions in the :mod:`lib` module.
    """
    def setUp(self):
        """
        Create the UI
        """
        fd, self.ini_file = mkstemp(u'.ini')
        Settings().set_filename(self.ini_file)
        self.application = QtGui.QApplication.instance()
        Settings().extend_default_settings(__default_settings__)
        self.parent = QtGui.QMainWindow()
        self.form = RemoteTab(self.parent, u'Remotes', None, None)

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.application
        del self.parent
        del self.form
        os.unlink(self.ini_file)

    def set_basic_urls_test(self):
        """
        Test the set_urls function with standard defaults
        """
        # GIVEN: A mocked location
        with patch(u'openlp.core.utils.applocation.Settings') as mocked_class, \
            patch(u'openlp.core.utils.AppLocation.get_directory') as mocked_get_directory, \
            patch(u'openlp.core.utils.applocation.check_directory_exists') as mocked_check_directory_exists, \
            patch(u'openlp.core.utils.applocation.os') as mocked_os:
            # GIVEN: A mocked out Settings class and a mocked out AppLocation.get_directory()
            mocked_settings = mocked_class.return_value
            mocked_settings.contains.return_value = False
            mocked_get_directory.return_value = u'test/dir'
            mocked_check_directory_exists.return_value = True
            mocked_os.path.normpath.return_value = u'test/dir'

            # WHEN: when the set_urls is called having reloaded the form.
            self.form.load()
            self.form.set_urls()
            # THEN: the following screen values should be set
            self.assertEqual(self.form.address_edit.text(), ZERO_URL, u'The default URL should be set on the screen')
            self.assertEqual(self.form.https_settings_group_box.isEnabled(), False,
                            u'The Https box should not be enabled')
            self.assertEqual(self.form.https_settings_group_box.isChecked(), False,
                             u'The Https checked box should note be Checked')
            self.assertEqual(self.form.user_login_group_box.isChecked(), False,
                             u'The authentication box should not be enabled')

    def set_certificate_urls_test(self):
        """
        Test the set_urls function with certificate available
        """
        # GIVEN: A mocked location
        with patch(u'openlp.core.utils.applocation.Settings') as mocked_class, \
            patch(u'openlp.core.utils.AppLocation.get_directory') as mocked_get_directory, \
            patch(u'openlp.core.utils.applocation.check_directory_exists') as mocked_check_directory_exists, \
            patch(u'openlp.core.utils.applocation.os') as mocked_os:
            # GIVEN: A mocked out Settings class and a mocked out AppLocation.get_directory()
            mocked_settings = mocked_class.return_value
            mocked_settings.contains.return_value = False
            mocked_get_directory.return_value = TEST_PATH
            mocked_check_directory_exists.return_value = True
            mocked_os.path.normpath.return_value = TEST_PATH

            # WHEN: when the set_urls is called having reloaded the form.
            self.form.load()
            self.form.set_urls()
            # THEN: the following screen values should be set
            self.assertEqual(self.form.http_settings_group_box.isEnabled(), True,
                             u'The Http group box should be enabled')
            self.assertEqual(self.form.https_settings_group_box.isChecked(), False,
                             u'The Https checked box should be Checked')
            self.assertEqual(self.form.https_settings_group_box.isEnabled(), True,
                             u'The Https box should be enabled')
