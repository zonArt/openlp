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

from openlp.plugins.audit.lib.models import init_models, metadata, AuditItem

class AuditManager():
    """
    The Song Manager provides a central location for all database code. This
    class takes care of connecting to the database and running all the queries.
    """

    global log
    log=logging.getLogger(u'AuditManager')
    log.info(u'Audit manager loaded')

    def __init__(self, config):
        """
        Creates the connection to the database, and creates the tables if they
        don't exist.
        """
        self.config = config
        log.debug(u'Audit Initialising')
        self.db_url = u''
        db_type = self.config.get_config(u'db type', u'sqlite')
        if db_type == u'sqlite':
            self.db_url = u'sqlite:///%s/audit.sqlite' % \
                self.config.get_data_path()
        else:
            self.db_url = u'%s://%s:%s@%s/%s' % \
                (db_type, self.config.get_config(u'db username'),
                    self.config.get_config(u'db password'),
                    self.config.get_config(u'db hostname'),
                    self.config.get_config(u'db database'))
        self.session = init_models(self.db_url)
        metadata.create_all(checkfirst=True)

        log.debug(u'Audit Initialised')

    def get_all_audits(self):
        """
        Returns the details of a audit
        """
        return self.session.query(AuditItem).order_by(AuditItem.title).all()

    def insert_audit(self, audititem):
        """
        Saves an audit to the database
        """
        log.debug(u'Audit added')
        try:
            self.session.add(audititem)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            log.exception(u'Audit item failed to save')
            return False

    def get_audit(self, id=None):
        """
        Returns the details of an audit
        """
        if id is None:
            return AuditItem()
        else:
            return self.session.query(AuditItem).get(id)

    def delete_audit(self, id):
        """
        Delete a audit record
        """
        if id !=0:
            audititem = self.get_audit(id)
            try:
                self.session.delete(audititem)
                self.session.commit()
                return True
            except:
                self.session.rollback()
                log.excertion(u'Audit Item failed to delete')
                return False
        else:
            return True

    def delete_all(self):
        """
        Delete a audit record
        """
        id = 0
        if id !=0:
            audititem = self.get_audit(id)
            try:
                self.session.delete(audititem)
                self.session.commit()
                return True
            except:
                self.session.rollback()
                log.excertion(u'Audit Item failed to delete')
                return False
        else:
            return True
