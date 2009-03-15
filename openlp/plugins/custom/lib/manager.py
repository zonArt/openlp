# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 - 2009 Martin Thompson, Tim Bentley

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

import os, os.path
import sys

from sqlalchemy import asc, desc
from openlp.plugins.custom.lib.models import init_models, metadata, session, \
    engine, CustomSlide, custom_slide_table

import logging

class CustomManager():
    """
    The Song Manager provides a central location for all database code. This
    class takes care of connecting to the database and running all the queries.
    """

    global log
    log=logging.getLogger(u'CustomManager')
    log.info(u'Custom manager loaded')

    def __init__(self, config):
        """
        Creates the connection to the database, and creates the tables if they
        don't exist.
        """
        self.config = config
        log.debug(u'Custom Initialising')
        self.db_url = u''
        db_type = self.config.get_config(u'db type', u'sqlite')
        if db_type == u'sqlite':
            self.db_url = u'sqlite:///' + self.config.get_data_path() + \
                u'/custom.sqlite'
        else:
            self.db_url = u'%s://%s:%s@%s/%s' % \
                (db_type, self.config.get_config(u'db username'),
                    self.config.get_config(u'db password'),
                    self.config.get_config(u'db hostname'),
                    self.config.get_config(u'db database'))
        self.session = init_models(self.db_url)
        if not custom_slide_table.exists():
            metadata.create_all()
        
        log.debug(u'Custom Initialised')
#
#    def process_dialog(self, dialogobject):
#        self.dialogobject = dialogobject
#
    def get_all_slides(self):
        """
        Returns the details of a song
        """
        return self.session.query(CustomSlide).order_by(CustomSlide.title).all()

    def save_slide(self, customslide):
        """
        Saves a song to the database
        """
        log.debug(u'Custom Slide added')
        try:
            self.session.add(customslide)
            self.session.commit()
            log.debug(u'Custom Slide saved')
            return True
        except:
            log.debug(u'Custom Slide failed')            
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
        if id !=0:
            customslide = self.get_custom(id)
            try:
                self.session.delete(customslide)
                self.session.commit()
                return True
            except:
                return False
        else:
            return True
