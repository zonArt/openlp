#!/usr/bin/python
# -*- encoding: utf-8 -*-

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

"""
Mac OS X Build Script
---------------------

This script is used to build the OS X binary and the accompanying installer.
For this script to work out of the box, it depends on a number of things:

Python 2.6
    This build script only works with Python 2.6.

PyQt4
    You should already have this installed, OpenLP doesn't work without it. The
    version the script expects is the packaged one available from River Bank
    Computing.

PyInstaller
    PyInstaller should be a checkout of revision 1355 of trunk, and in a
    directory  which is configured in the openlp.cfg. The revision is very
    important as there is just included a fix for builds on OS X.

    To install PyInstaller, first checkout trunk from Subversion. The easiest
    way is to do a
    
        svn co http://svn.pyinstaller.org/trunk

    Then you need to copy the two hook-*.py files from the "pyinstaller"
    subdirectory in OpenLP's "resources" directory into PyInstaller's "hooks"
    directory.
    
openlp.cfg
    The configuration file contains settings of the version string to include
    in the bundle as well as directory and file settings for different purposes
    (e.g. PyInstaller location or installer background image)
    
To start the build process do a 

   make

inside the resources/osx directory. The result should be a {openlp_dmgname}.dmg
file in the same directory. If something went wrong - this sometimes happen
with the graphical commands in the Apple script - do a 

   make clean
   
and start the build process again. If you want to execute only parts of the
build process you can specify different make targets
  
    make view -- runs the Apple scripts to set the icons
    make package -- creates the dmg file and copies the application files
    make bundle -- compresses the dmg file and sets the dmg file icon
"""

import time
import os
import ConfigParser
import logging
import optparse
import sys
import platform
import re
import subprocess as subp

# set the script name
script_name = "build"

def build_application(settings, app_name_lower, app_dir):
    logging.info('[%s] now building the app with pyinstaller at "%s"...',
        script_name, settings['pyinstaller_basedir'])
    result = os.system('python %s/pyinstaller.py openlp.spec' \
              % settings['pyinstaller_basedir'])
    if (result != 0):
        logging.error('[%s] The pyinstaller build reported an error, cannot \
            continue!', script_name)
        sys.exit(1)
    
    logging.info('[%s] copying the qt_menu files...', script_name)
    # see http://www.pyinstaller.org/ticket/157
    result = os.system('cp -R %(qt_menu_directory)s \
        %(application_directory)s/Contents/Resources' \
        % { 'qt_menu_directory' : settings['qt_menu_basedir'], 
            'application_directory' : app_dir })
    if (result != 0):
        logging.error('[%s] could not copy the qt_menu files, cannot \
            continue!', script_name)
        sys.exit(1)

    dist_folder = os.getcwd() + '/dist/' + app_name_lower
    # logging.info('[%s] copying the additional app files (from %s)...',
    #    script_name, dist_folder)
    # result = os.system('cp -R %(dist_directory)s/* '
    #    + '%(application_directory)s/Contents/MacOS' \
    #    % { 'dist_directory' : dist_folder,
    #        'application_directory' : app_dir })
    # if (result != 0):
    #     logging.error('[%s] could not copy additional files, cannot '
    #         + 'continue!', script_name)
    #     sys.exit(1)

    logging.info('[%s] copying the new plugins...', script_name)
    result = os.system('cp -R %(openlp_directory)s/openlp/plugins \
        %(application_directory)s/Contents/MacOS' \
        % { 'openlp_directory' : settings['openlp_basedir'], 
            'application_directory' : app_dir })
    if (result != 0):
        logging.error('[%s] could not copy plugins, dmg creation failed!',
            script_name)
        sys.exit(1)

    logging.info('[%s] copying the icons to the resource directory...',
        script_name)
    result = os.system('cp %(icon_file)s \
        %(application_directory)s/Contents/Resources' \
        % { 'icon_file' : settings['openlp_icon_file'], 
            'application_directory' : app_dir })
    if (result != 0):
        logging.error('[%s] could not copy the icon, dmg creation failed!',
            script_name)
        sys.exit(1)

    logging.info('[%s] copying the version file...', script_name)
    result = os.system('CpMac %s/.version %s/Contents/MacOS' % (os.getcwd(),
        app_dir)) 
    if (result != 0):
        logging.error('[%s] could not copy the version file, dmg creation \
            failed!', script_name)
        sys.exit(1)
    
    logging.info('[%s] copying the new Info.plist...', script_name)
    result = os.system('cp %(target_directory)s/Info.plist \
        %(application_directory)s/Contents' \
        % { 'target_directory' : os.getcwd(), 
            'application_directory' : app_dir })
    if (result != 0):
        logging.error('[%s] could not copy the info file, dmg creation \
            failed!', script_name)
        sys.exit(1)

