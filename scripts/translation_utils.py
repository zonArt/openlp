#!/usr/bin/env python
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
# Short description
# Steps for creating languages:
# 1. make shure that the openlp_en.ts file exist
# 2. go to scripts folder and start:
#     python translation_utils.py -a
###############################################################################

import os
import urllib

from optparse import OptionParser
from PyQt4 import QtCore

ignore_pathes = [u"./scripts", u"./openlp/core/test"]
ignore_files = [u"setup.py"]
translation_path = u"http://pootle.projecthq.biz/export/openlp/"
translations = [ u"en" 
                , u"af"
                , u"en_ZA"
                , u"en_GB"
                , u"de"
                , u"hu"
                , u"ko"
                , u"nb"
                , u"pt_BR"
                , u"es"
                , u"sv"]

def write_file(filename, stringlist):
    content = u''
    for line in stringlist:
        content = u'%s%s\n' % (content, line)
    file = open(filename, u'w')
    file.write(content.encode('utf8'))
    file.close()

def main():
    # Set up command line options.
    usage = u'Usage: %prog [options]'
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--download-ts", action="store_true",
        dest="download", help="Load languages from Pootle Server")
    parser.add_option("-p", "--prepare", action="store_true", dest="prepare",
        help="preparation (generate pro file)")
    parser.add_option("-u", "--update", action="store_true", dest="update",
        help="update translation files")
    parser.add_option("-g", "--generate", action="store_true", dest="generate",
        help="generate qm files")
    parser.add_option("-a", "--all", action="store_true", dest="all",
        help="proceed all options")

    (options, args) = parser.parse_args()
    if options.download:
        downloadTranslations()
    elif options.prepare:
        preparation()
    elif options.update:
        update()
    elif options.generate:
        generate()
    elif options.all:
        all()
    else:
        pass

def downloadTranslations():
    print "download()"
    for language in translations:
        filename = os.path.join(u'..', u'resources', u'i18n',
            u"openlp_%s.ts" % language)
        print filename
        page = urllib.urlopen(u"%s%s.ts" % (translation_path, language))
        content = page.read().decode("utf8")
        page.close()
        file = open(filename, u'w')
        file.write(content.encode('utf8'))
        file.close()

def preparation():
    stringlist = []
    start_dir = os.path.join(u'..')
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            path = u"%s" % root
            path = path.replace("\\","/")
            path = path.replace("..",".")
            
            if file.startswith(u'hook-') or file.startswith(u'test_'):
               continue

            cond = False
            for search in ignore_pathes:
                if path.startswith(search):
                    cond = True
            if cond:
                continue
            cond = False
            for search in ignore_files:
                if search == file:
                    cond = True
            if cond:
                continue
            
            if file.endswith(u'.py'):
                line = u"%s/%s" % (path, file)
                print u'Parsing "%s"' % line
                stringlist.append(u"SOURCES      += %s" % line)
            elif file.endswith(u'.pyw'):
                line = u"%s/%s" % (path, file)
                print u'Parsing "%s"' % line
                stringlist.append(u"SOURCES      += %s" % line)
            elif file.endswith(u'.ts'):
                line = u"%s/%s" % (path, file)
                print u'Parsing "%s"' % line
                stringlist.append(u"TRANSLATIONS += %s" % line)
            
    print u'Generating PRO file...',
    stringlist.sort()
    write_file(os.path.join(start_dir, u'openlp.pro'), stringlist)
    print u'done.'

def update():
    print "update()"
    updateProcess = QtCore.QProcess()
    updateProcess.start(u"pylupdate4 -noobsolete ../openlp.pro")
    updateProcess.waitForFinished(60000)

def generate():
    print "generate()"
    generateProcess = QtCore.QProcess()
    generateProcess.start(u"lrelease ../openlp.pro")
    generateProcess.waitForFinished(60000)

def all():
    print "all()"
    downloadTranslations()
    preparation()
    update()
    generate()

    
if __name__ == u'__main__':
    if os.path.split(os.path.abspath(u'.'))[1] != u'scripts':
        print u'You need to run this script from the scripts directory.'
    else:
        main()
