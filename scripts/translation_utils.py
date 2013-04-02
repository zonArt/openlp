#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Edwin Lunando, Joshua Miller, Stevan Pettit,  #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Simon Scudder, Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon      #
# Tibble, Dave Warnock, Frode Woldsund                                        #
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
This script is used to maintain the translation files in OpenLP. It downloads
the latest translation files from the Transifex translation server, updates the
local translation files from both the source code and the files from Transifex,
and can also generate the compiled translation files.

Create New Language
-------------------

To create a new language, simply run this script with the ``-c`` command line
option::

    @:~$ ./translation_utils.py -c

Update Translation Files
------------------------

The best way to update the translations is to download the files from Transifex,
and then update the local files using both the downloaded files and the source.
This is done easily via the ``-d``, ``-p`` and ``-u`` options::

    @:~$ ./translation_utils.py -dpu

"""
import os
import urllib2
from getpass import getpass
import base64
import json
import webbrowser

from optparse import OptionParser
from PyQt4 import QtCore

SERVER_URL = u'http://www.transifex.net/api/2/project/openlp/'
IGNORED_PATHS = [u'scripts']
IGNORED_FILES = [u'setup.py']

verbose_mode = False
quiet_mode = False
username = ''
password = ''

class Command(object):
    """
    Provide an enumeration of commands.
    """
    Download = 1
    Create = 2
    Prepare = 3
    Update = 4
    Generate = 5

class CommandStack(object):
    """
    This class provides an iterable stack.
    """
    def __init__(self):
        self.current_index = 0
        self.data = []

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        if not index in self.data:
            return None
        elif self.data[index].get(u'arguments'):
            return self.data[index][u'command'], self.data[index][u'arguments']
        else:
            return self.data[index][u'command']

    def __iter__(self):
        return self

    def next(self):
        if self.current_index == len(self.data):
            raise StopIteration
        else:
            current_item = self.data[self.current_index][u'command']
            self.current_index += 1
            return current_item

    def append(self, command, **kwargs):
        data = {u'command': command}
        if u'arguments' in kwargs:
            data[u'arguments'] = kwargs[u'arguments']
        self.data.append(data)

    def reset(self):
        self.current_index = 0

    def arguments(self):
        if self.data[self.current_index - 1].get(u'arguments'):
            return self.data[self.current_index - 1][u'arguments']
        else:
            return []

    def __repr__(self):
        results = []
        for item in self.data:
            if item.get(u'arguments'):
                results.append(str((item[u'command'], item[u'arguments'])))
            else:
                results.append(str((item[u'command'], )))
        return u'[%s]' % u', '.join(results)

def print_quiet(text, linefeed=True):
    """
    This method checks to see if we are in quiet mode, and if not prints
    ``text`` out.

    ``text``
        The text to print.
    """
    global quiet_mode
    if not quiet_mode:
        if linefeed:
            print text
        else:
            print text,

def print_verbose(text):
    """
    This method checks to see if we are in verbose mode, and if so prints
    ``text`` out.

    ``text``
        The text to print.
    """
    global verbose_mode, quiet_mode
    if not quiet_mode and verbose_mode:
        print(u'    %s' % text)

def run(command):
    """
    This method runs an external application.

    ``command``
        The command to run.
    """
    print_verbose(command)
    process = QtCore.QProcess()
    process.start(command)
    while (process.waitForReadyRead()):
        print_verbose(u'ReadyRead: %s' % QtCore.QString(process.readAll()))
    print_verbose(u'Error(s):\n%s' % process.readAllStandardError())
    print_verbose(u'Output:\n%s' % process.readAllStandardOutput())

def download_translations():
    """
    This method downloads the translation files from the Pootle server.

    **Note:** URLs and headers need to remain strings, not unicode.
    """
    global username, password
    print_quiet(u'Download translation files from Transifex')
    if not username:
        username = raw_input(u'   Transifex username: ')
    if not password:
        password = getpass(u'   Transifex password: ')
    # First get the list of languages
    url = SERVER_URL + 'resource/ents/'
    base64string = base64.encodestring(
        '%s:%s' % (username, password))[:-1]
    auth_header =  'Basic %s' % base64string
    request = urllib2.Request(url + '?details')
    request.add_header('Authorization', auth_header)
    print_verbose(u'Downloading list of languages from: %s' % url)
    try:
        json_response = urllib2.urlopen(request)
    except urllib2.HTTPError:
        print_quiet(u'Username or password incorrect.')
        return False
    json_dict = json.loads(json_response.read())
    languages = [lang[u'code'] for lang in json_dict[u'available_languages']]
    for language in languages:
        lang_url = url + 'translation/%s/?file' % language
        request = urllib2.Request(lang_url)
        request.add_header('Authorization', auth_header)
        filename = os.path.join(os.path.abspath(u'..'), u'resources', u'i18n',
            language + u'.ts')
        print_verbose(u'Get Translation File: %s' % filename)
        response = urllib2.urlopen(request)
        fd = open(filename, u'w')
        fd.write(response.read())
        fd.close()
    print_quiet(u'   Done.')
    return True

def prepare_project():
    """
    This method creates the project file needed to update the translation files
    and compile them into .qm files.
    """
    print_quiet(u'Generating the openlp.pro file')
    lines = []
    start_dir = os.path.abspath(u'..')
    start_dir = start_dir + os.sep
    print_verbose(u'Starting directory: %s' % start_dir)
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            path = root.replace(start_dir, u'').replace(u'\\', u'/') #.replace(u'..', u'.')
            if file.startswith(u'hook-') or file.startswith(u'test_'):
               continue
            ignore = False
            for ignored_path in IGNORED_PATHS:
                if path.startswith(ignored_path):
                    ignore = True
                    break
            if ignore:
                continue
            ignore = False
            for ignored_file in IGNORED_FILES:
                if file == ignored_file:
                    ignore = True
                    break
            if ignore:
                continue
            if file.endswith(u'.py') or file.endswith(u'.pyw'):
                if path:
                    line = u'%s/%s' % (path, file)
                else:
                    line = file
                print_verbose(u'Parsing "%s"' % line)
                lines.append(u'SOURCES      += %s' % line)
            elif file.endswith(u'.ts'):
                line = u'%s/%s' % (path, file)
                print_verbose(u'Parsing "%s"' % line)
                lines.append(u'TRANSLATIONS += %s' % line)
    lines.sort()
    file = open(os.path.join(start_dir, u'openlp.pro'), u'w')
    file.write(u'\n'.join(lines).encode('utf8'))
    file.close()
    print_quiet(u'   Done.')

def update_translations():
    print_quiet(u'Update the translation files')
    if not os.path.exists(os.path.join(os.path.abspath(u'..'), u'openlp.pro')):
        print(u'You have not generated a project file yet, please run this script with the -p option.')
        return
    else:
        os.chdir(os.path.abspath(u'..'))
        run(u'pylupdate4 -verbose -noobsolete openlp.pro')
        os.chdir(os.path.abspath(u'scripts'))

def generate_binaries():
    print_quiet(u'Generate the related *.qm files')
    if not os.path.exists(os.path.join(os.path.abspath(u'..'), u'openlp.pro')):
        print(u'You have not generated a project file yet, please run this script with the -p option. It is also ' +
            u'recommended that you this script with the -u option to update the translation files as well.')
        return
    else:
        os.chdir(os.path.abspath(u'..'))
        run(u'lrelease openlp.pro')
        print_quiet(u'   Done.')


def create_translation():
    """
    This method opens a browser to the OpenLP project page at Transifex so
    that the user can request a new language.
    """
    print_quiet(u'Please request a new language at the OpenLP project on '
        'Transifex.')
    webbrowser.open('https://www.transifex.net/projects/p/openlp/'
        'resource/ents/')
    print_quiet(u'Opening browser to OpenLP project...')

def process_stack(command_stack):
    """
    This method looks at the commands in the command stack, and processes them
    in the order they are in the stack.

    ``command_stack``
        The command stack to process.
    """
    if command_stack:
        print_quiet(u'Processing %d commands...' % len(command_stack))
        for command in command_stack:
            print_quiet(u'%d.' % (command_stack.current_index), False)
            if command == Command.Download:
                if not download_translations():
                    return
            elif command == Command.Prepare:
                prepare_project()
            elif command == Command.Update:
                update_translations()
            elif command == Command.Generate:
                generate_binaries()
            elif command == Command.Create:
                create_translation()
        print_quiet(u'Finished processing commands.')
    else:
        print_quiet(u'No commands to process.')

def main():
    global verbose_mode, quiet_mode, username, password
    # Set up command line options.
    usage = u'%prog [options]\nOptions are parsed in the order they are ' + \
        u'listed below. If no options are given, "-dpug" will be used.\n\n' + \
        u'This script is used to manage OpenLP\'s translation files.'
    parser = OptionParser(usage=usage)
    parser.add_option('-U', '--username', dest='username', metavar='USERNAME',
        help='Transifex username, used for authentication')
    parser.add_option('-P', '--password', dest='password', metavar='PASSWORD',
        help='Transifex password, used for authentication')
    parser.add_option('-d', '--download-ts', dest='download',
        action='store_true', help='download language files from Transifex')
    parser.add_option('-c', '--create', dest='create', action='store_true',
        help='go to Transifex to request a new translation file')
    parser.add_option('-p', '--prepare', dest='prepare', action='store_true',
        help='generate a project file, used to update the translations')
    parser.add_option('-u', '--update', action='store_true', dest='update',
        help='update translation files (needs a project file)')
    parser.add_option('-g', '--generate', dest='generate', action='store_true',
        help='compile .ts files into .qm files')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
        help='show extra information while processing translations')
    parser.add_option('-q', '--quiet', dest='quiet', action='store_true',
        help='suppress all output other than errors')
    (options, args) = parser.parse_args()
    # Create and populate the command stack
    command_stack = CommandStack()
    if options.download:
        command_stack.append(Command.Download)
    if options.create:
        command_stack.append(Command.Create, arguments=[options.create])
    if options.prepare:
        command_stack.append(Command.Prepare)
    if options.update:
        command_stack.append(Command.Update)
    if options.generate:
        command_stack.append(Command.Generate)
    verbose_mode = options.verbose
    quiet_mode = options.quiet
    if options.username:
        username = options.username
    if options.password:
        password = options.password
    if not command_stack:
        command_stack.append(Command.Download)
        command_stack.append(Command.Prepare)
        command_stack.append(Command.Update)
        command_stack.append(Command.Generate)
    # Process the commands
    process_stack(command_stack)

if __name__ == u'__main__':
    if os.path.split(os.path.abspath(u'.'))[1] != u'scripts':
        print(u'You need to run this script from the scripts directory.')
    else:
        main()
