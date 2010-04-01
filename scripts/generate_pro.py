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
# 1. create an empty ts file for the wished translation in ./resources/i18n folder
# 2. go to scripts folder and start:
#     python generate_pro.py
# 3. go to main folder and start:
#     pylupdate4 openlp.pro
# 4. do all the translation stuff at the related *.ts files (install first qt3-dev-tools)
# 5. at main folder start:
#     lrelease -verbose openlp.pro
###############################################################################

import os

ignore_pathes = ["./scripts", "./openlp/core/test"]
ignore_files = ["setup.py"]

def write_file(filename, stringlist):
    content = u''
    for line in stringlist:
        content = u'%s%s\n' % (content, line)
    file = open(filename, u'w')
    file.write(content.encode('utf8'))
    file.close()

def main():
    stringlist = []
    start_dir = os.path.join(u'..')
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            path = "%s" % root
            path = path.replace("\\","/")
            path = path.replace("..",".")
            
            if file.startswith(u'hook-') or file.startswith(u'test_'):
               continue

            cond = False
            for search in ignore_pathes:
                if path.startswith(search):
                    cond = True
            if cond == True:
                continue
            cond = False
            for search in ignore_files:
                if search == file:
                    cond = True
            if cond == True:
                continue
            
#            if file.endswith(u'.ui'):
#                line = "%s/%s" % (path, file)
#                print u'Parsing "%s"' % line
#                stringlist.append("FORMS        += %s" % line)
            if file.endswith(u'.py'):
                line = "%s/%s" % (path, file)
                print u'Parsing "%s"' % line
                stringlist.append("SOURCES      += %s" % line)
            elif file.endswith(u'.pyw'):
                line = "%s/%s" % (path, file)
                print u'Parsing "%s"' % line
                stringlist.append("SOURCES      += %s" % line)
            elif file.endswith(u'.ts'):
                line = "%s/%s" % (path, file)
                print u'Parsing "%s"' % line
                stringlist.append("TRANSLATIONS += %s" % line)
            
    print u'Generating PRO file...',
    stringlist.sort()
    write_file(os.path.join(start_dir, u'openlp.pro'), stringlist)
    print u'done.'

if __name__ == u'__main__':
    if os.path.split(os.path.abspath(u'.'))[1] != u'scripts':
        print u'You need to run this script from the scripts directory.'
    else:
        main()
