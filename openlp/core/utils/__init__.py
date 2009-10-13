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

from registry import Registry
from confighelper import ConfigHelper

log = logging.getLogger()

__all__ = ['Registry', 'ConfigHelper']

def check_latest_version(config, current_version):
    version_string = current_version
    lastTest = config.get_config(u'Application version Test', datetime.now().date())
    thisTest = unicode(datetime.now().date())
    config.set_config(u'Application version Test', thisTest)
    if lastTest != thisTest:
        version_string = u''
        req = urllib2.Request(u'http://www.openlp.org/files/version.txt')
        req.add_header(u'User-Agent', u'OpenLP Version Checker')
        try:
            handle = urllib2.urlopen(req, None, 1)
            html = handle.read()
            version_string = unicode(html).rstrip()
        except IOError, e:
            if hasattr(e, u'reason'):
                log.exception(u'Reason for failure: %s', e.reason)
    return version_string
