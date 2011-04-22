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
Windows Build Script
--------------------

This script is used to build the Windows binary and the accompanying installer.
For this script to work out of the box, it depends on a number of things:

Python 2.6
    This build script only works with Python 2.6.

PyQt4
    You should already have this installed, OpenLP doesn't work without it. The
    version the script expects is the packaged one available from River Bank
    Computing.

PyEnchant
    This script expects the precompiled, installable version of PyEnchant to be
    installed. You can find this on the PyEnchant site.

Inno Setup 5
    Inno Setup should be installed into "C:\%PROGRAMFILES%\Inno Setup 5"

UPX
    This is used to compress DLLs and EXEs so that they take up less space, but
    still function exactly the same. To install UPS, download it from
    http://upx.sourceforge.net/, extract it into C:\%PROGRAMFILES%\UPX, and then
    add that directory to your PATH environment variable.

Sphinx
    This is used to build the documentation

HTML Help Workshop
    This is used to create the help file

PyInstaller
    PyInstaller should be a checkout of revision 844 of trunk, and in a
    directory called, "pyinstaller" on the same level as OpenLP's Bazaar shared
    repository directory. The revision is very important as there is currently
    a major regression in HEAD.

    To install PyInstaller, first checkout trunk from Subversion. The easiest
    way is to install TortoiseSVN and then checkout the following URL to a
    directory called "pyinstaller"::

        http://svn.pyinstaller.org/trunk

    Then you need to copy the two hook-*.py files from the "pyinstaller"
    subdirectory in OpenLP's "resources" directory into PyInstaller's "hooks"
    directory.

    Once you've done that, open a command prompt (DOS shell), navigate to the
    PyInstaller directory and run::

        C:\Projects\pyinstaller>python Configure.py

Bazaar
    You need the command line "bzr" client installed.

OpenLP
    A checkout of the latest code, in a branch directory, which is in a Bazaar
    shared repository directory. This means your code should be in a directory
    structure like this: "openlp\branch-name".

Visual C++ 2008 Express Edition
    This is to build pptviewlib.dll, the library for controlling the
    PowerPointViewer

windows-builder.py
    This script, of course. It should be in the "scripts" directory of OpenLP.

