import logging
import os
import platform
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from distutils.version import LooseVersion
from subprocess import Popen, PIPE

from openlp.core.common import AppLocation, Settings

from PyQt5 import QtCore

log = logging.getLogger(__name__)

APPLICATION_VERSION = {}
CONNECTION_TIMEOUT = 30
CONNECTION_RETRIES = 2


class VersionThread(QtCore.QThread):
    """
    A special Qt thread class to fetch the version of OpenLP from the website.
    This is threaded so that it doesn't affect the loading time of OpenLP.
    """
    def __init__(self, main_window):
        """
        Constructor for the thread class.

        :param main_window: The main window Object.
        """
        log.debug("VersionThread - Initialise")
        super(VersionThread, self).__init__(None)
        self.main_window = main_window

    def run(self):
        """
        Run the thread.
        """
        self.sleep(1)
        log.debug('Version thread - run')
        app_version = get_application_version()
        version = check_latest_version(app_version)
        log.debug("Versions {version1} and {version2} ".format(version1=LooseVersion(str(version)),
                                                               version2=LooseVersion(str(app_version['full']))))
        if LooseVersion(str(version)) > LooseVersion(str(app_version['full'])):
            self.main_window.openlp_version_check.emit('{version}'.format(version=version))


def get_application_version():
    """
    Returns the application version of the running instance of OpenLP::

        {'full': '1.9.4-bzr1249', 'version': '1.9.4', 'build': 'bzr1249'}
    """
    global APPLICATION_VERSION
    if APPLICATION_VERSION:
        return APPLICATION_VERSION
    if '--dev-version' in sys.argv or '-d' in sys.argv:
        # NOTE: The following code is a duplicate of the code in setup.py. Any fix applied here should also be applied
        # there.

        # Get the revision of this tree.
        bzr = Popen(('bzr', 'revno'), stdout=PIPE)
        tree_revision, error = bzr.communicate()
        tree_revision = tree_revision.decode()
        code = bzr.wait()
        if code != 0:
            raise Exception('Error running bzr log')

        # Get all tags.
        bzr = Popen(('bzr', 'tags'), stdout=PIPE)
        output, error = bzr.communicate()
        code = bzr.wait()
        if code != 0:
            raise Exception('Error running bzr tags')
        tags = list(map(bytes.decode, output.splitlines()))
        if not tags:
            tag_version = '0.0.0'
            tag_revision = '0'
        else:
            # Remove any tag that has "?" as revision number. A "?" as revision number indicates, that this tag is from
            # another series.
            tags = [tag for tag in tags if tag.split()[-1].strip() != '?']
            # Get the last tag and split it in a revision and tag name.
            tag_version, tag_revision = tags[-1].split()
        # If they are equal, then this tree is tarball with the source for the release. We do not want the revision
        # number in the full version.
        if tree_revision == tag_revision:
            full_version = tag_version.strip()
        else:
            full_version = '{tag}-bzr{tree}'.format(tag=tag_version.strip(), tree=tree_revision.strip())
    else:
        # We're not running the development version, let's use the file.
        file_path = AppLocation.get_directory(AppLocation.VersionDir)
        file_path = os.path.join(file_path, '.version')
        version_file = None
        try:
            version_file = open(file_path, 'r')
            full_version = str(version_file.read()).rstrip()
        except IOError:
            log.exception('Error in version file.')
            full_version = '0.0.0-bzr000'
        finally:
            if version_file:
                version_file.close()
    bits = full_version.split('-')
    APPLICATION_VERSION = {
        'full': full_version,
        'version': bits[0],
        'build': bits[1] if len(bits) > 1 else None
    }
    if APPLICATION_VERSION['build']:
        log.info('Openlp version {version} build {build}'.format(version=APPLICATION_VERSION['version'],
                                                                 build=APPLICATION_VERSION['build']))
    else:
        log.info('Openlp version {version}'.format(version=APPLICATION_VERSION['version']))
    return APPLICATION_VERSION


def check_latest_version(current_version):
    """
    Check the latest version of OpenLP against the version file on the OpenLP
    site.

    **Rules around versions and version files:**

    * If a version number has a build (i.e. -bzr1234), then it is a nightly.
    * If a version number's minor version is an odd number, it is a development release.
    * If a version number's minor version is an even number, it is a stable release.

    :param current_version: The current version of OpenLP.
    """
    version_string = current_version['full']
    # set to prod in the distribution config file.
    settings = Settings()
    settings.beginGroup('core')
    last_test = settings.value('last version test')
    this_test = str(datetime.now().date())
    settings.setValue('last version test', this_test)
    settings.endGroup()
    if last_test != this_test:
        if current_version['build']:
            req = urllib.request.Request('http://www.openlp.org/files/nightly_version.txt')
        else:
            version_parts = current_version['version'].split('.')
            if int(version_parts[1]) % 2 != 0:
                req = urllib.request.Request('http://www.openlp.org/files/dev_version.txt')
            else:
                req = urllib.request.Request('http://www.openlp.org/files/version.txt')
        req.add_header('User-Agent', 'OpenLP/{version} {system}/{release}; '.format(version=current_version['full'],
                                                                                    system=platform.system(),
                                                                                    release=platform.release()))
        remote_version = None
        retries = 0
        while True:
            try:
                remote_version = str(urllib.request.urlopen(req, None,
                                                            timeout=CONNECTION_TIMEOUT).read().decode()).strip()
            except (urllib.error.URLError, ConnectionError):
                if retries > CONNECTION_RETRIES:
                    log.exception('Failed to download the latest OpenLP version file')
                else:
                    retries += 1
                    time.sleep(0.1)
                    continue
            break
        if remote_version:
            version_string = remote_version
    return version_string
