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

import os, os.path
import sys

from sqlalchemy import asc, desc
from openlp.plugins.audit.lib.models import init_models, metadata, session, \
    engine, audit_table, Audit

import logging

class AuditManager():
    """
    The Song Manager provides a central location for all database code. This
    class takes care of connecting to the database and running all the queries.
    """

    global log
    log = logging.getLogger(u'AuditManager')
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
            self.db_url = u'sqlite:///%s/Audit.sqlite' % \
                self.config.get_data_path()
        else:
            self.db_url = db_type + 'u://' + \
                self.config.get_config(u'db username') + u':' + \
                self.config.get_config(u'db password') + u'@' + \
                self.config.get_config(u'db hostname') + u'/' + \
                self.config.get_config(u'db database')
        self.session = init_models(self.db_url)
        metadata.create_all(checkfirst=True)
        log.debug(u'AuditInitialised')

    def get_audits(self):
        """
        Returns a list of all the audits
        """
        return self.session.query(audit).order_by(audit.whensung).all()

    def get_audit(self, id):
        """
        Details of the audit
        """
        return self.session.query(audit).get(id)

    def save_audit(self, audit):
        """
        Save the audit and refresh the cache
        """
        try:
            self.session.add(audit)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            log.exception(u'Could not save audit to song database')
            return False

    def delete_audit(self, auditid):
        """
        Delete the audit
        """
        audit = self.get_audit(auditid)
        try:
            self.session.delete(audit)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            log.exception(u'Could not delete audit from song database')
            return False

