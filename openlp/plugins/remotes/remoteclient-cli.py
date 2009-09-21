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
import socket
import sys
from optparse import OptionParser


def sendData(options, message):
    addr = (options.address, options.port)
    try:
        UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        UDPSock.sendto(message, addr)
        print u'message sent ', message, addr
    except:
        print u'Errow thrown ', sys.exc_info()[1]

def format_message(options):
    return u'%s:%s' % (options.event, options.message)

def main():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=True,
                      help="make lots of noise [%default]")
    parser.add_option("-p", "--port",
                      default=4316,
                      help="IP Port number %default ")
    parser.add_option("-a", "--address",
                      help="Recipient address ")
    parser.add_option("-e", "--event",
                      default=u'Alert',
                      help="Action to be undertaken")
    parser.add_option("-m", "--message",
                      help="Message to be passed for the action")
    parser.add_option("-n", "--slidenext",
                      help="Trigger the next slide")

    (options, args) = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        parser.error("incorrect number of arguments")
    elif options.message is None:
        parser.print_help()
        parser.error("No message passed")
    elif options.address is None:
        parser.print_help()
        parser.error("IP address missing")
    elif options.slidenext is not None:
        options.event = u'next_slide'
        options.message = u''
        text = format_message(options)
        sendData(options, text)
    else:
        text = format_message(options)
        sendData(options, text)

if __name__ == u'__main__':
    main()