def deploy_qt(settings):
    logging.info('[%s] running mac deploy qt on %s.app...', script_name,
        settings['openlp_appname']);

    result = os.system('macdeployqt %s.app' % settings['openlp_appname']);
    if (result != 0):
        logging.error('[%s] could not create dmg file!', script_name)
        sys.exit(1)

def create_dmg(settings):
    logging.info('[%s] creating the dmg...', script_name)
    dmg_file = os.getcwd() + '/' + settings['openlp_dmgname'] + '.dmg' 
    result = os.system('hdiutil create %(dmg_file)s~ -ov -megabytes \
        %(vol_size)s -fs HFS+ -volname %(vol_name)s' \
        % { 'dmg_file' : dmg_file,
            'vol_size' : '250',
            'vol_name' : settings['openlp_appname'] })
    if (result != 0):
        logging.error('[%s] could not create dmg file!', script_name)
        sys.exit(1)

    logging.info('[%s] mounting the dmg file...', script_name)
    output = subp.Popen(["hdiutil", "attach", dmg_file + "~.dmg"],
        stdout=subp.PIPE).communicate()[0]
    logging.debug(output)

    p = re.compile('Apple_HFS\s+(.+?)\s*$')
    result = p.search(output, re.M)
    volume_basedir = ''
    if result:
        volume_basedir = result.group(1)
    else:
        logging.error('could not mount dmg file, cannot continue!')
        sys.exit(1)

    logging.info('[%s] copying the app (from %s) to the dmg (at %s)...',
        script_name, app_dir, volume_basedir)
    result = os.system('CpMac -r %s %s' \
             % ( app_dir, volume_basedir ))
    if (result != 0):
        logging.error('[%s] could not copy application, dmg creation failed!',
            script_name)
        sys.exit(1)

    logging.info('[%s] copying the background image...', script_name)
    # os.mkdir(volume_basedir + '/.background')
    result = os.system('CpMac %s %s'
        % (settings['installer_backgroundimage_file'],
           volume_basedir + '/.installer-background.png'))
    if (result != 0):
        logging.error('[%s] could not copy the background image, dmg creation\
            failed!', script_name)
        sys.exit(1)
    
    return (volume_basedir, dmg_file)

def unmount_dmg(settings, volume_basedir):
    logging.info('[%s] unmounting the dmg...', script_name)
    result = os.system('hdiutil detach %s' % volume_basedir)
    if (result != 0):
        logging.error('[%s] could not unmount the dmg file, dmg creation \
            failed!', script_name)
        sys.exit(1)

def compress_view(settings, seticon_scriptname, dmg_file):
    logging.info('[%s] setting icon of the dmg file...', script_name)
    try:
        f = open(seticon_scriptname)
        p = subp.Popen(["osascript"], stdin=subp.PIPE)
        p.communicate(f.read() % ((os.getcwd() + '/' +
            settings['openlp_dmg_icon_file']), dmg_file))
        f.close()
        result = p.returncode
        if (result != 0):
            logging.error('[%s] could not set the icon to the dmg file, \
                dmg creation failed!', script_name)
            sys.exit(1)
    except IOError, e:
        logging.error('[%s] could not adjust the view (%s), dmg creation \
            failed!', script_name, e)
        sys.exit(1)
    except OSError, e:
        logging.error('[%s] could not set the icon to the dmg file(%s), \
            dmg creation failed!', script_name, e)
        sys.exit(1)

def adjust_package_view(settings, adjustview_scriptname):
    logging.info('[%s] making adjustments to the view...', script_name)
    try:
        f = open(adjustview_scriptname)
        p = subp.Popen(["osascript"], stdin=subp.PIPE)
        p.communicate(f.read() % ((os.getcwd() + '/' + \
            settings['openlp_dmg_icon_file']),
            settings['openlp_appname'],
            settings['openlp_appname'],
            settings['openlp_appname']))
        f.close()
        result = p.returncode
        if (result != 0):
            logging.error('[%s] could not adjust the view, dmg creation \
                failed!', script_name)
            sys.exit(1)
    except IOError, e:
        logging.error('[%s] could not adjust the view (%s), dmg creation \
            failed!', script_name, e)
        sys.exit(1)
    except OSError, e:
        logging.error('[%s] could not adjust the view (%s), dmg creation \
            failed!', script_name, e)
        sys.exit(1)

def compress_dmg(settings):
    logging.info('[%s] compress the dmg file...', script_name)
    result = os.system('hdiutil convert %s~.dmg -format UDZO \
        -imagekey zlib-level=9 -o %s' \
        % (dmg_file, dmg_file))
    if (result != 0):
        logging.error('[%s] could not compress the dmg file, dmg creation \
            failed!', script_name)
        sys.exit(1)


