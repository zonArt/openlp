# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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
Windows Build Script
--------------------

This script is used to build the Windows binary and the accompanying installer.

For this script to work out of the box, it depends on being inside the
"resources/pyinstaller" directory in the OpenLP source tree, it depends on
OpenLP having it's own project directory which all the branches live in, and it
depends on PyInstaller being
"""

import os
from shutil import copy
from subprocess import Popen, PIPE

script_path = os.path.split(os.path.abspath(__file__))[0]
pyinstaller_path = os.path.abspath(os.path.join(script_path, u'..', u'..', u'..', u'..', u'pyinstaller'))
innosetup_path = os.path.join(os.getenv(u'PROGRAMFILES'), 'Inno Setup 5')
iss_path = os.path.abspath(os.path.join(script_path, u'..', u'innosetup'))
branch_path = os.path.abspath(os.path.join(script_path, u'..', u'..'))
source_path = os.path.join(branch_path, u'openlp')
dist_path = os.path.join(branch_path, u'dist', u'OpenLP')


def run_pyinstaller():
    print u'Running PyInstaller...'
    os.chdir(branch_path)
    pyinstaller = Popen((u'python', os.path.join(pyinstaller_path, u'Build.py'),
        u'OpenLP.spec'))
    code = pyinstaller.wait()
    if code != 0:
        raise Exception(u'Error running PyInstaller Build.py')

def write_version_file():
    print u'Writing version file...'
    os.chdir(branch_path)
    bzr = Popen((u'bzr', u'tags', u'--sort', u'time'), stdout=PIPE)
    output, error = bzr.communicate()
    code = bzr.wait()
    if code != 0:
        raise Exception(u'Error running bzr tags')
    lines = output.splitlines()
    if len(lines) == 0:
        tag = u'0.0.0'
        revision = u'0'
    else:
        tag, revision = lines[-1].split()
    bzr = Popen((u'bzr', u'log', u'--line', u'-r', u'-1'), stdout=PIPE)
    output, error = bzr.communicate()
    code = bzr.wait()
    if code != 0:
        raise Exception(u'Error running bzr log')
    latest = output.split(u':')[0]
    versionstring = latest == revision and tag or u'%s-bzr%s' % (tag, latest)
    f = open(os.path.join(dist_path, u'.version'), u'w')
    f.write(versionstring)
    f.close()

def copy_plugins():
    print u'Copying plugins...'
    source = os.path.join(source_path, u'plugins')
    dest = os.path.join(dist_path, u'plugins')
    for root, dirs, files in os.walk(source):
        for filename in files:
            if not filename.endswith(u'.pyc'):
                dest_path = os.path.join(dest, root[len(source)+1:])
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                copy(os.path.join(root, filename),
                    os.path.join(dest_path, filename))

def copy_windows_files():
    print u'Copying extra files for Windows...'
    copy(os.path.join(iss_path, u'OpenLP.ico'), os.path.join(dist_path, u'OpenLP.ico'))
    copy(os.path.join(iss_path, u'LICENSE.txt'), os.path.join(dist_path, u'LICENSE.txt'))

def run_innosetup():
    print u'Running Inno Setup...'
    os.chdir(iss_path)
    run_command = u'"%s" "%s"' % (os.path.join(innosetup_path, u'ISCC.exe'),
        os.path.join(iss_path, u'OpenLP-2.0.iss'))
    print run_command
    innosetup = Popen(run_command)
    code = innosetup.wait()
    if code != 0:
        raise Exception(u'Error running Inno Setup')

def main():
    print "Script path:", script_path
    print "PyInstaller path:", pyinstaller_path
    print "Inno Setup path:", innosetup_path
    print "ISS file path:", iss_path
    print "Branch path:", branch_path
    print "Source path:", source_path
    print "\"dist\" path:", dist_path
    run_pyinstaller()
    write_version_file()
    copy_plugins()
    copy_windows_files()
    run_innosetup()
    print "Done."

if __name__ == u'__main__':
    main()