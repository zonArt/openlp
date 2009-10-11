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

import logging
import urllib2
from datetime import datetime


class LatestVersion(object):
    """
    """
    global log
    log = logging.getLogger(u'LatestVersion')
    log.info(u'Latest Version detector loaded')

    def __init__(self, config):
        self.config = config

    def checkVersion(self, current_version):
        version_string = current_version
        lastTest = self.config.get_config(u'Application version Test', datetime.now().date())
        thisTest = unicode(datetime.now().date())
        self.config.set_config(u'Application version Test', thisTest)
        if lastTest != thisTest:
            print "Now check"
            version_string = u''
            req = urllib2.Request(u'http://www.openlp.oeg/files/version.txt')
            req.add_header(u'User-Agent', u'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
            try:
                handle = urllib2.urlopen(req, None, 1)
                html = handle.read()
                version_string = unicode(html).rstrip()
            except IOError, e:
                if hasattr(e, u'reason'):
                    log.exception(u'Reason for failure: %s', e.reason)
        return version_string
