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

from openlp.plugins.songusage.lib.models import init_models, metadata, SongUsageItem

class SongUsageManager():
    """
    The Song Manager provides a central location for all database code. This
    class takes care of connecting to the database and running all the queries.
    """

    global log
    log = logging.getLogger(u'SongUsageManager')
    log.info(u'SongUsage manager loaded')

    def __init__(self, config):
        """
        Creates the connection to the database, and creates the tables if they
        don't exist.
        """
        self.config = config
        log.debug(u'SongUsage Initialising')
        self.db_url = u''
        db_type = self.config.get_config(u'db type', u'sqlite')
        if db_type == u'sqlite':
            self.db_url = u'sqlite:///%s/songusage.sqlite' % \
                self.config.get_data_path()
        else:
            self.db_url = u'%s://%s:%s@%s/%s' % \
                (db_type, self.config.get_config(u'db username'),
                    self.config.get_config(u'db password'),
                    self.config.get_config(u'db hostname'),
                    self.config.get_config(u'db database'))
        self.session = init_models(self.db_url)
        metadata.create_all(checkfirst=True)

        log.debug(u'SongUsage Initialised')

    def get_all_songusage(self):
        """
        Returns the details of SongUsage
        """
        return self.session.query(SongUsageItem).\
            order_by(SongUsageItem.usagedate, SongUsageItem.usagetime ).all()

    def insert_songusage(self, songusageitem):
        """
        Saves an SongUsage to the database
        """
        log.debug(u'SongUsage added')
        try:
            self.session.add(songusageitem)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            log.exception(u'SongUsage item failed to save')
            return False

    def get_songusage(self, id=None):
        """
        Returns the details of a SongUsage
        """
        if id is None:
            return SongUsageItem()
        else:
            return self.session.query(SongUsageItem).get(id)

    def delete_songusage(self, id):
        """
        Delete a SongUsage record
        """
        if id !=0:
            songusageitem = self.get_songusage(id)
            try:
                self.session.delete(songusageitem)
                self.session.commit()
                return True
            except:
                self.session.rollback()
                log.exception(u'SongUsage Item failed to delete')
                return False
        else:
            return True

    def delete_all(self):
        """
        Delete all Song Usage records
        """
        try:
            self.session.query(SongUsageItem).delete(synchronize_session=False)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            log.exception(u'Failed to delete all Song Usage items')
            return False

    def delete_to_date(self, date):
        """
        Delete SongUsage records before given date
        """
        try:
            self.session.query(SongUsageItem)\
                .filter(SongUsageItem.usagedate <= date)\
                .delete(synchronize_session=False)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            log.exception(u'Failed to delete all Song Usage items to %s' % date)
            return False