if __name__ == '__main__':

    # set default actions
    do_build = True
    do_compress_view = True
    do_package_view = True
    do_create_dmg = True
    do_compress_dmg = True
    do_deploy_qt = True
    
    parser = optparse.OptionParser()
    parser.add_option('-c', '--config', dest='config', help='config file',
        metavar='CONFIG')
    parser.add_option('-v', '--package-view', dest='package_view',
        help='triggers view adjustment scripts for package',
        metavar='PACKAGEVIEWONLY', action='store_true', default=False)
    parser.add_option('-y', '--compress-view', dest='compress_view',
       help='triggers view adjustment scripts for dmg',
       metavar='COMPRESSVIEWONLY', action='store_true', default=False)
    parser.add_option('-p', '--package', dest='package',
        help='package application folder to dmg', metavar='PACKAGE',
        action='store_true', default=False)
    parser.add_option('-z', '--compress', dest='compress',
        help='compresses the existing dmg', metavar='COMPRESS',
        action='store_true', default=False)
    parser.add_option('-b', '--basedir', dest='basedir',
        help='volume basedir like /Volumes/OpenLP', metavar='BASEDIR',
        default='/Volumes/OpenLP')
    
    (options, args) = parser.parse_args()
    
    # if an option is set, false all
    if (options.package_view is True or options.compress_view is True
        or options.package is True or options.compress is True):
        do_build = False
        do_deploy_qt = False
        do_package_view = options.package_view
        do_compress_view = options.compress_view
        do_create_dmg = options.package
        do_compress_dmg = options.compress

    if not options.config:
        parser.error('option --config|-c is required')

    logHandler = logging.StreamHandler()
    logHandler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)-8s %(message)s',
        '%a, %d %b %Y %H:%M:%S'))
    logging.getLogger().addHandler(logHandler)
    logging.getLogger().setLevel(logging.DEBUG)
 
    config = ConfigParser.RawConfigParser()
    config.readfp(open(options.config, 'r'))
 
    if not config.has_section('openlp'):
        logging.error('[%s] config file "%s" lacks an [openlp] section',
                      script_name, options.config)
        sys.exit(1)

    if not sys.platform == "darwin":
        logging.error('[%s] this script only works on Macintosh OS X systems,'
            + 'not on %s', script_name, sys.platform)
        sys.exit(1)

    version = platform.mac_ver()[0]
    # we only need the differenciation between leopard and snow leopard
    if version.startswith("10.6"):
        SNOWLEOPARD = True
        logging.info('[%s] using snow leopard scripts (version = %s)',
            script_name, version)
        adjustview_scriptname = "applescript-adjustview-10-6.master"
        seticon_scriptname = "applescript-seticon-10-6.master"
    else:
        SNOWLEOPARD = False
        logging.info('[%s] using leopard scripts (version = %s)', script_name,
            version)
        adjustview_scriptname = "applescript-adjustview-10-5.master"
        seticon_scriptname = "applescript-seticon-10-5.master"

    if not os.path.isfile(adjustview_scriptname) \
        or not os.path.isfile(seticon_scriptname):
        logging.error('[%s] could not find apple scripts for given OS X '
            + 'version %s', script_name, version)
        sys.exit(1)

    settings = dict()
    for k in config.options('openlp'):
        settings[k] = config.get('openlp', k)

    # prepare the configuration files
    os.system('python expander.py --config %(config_file)s \
        --template openlp.spec.master \
        --expandto %(target_directory)s/openlp.spec' \
        % { 'config_file' : options.config, 'target_directory' : os.getcwd() })
    os.system('python expander.py --config %(config_file)s \
        --template Info.plist.master \
        --expandto %(target_directory)s/Info.plist' \
        % { 'config_file' : options.config, 'target_directory' : os.getcwd() })
    os.system('python expander.py --config %(config_file)s \
        --template version.master \
        --expandto %(target_directory)s/.version' \
        % { 'config_file' : options.config, 'target_directory' : os.getcwd() })

    # prepare variables
    app_name_lower = settings['openlp_appname'].lower()
    app_dir = os.getcwd() + '/' + settings['openlp_appname'] + '.app'

    # if the view option is set, skip the building steps
    if (do_build is True):
        build_application(settings, app_name_lower, app_dir)

    if (do_deploy_qt is True):
        deploy_qt(settings)
        
    if (do_create_dmg is True):
        (volume_basedir, dmg_file) = create_dmg(settings)
    else:
        # setting base dir
        volume_basedir = options.basedir
        dmg_file = os.getcwd() + '/' + settings['openlp_dmgname'] + '.dmg'

    if (do_package_view is True):
        adjust_package_view(settings, adjustview_scriptname)

    if (do_create_dmg is True):
        unmount_dmg(settings, volume_basedir)

    if (do_compress_dmg is True):
        compress_dmg(settings)

    if (do_compress_view is True):
        compress_view(settings, seticon_scriptname, dmg_file)

    if (do_compress_dmg is True):
        logging.info('[%s] finished creating dmg file, resulting file is "%s"',
            script_name, dmg_file)

