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
from sqlalchemy.exceptions import InvalidRequestError

from openlp.core.utils import AppLocation
from openlp.plugins.custom.lib.models import init_models, metadata, CustomSlide

log = logging.getLogger(__name__)

class CustomManager(object):
    """
    The Song Manager provides a central location for all database code. This
    class takes care of connecting to the database and running all the queries.
    """
    log.info(u'Custom manager loaded')

    def __init__(self):
        """
        Creates the connection to the database, and creates the tables if they
        don't exist.
        """
        log.debug(u'Custom Initialising')
        settings = QtCore.QSettings()
        settings.beginGroup(u'custom')
        self.db_url = u''
        db_type = unicode(
            settings.value(u'db type', QtCore.QVariant(u'sqlite')).toString())
        if db_type == u'sqlite':
            self.db_url = u'sqlite:///%s/custom.sqlite' % \
                AppLocation.get_section_data_path(u'custom')
        else:
            self.db_url = u'%s://%s:%s@%s/%s' % (db_type,
                unicode(settings.value(u'db username').toString()),
                unicode(settings.value(u'db password').toString()),
                unicode(settings.value(u'db hostname').toString()),
                unicode(settings.value(u'db database').toString()))
        self.session = init_models(self.db_url)
        metadata.create_all(checkfirst=True)
        settings.endGroup()
        log.debug(u'Custom Initialised')

    def get_all_slides(self):
        """
        Returns the details of a Custom Slide Show
        """
        return self.session.query(CustomSlide).order_by(CustomSlide.title).all()

    def save_slide(self, customslide):
        """
        Saves a Custom slide show to the database
        """
        log.debug(u'Custom Slide added')
        try:
            self.session.add(customslide)
            self.session.commit()
            log.debug(u'Custom Slide saved')
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Custom Slide save failed')
            return False

    def get_custom(self, id=None):
        """
        Returns the details of a Custom Slide
        """
        if id is None:
            return CustomSlide()
        else:
            return self.session.query(CustomSlide).get(id)

    def delete_custom(self, id):
        """
        Delete a Custom slide show
        """
        if id != 0:
            customslide = self.get_custom(id)
            try:
                self.session.delete(customslide)
                self.session.commit()
                return True
            except InvalidRequestError:
                self.session.rollback()
                log.exception(u'Custom Slide deleton failed')
                return False
        else:
            return True

    def get_customs_for_theme(self, theme):
        return self.session.query(
            CustomSlide).filter(CustomSlide.theme_name == theme).all()
