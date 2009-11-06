#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

import os
import re

ts_file = u"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="1.1">
%s
</TS>
"""
ts_context = u"""  <context>
    <name>%s</name>
%s  </context>
"""
ts_message = u"""    <message>
      <location filename="%s" line="%d"/>
      <source>%s</source>
      <translation type="unfinished"></translation>
    </message>
"""
find_trUtf8 = re.compile(r"trUtf8\(u?(['\"])([^\1]+)\1\)", re.UNICODE)
strings = {}

def parse_file(filename):
    global strings
    file = open(filename, u'r')
    class_name = u''
    line_number = 0
    for line in file:
        line_number += 1
        if line[:5] == u'class':
            class_name = line[6:line.find(u'(')]
            continue
        for match in find_trUtf8.finditer(line):
            key = u'%s-%s' % (class_name, match.group(1))
            if not key in strings:
                strings[key] = [class_name, filename, line_number, match.group(1)]
    file.close()

def write_file(filename):
    global strings
    translation_file = u''
    translation_contexts = []
    translation_messages = []
    class_name = strings[strings.keys()[0]][0]
    current_context = u''
    for key, translation in strings.iteritems():
        if class_name != translation[0]:
            current_context = ts_context % (class_name, u''.join(translation_messages))
            translation_contexts.append(current_context)
            translation_messages = []
            class_name = translation[0]
        translation_messages.append(ts_message % (translation[1], translation[2], translation[3]))
    current_context = ts_context % (class_name, u''.join(translation_messages))
    translation_contexts.append(current_context)
    translation_file = ts_file % (u''.join(translation_contexts))
    file = open(filename, u'w')
    file.write(translation_file)
    file.close()

def main():
    start_dir = u'.'
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(u'.py'):
                print u'Parsing "%s"' % file
                parse_file(os.path.join(root, file))
    print u'Generating TS file...',
    write_file(os.path.join(start_dir, u'i18n', u'openlp_en.ts'))
    print u'done.'

if __name__ == u'__main__':
    main()