"""

import os
import sys
from shutil import copy
from subprocess import Popen, PIPE

python_exe = sys.executable
innosetup_exe = os.path.join(os.getenv(u'PROGRAMFILES'), 'Inno Setup 5',
    u'ISCC.exe')
sphinx_exe = os.path.join(os.path.split(python_exe)[0], u'Scripts',
    u'sphinx-build.exe')
hhc_exe = os.path.join(os.getenv(u'PROGRAMFILES'), 'HTML Help Workshop',
    u'hhc.exe')
vcbuild_exe = os.path.join(os.getenv(u'PROGRAMFILES'), 
    'Microsoft Visual Studio 9.0', 'VC','vcpackages','vcbuild.exe')

# Base paths
script_path = os.path.split(os.path.abspath(__file__))[0]
branch_path = os.path.abspath(os.path.join(script_path, u'..'))
site_packages = os.path.join(os.path.split(python_exe)[0], u'Lib',
    u'site-packages')

# Files and executables
pyi_build = os.path.abspath(os.path.join(branch_path, u'..', u'..',
    u'pyinstaller', u'Build.py'))
lrelease_exe = os.path.join(site_packages, u'PyQt4', u'bin', u'lrelease.exe')
i18n_utils = os.path.join(script_path, u'translation_utils.py')

# Paths
source_path = os.path.join(branch_path, u'openlp')
manual_path = os.path.join(branch_path, u'documentation', u'manual')
i18n_path = os.path.join(branch_path, u'resources', u'i18n')
winres_path = os.path.join(branch_path, u'resources', u'windows')
build_path = os.path.join(branch_path, u'build', u'pyi.win32', u'OpenLP')
dist_path = os.path.join(branch_path, u'dist', u'OpenLP')
enchant_path = os.path.join(site_packages, u'enchant')
pptviewlib_path = os.path.join(source_path, u'plugins', u'presentations',
    u'lib', u'pptviewlib')

def update_code():
    os.chdir(branch_path)
    print u'Reverting any changes to the code...'
    bzr = Popen((u'bzr', u'revert'), stdout=PIPE)
    output, error = bzr.communicate()
    code = bzr.wait()
    if code != 0:
       print output
       raise Exception(u'Error reverting the code')
    print u'Updating the code...'
    bzr = Popen((u'bzr', u'update'), stdout=PIPE)
    output, error = bzr.communicate()
    code = bzr.wait()
    if code != 0:
       print output
       raise Exception(u'Error updating the code')

def run_pyinstaller():
    print u'Running PyInstaller...'
    os.chdir(branch_path)
    pyinstaller = Popen((python_exe, pyi_build, u'-y', u'-o', build_path,
        os.path.join(winres_path, u'OpenLP.spec')), stdout=PIPE)
    output, error = pyinstaller.communicate()
    code = pyinstaller.wait()
    if code != 0:
        print output
        raise Exception(u'Error running PyInstaller')

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

def copy_enchant():
    print u'Copying enchant/pyenchant...'
    source = enchant_path
    dest = os.path.join(dist_path, u'enchant')
    for root, dirs, files in os.walk(source):
        for filename in files:
            if not filename.endswith(u'.pyc') and not filename.endswith(u'.pyo'):
                dest_path = os.path.join(dest, root[len(source) + 1:])
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                copy(os.path.join(root, filename),
                    os.path.join(dest_path, filename))

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
    copy(os.path.join(winres_path, u'OpenLP.ico'),
        os.path.join(dist_path, u'OpenLP.ico'))
    copy(os.path.join(winres_path, u'LICENSE.txt'),
        os.path.join(dist_path, u'LICENSE.txt'))

def update_translations():
    print u'Updating translations...'
    os.chdir(script_path)
    translation_utils = Popen((python_exe, i18n_utils, u'-qdpu'))
    code = translation_utils.wait()
    if code != 0:
        raise Exception(u'Error running translation_utils.py')

def compile_translations():
    print u'Compiling translations...'
    files = os.listdir(i18n_path)
    if not os.path.exists(os.path.join(dist_path, u'i18n')):
        os.makedirs(os.path.join(dist_path, u'i18n'))
    for file in files:
        if file.endswith(u'.ts'):
            source_path = os.path.join(i18n_path, file)
            dest_path = os.path.join(dist_path, u'i18n',
                file.replace(u'.ts', u'.qm'))
            lconvert = Popen((lrelease_exe, u'-compress', u'-silent',
                source_path, u'-qm', dest_path))
            code = lconvert.wait()
            if code != 0:
                raise Exception('Error running lconvert on %s' % source_path)

def run_sphinx():
    print u'Running Sphinx...'
    os.chdir(manual_path)
    sphinx = Popen((sphinx_exe, u'-b', u'htmlhelp', u'-d', u'build/doctrees',
        u'source', u'build/htmlhelp'), stdout=PIPE)
    output, error = sphinx.communicate()
    code = sphinx.wait()
    if code != 0:
        print output
        raise Exception(u'Error running Sphinx')

def run_htmlhelp():
    print u'Running HTML Help Workshop...'
    os.chdir(os.path.join(manual_path, u'build', u'htmlhelp'))
    hhc = Popen((hhc_exe, u'OpenLP.chm'), stdout=PIPE)
    output, error = hhc.communicate()
    code = hhc.wait()
    if code != 1:
        print u'Exit code:', code
        print output
        raise Exception(u'Error running HTML Help Workshop')
    else:
        copy(os.path.join(manual_path, u'build', 'htmlhelp', u'OpenLP.chm'),
            os.path.join(dist_path, u'OpenLP.chm'))

def run_innosetup():
    print u'Running Inno Setup...'
    os.chdir(winres_path)
    innosetup = Popen((innosetup_exe,
        os.path.join(winres_path, u'OpenLP-2.0.iss'), u'/q'))
    code = innosetup.wait()
    if code != 0:
        raise Exception(u'Error running Inno Setup')

def build_pptviewlib():
    print u'Building PPTVIEWLIB.DLL...'
    vcbuild = Popen((vcbuild_exe, '/rebuild',
        os.path.join(pptviewlib_path, u'pptviewlib.vcproj'), u'Release|Win32'))
    code = vcbuild.wait()
    if code != 0:
        raise Exception(u'Error building pptviewlib.dll')
    copy(os.path.join(pptviewlib_path, u'Release', 'pptviewlib.dll'),
        pptviewlib_path)

def main():
    skip_update = False
    import sys
    for arg in sys.argv:
        if arg == u'-v' or arg == u'--verbose':
            print "Script path:", script_path
            print "Branch path:", branch_path
            print "Source path:", source_path
            print "\"dist\" path:", dist_path
            print "PyInstaller:", pyi_build
            print "Inno Setup path:", innosetup_exe
            print "Windows resources:", winres_path
            print "VCBuild path:", vcbuild_exe
            print "PPTVIEWLIB path:", pptviewlib_path
        elif arg == u'--skip-update':
            skip_update = True
        elif arg == u'/?' or arg == u'-h' or arg == u'--help':
            print u'Command options:'
            print u' -v --verbose : More verbose output'
            print u' --skip-update : Do not update or revert current branch'
            exit()
    if not skip_update:
        update_code()
    build_pptviewlib()
    run_pyinstaller()
    write_version_file()
    copy_enchant()
    copy_plugins()
    copy_windows_files()
    update_translations()
    compile_translations()
    run_sphinx()
    run_htmlhelp()
    run_innosetup()
    print "Done."

if __name__ == u'__main__':
    main()
