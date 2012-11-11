#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky                                             #
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

import urllib
import sys
from optparse import OptionParser

def sendData(options):
    addr = 'http://%s:%s/send/%s?q=%s' % (options.address, options.port,
        options.event, options.message)
    try:
        urllib.urlopen(addr)
        print u'Message sent ', addr
    except:
        print u'Error thrown ', sys.exc_info()[1]

def main():
    usage = "usage: %prog [-a address] [-p port] [-e event] [-m message]"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--port", default=4316,
                      help="IP Port number %default ")
    parser.add_option("-a", "--address",
                      help="Recipient address ",
                      default="localhost")
    parser.add_option("-e", "--event",
                      help="Action to be performed",
                      default="alerts_text")
    parser.add_option("-m", "--message",
                      help="Message to be passed for the action",
                      default="")

    (options, args) = parser.parse_args()
    if args:
        parser.print_help()
        parser.error("incorrect number of arguments")
    elif options.address is None:
        parser.print_help()
        parser.error("IP address missing")
    else:
        sendData(options)

if __name__ == u'__main__':
    main()
