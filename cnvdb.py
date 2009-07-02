#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import codecs
import sys


class Convert():
    def __init__(self):
        pass

    def process(self, inname, outname):
        infile = codecs.open(inname, 'r', encoding='iso-8859-1')
        writefile = codecs.open(outname, 'w', encoding='utf-8')
        for line in infile:
            #replace the quotes with quotes
            line, replace("''", "'")
            writefile.write(line)
        infile.close()
        writefile.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'No action specified.'
        sys.exit()
    print u'Uncode conversion '
    print u'Input file  = ',  sys.argv[1:]
    print u'Output file = ',  sys.argv[2:]
    mig = Convert()
    mig.process(sys.argv[1:],sys.argv[2:])
