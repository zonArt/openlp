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

import logging

from sqlalchemy.exceptions import InvalidRequestError

from openlp.core.lib.db import Manager
from openlp.plugins.songusage.lib.db import init_schema, SongUsageItem

log = logging.getLogger(__name__)

class SongUsageManager(Manager):
    """
    The Song Manager provides a central location for all database code. This
    class takes care of connecting to the database and running all the queries.
    """
    log.info(u'SongUsage manager loaded')

    def __init__(self):
        """
        Creates the connection to the database, and creates the tables if they
        don't exist.
        """
        log.debug(u'SongUsage Initialising')
        Manager.__init__(self, u'songusage', init_schema)
        log.debug(u'SongUsage Initialised')

    def get_songusage_for_period(self, start_date, end_date):
        """
        Returns the details of SongUsage for a designated time period

        ``start_date``
            The start of the period to return

        ``end_date``
            The end of the period to return
        """
        return self.session.query(SongUsageItem) \
            .filter(SongUsageItem.usagedate >= start_date.toPyDate()) \
            .filter(SongUsageItem.usagedate < end_date.toPyDate()) \
            .order_by(SongUsageItem.usagedate, SongUsageItem.usagetime).all()

    def delete_to_date(self, date):
        """
        Delete SongUsage records before given date
        """
        try:
            self.session.query(SongUsageItem) \
                .filter(SongUsageItem.usagedate <= date) \
                .delete(synchronize_session=False)
            self.session.commit()
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Failed to delete all Song Usage items to %s' % date)
            return False
