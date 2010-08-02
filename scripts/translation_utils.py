#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
# Short description
# Steps for creating languages:
# 1. make sure that the openlp_en.ts file exist
# 2. go to scripts folder and start:
#     python translation_utils.py -a
###############################################################################

import os
import urllib
import re

from optparse import OptionParser
from PyQt4 import QtCore
from BeautifulSoup import BeautifulSoup

class TranslationUtils(object):
    def __init__(self):
        self.ignore_paths = [u'./scripts']
        self.ignore_files = [u'setup.py']
        self.server_url = u'http://pootle.projecthq.biz/export/openlp/'
        self.cmd_stack = []
        self.stack_count = 0
        self.verbose = False
    

    def process_stack(self):
        if len(self.cmd_stack) > 0:
            if len(self.cmd_stack) == self.stack_count:
                print u'Process %d commands' % self.stack_count
            print u'%d. ' % (self.stack_count-len(self.cmd_stack)+1),
            command = self.cmd_stack.pop(0)
            if len(command) > 1:
                command[0](command[1])
            else:
                command[0]()
        else:
            print "Finished all commands"


    def downloadTranslations(self):
        print 'Download Translation files from HQ-Server'
        page = urllib.urlopen(u'%s' % (self.server_url))
        soup = BeautifulSoup(page)
        languages = soup.findAll(text=re.compile(".*\.ts"))
        for language in languages:
            filename = os.path.join(u'..', u'resources', u'i18n',
                u'openlp_%s' % language)
            self.printVerbose(u'Get Translation File: %s' % filename)
            self.get_and_write_file(language, filename)
        print u'  done'
        self.process_stack()

    def get_and_write_file(self, language, filename):
        page = urllib.urlopen(u'%s%s' % (self.server_url, language))
        content = page.read().decode('utf8')
        page.close()
        file = open(filename, u'w')
        file.write(content.encode('utf8'))
        file.close()
            
    def creation(self, language):
        print "Create new Translation File"
        """
            Use this option to create a new translation file
            this function: 
                * create the new *.ts file
        """
        filename = os.path.join(u'..', u'resources', u'i18n',
                u'openlp_%s.ts' % language)
        self.get_and_write_file(u'en.ts', filename)
        self.printVerbose("""
            Please remind: For permanent providing this language:
            this language name have to append to the global list 
            variable "translations" in this file
            and this file have to be uploaded to the Pootle Server
            Please contact the developers!
            """)
        print u'  done'
        self.process_stack()
        
        
    def preparation(self):
        print u'Generating the openlp.pro file'
        stringlist = []
        start_dir = os.path.join(u'..')
        for root, dirs, files in os.walk(start_dir):
            for file in files:
                path = u'%s' % root
                path = path.replace('\\','/')
                path = path.replace('..','.')
                
                if file.startswith(u'hook-') or file.startswith(u'test_'):
                   continue

                cond = False
                for search in self.ignore_paths:
                    if path.startswith(search):
                        cond = True
                if cond:
                    continue
                cond = False
                for search in self.ignore_files:
                    if search == file:
                        cond = True
                if cond:
                    continue
                
                if file.endswith(u'.py'):
                    line = u'%s/%s' % (path, file)
                    self.printVerbose(u'Parsing "%s"' % line)
                    stringlist.append(u'SOURCES      += %s' % line)
                elif file.endswith(u'.pyw'):
                    line = u'%s/%s' % (path, file)
                    self.printVerbose(u'Parsing "%s"' % line)
                    stringlist.append(u'SOURCES      += %s' % line)
                elif file.endswith(u'.ts'):
                    line = u'%s/%s' % (path, file)
                    self.printVerbose(u'Parsing "%s"' % line)
                    stringlist.append(u'TRANSLATIONS += %s' % line)
                
        stringlist.sort()
        self.write_file(os.path.join(start_dir, u'openlp.pro'), stringlist)
        print u'  done'
        self.process_stack()

    def update(self):
        print u'Update the translation files'
        cmd = u'pylupdate4 -verbose -noobsolete ../openlp.pro'
        self.start_cmd(cmd)

    def generate(self):
        print u'Generate the related *.qm files'
        cmd = u'lrelease ../openlp.pro'
        self.start_cmd(cmd)
        
    def write_file(self, filename, stringlist):
        content = u''
        for line in stringlist:
            content = u'%s%s\n' % (content, line)
        file = open(filename, u'w')
        file.write(content.encode('utf8'))
        file.close()

    def printVerbose(self, data):
        if self.verbose:
            print u'    %s' % data

    def start_cmd(self, command):
        self.printVerbose(command)
        self.process = QtCore.QProcess()
        self.process.start(command)
        while (self.process.waitForReadyRead()):
            self.printVerbose(u'ReadyRead: %s' % QtCore.QString(self.process.readAll()))
        self.printVerbose(self.process.readAllStandardError())
        self.printVerbose(self.process.readAllStandardOutput())
        print u'  done'
        self.process_stack()
        

def main():
    # start Main Class
    Util = TranslationUtils()
    
    # Set up command line options.
    usage = u'''
        This script handle the translation files for OpenLP.
        Usage: %prog [options]
        If no option will be used, options "-d -p -u -g" will be set automatically
        '''
    parser = OptionParser(usage=usage)
    parser.add_option('-d', '--download-ts', action='store_true',
        dest='download', help='Load languages from Pootle Server')
    parser.add_option('-c', '--create', metavar='lang',
        help='creation of new translation file, Parameter: language (e.g. "en_GB"')
    parser.add_option('-p', '--prepare', action='store_true', dest='prepare',
        help='preparation (generate pro file)')
    parser.add_option('-u', '--update', action='store_true', dest='update',
        help='update translation files')
    parser.add_option('-g', '--generate', action='store_true', dest='generate',
        help='generate qm files')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
        help='Give more informations while processing')

    (options, args) = parser.parse_args()
    if options.download:
        Util.cmd_stack.append([Util.downloadTranslations])
    if options.create:
        Util.cmd_stack.append([Util.creation, u'%s' % options.create])
    if options.prepare:
        Util.cmd_stack.append([Util.preparation])
    if options.update:
        Util.cmd_stack.append([Util.update])
    if options.generate:
        Util.cmd_stack.append([Util.generate])
    if options.verbose:
        Util.verbose = True

    if len(Util.cmd_stack) == 0:
        Util.cmd_stack.append([Util.downloadTranslations])
        Util.cmd_stack.append([Util.preparation])
        Util.cmd_stack.append([Util.update])
        Util.cmd_stack.append([Util.generate])

    Util.stack_count = len(Util.cmd_stack)
    Util.process_stack()
    

    
if __name__ == u'__main__':
    if os.path.split(os.path.abspath(u'.'))[1] != u'scripts':
        print u'You need to run this script from the scripts directory.'
    else:
        main()
