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

from PyQt4 import QtCore

from openlp.core.utils import AppLocation
from openlp.plugins.alerts.lib.models import init_models, metadata, AlertItem

log = logging.getLogger(__name__)

class DBManager(object):
    """
    The Song Manager provides a central location for all database code. This
    class takes care of connecting to the database and running all the queries.
    """
    log.info(u'Alerts DB loaded')

    def __init__(self):
        """
        Creates the connection to the database, and creates the tables if they
        don't exist.
        """
        log.debug(u'Alerts Initialising')
        settings = QtCore.QSettings()
        settings.beginGroup(u'alerts')
        self.db_url = u''
        db_type = unicode(
            settings.value(u'db type', QtCore.QVariant(u'sqlite')).toString())
        if db_type == u'sqlite':
            self.db_url = u'sqlite:///%s/alerts.sqlite' % \
                AppLocation.get_section_data_path(u'alerts')
        else:
            self.db_url = u'%s://%s:%s@%s/%s' % (db_type,
                unicode(settings.value(u'db username').toString()),
                unicode(settings.value(u'db password').toString()),
                unicode(settings.value(u'db hostname').toString()),
                unicode(settings.value(u'db database').toString()))
        settings.endGroup()
        self.session = init_models(self.db_url)
        metadata.create_all(checkfirst=True)
        log.debug(u'Alerts Initialised')

    def get_all_alerts(self):
        """
        Returns the details of a Alert Show
        """
        return self.session.query(AlertItem).order_by(AlertItem.text).all()

    def save_alert(self, alert_item):
        """
        Saves a Alert show to the database
        """
        log.debug(u'Alert added')
        try:
            self.session.add(alert_item)
            self.session.commit()
            log.debug(u'Alert saved')
            return True
        except:
            self.session.rollback()
            log.exception(u'Alert save failed')
            return False

    def get_alert(self, id=None):
        """
        Returns the details of a Alert
        """
        if id is None:
            return AlertItem()
        else:
            return self.session.query(AlertItem).get(id)

    def delete_alert(self, id):
        """
        Delete a Alert show
        """
        if id != 0:
            alert_item = self.get_alert(id)
            try:
                self.session.delete(alert_item)
                self.session.commit()
                return True
            except:
                self.session.rollback()
                log.exception(u'Alert deleton failed')
                return False
        else:
            return True

