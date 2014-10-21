# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Ken Roberts, Simon Scudder,               #
# Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon Tibble,             #
# Dave Warnock, Frode Woldsund, Martin Zibricky, Patrick Zimmermann           #
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
"""
    :mod:`openlp.core.lib.projector.db` module

    Provides the database functions for the Projector module.

    The Manufacturer, Model, Source tables keep track of the video source
    strings used for display of input sources. The Source table maps
    manufacturer-defined or user-defined strings from PJLink default strings
    to end-user readable strings; ex: PJLink code 11 would map "RGB 1"
    default string to "RGB PC (analog)" string.
    (Future feature).

    The Projector table keeps track of entries for controlled projectors.
"""

import logging
log = logging.getLogger(__name__)
log.debug('projector.lib.db module loaded')

from os import path

from sqlalchemy import Column, ForeignKey, Integer, MetaData, String
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import backref, relationship

from openlp.core.lib.db import Manager, init_db, init_url
from openlp.core.lib.projector.constants import PJLINK_DEFAULT_SOURCES, PJLINK_DEFAULT_CODES

metadata = MetaData()
Base = declarative_base(metadata)


class CommonBase(object):
    """
    Base class to automate table name and ID column.
    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class Manufacturer(CommonBase, Base):
    """
    Projector manufacturer table.

    Manufacturer:
        name:   Column(String(30))
        models: Relationship(Model.id)

    Model table is related.
    """
    def __repr__(self):
        """
        Returns a basic representation of a Manufacturer table entry.
        """
        return '<Manufacturer(name="%s")>' % self.name

    name = Column(String(30))
    models = relationship('Model',
                          order_by='Model.name',
                          backref='manufacturer',
                          cascade='all, delete-orphan',
                          primaryjoin='Manufacturer.id==Model.manufacturer_id',
                          lazy='joined')


class Model(CommonBase, Base):
    """
    Projector model table.

    Model:
        name:               Column(String(20))
        sources:            Relationship(Source.id)
        manufacturer_id:    Foreign_key(Manufacturer.id)

    Manufacturer table links here.
    Source table is related.
    """
    def __repr__(self):
        """
        Returns a basic representation of a Model table entry.
        """
        return '<Model(name=%s)>' % self.name

    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'))
    name = Column(String(20))
    sources = relationship('Source',
                           order_by='Source.pjlink_name',
                           backref='model',
                           cascade='all, delete-orphan',
                           primaryjoin='Model.id==Source.model_id',
                           lazy='joined')


class Source(CommonBase, Base):
    """
    Projector video source table.

    Source:
        pjlink_name:    Column(String(15))
        pjlink_code:    Column(String(2))
        text:           Column(String(30))
        model_id:       Foreign_key(Model.id)

    Model table links here.

    These entries map PJLink input video source codes to text strings.
    """
    def __repr__(self):
        """
        Return basic representation of Source table entry.
        """
        return '<Source(pjlink_name="%s", pjlink_code="%s", text="%s")>' % \
            (self.pjlink_name, self.pjlink_code, self.text)
    model_id = Column(Integer, ForeignKey('model.id'))
    pjlink_name = Column(String(15))
    pjlink_code = Column(String(2))
    text = Column(String(30))


class Projector(CommonBase, Base):
    """
    Projector table.

    Projector:
        ip:             Column(String(100))  # Allow for IPv6 or FQDN
        port:           Column(String(8))
        pin:            Column(String(20))   # Allow for test strings
        name:           Column(String(20))
        location:       Column(String(30))
        notes:          Column(String(200))
        pjlink_name:    Column(String(128))  # From projector (future)
        manufacturer:   Column(String(128))  # From projector (future)
        model:          Column(String(128))  # From projector (future)
        other:          Column(String(128))  # From projector (future)
        sources:        Column(String(128))  # From projector (future)
    """
    ip = Column(String(100))
    port = Column(String(8))
    pin = Column(String(20))
    name = Column(String(20))
    location = Column(String(30))
    notes = Column(String(200))
    pjlink_name = Column(String(128))
    manufacturer = Column(String(128))
    model = Column(String(128))
    other = Column(String(128))
    sources = Column(String(128))


class ProjectorSource(CommonBase, Base):
    """
    Projector local source table
    This table allows mapping specific projector source input to a local
    connection; i.e., '11': 'DVD Player'

    Projector Source:
        projector_id:   Foreign_key(Column(Projector.id))
        code:           Column(String(3)) #  PJLink source code
        text:           Column(String(20))  # Text to display
    """
    code = Column(String(3))
    text = Column(String(20))
    projector_id = (Integer, ForeignKey('projector.id'))


class ProjectorDB(Manager):
    """
    Class to access the projector database.
    """
    def __init__(self, *args, **kwargs):
        log.debug('ProjectorDB().__init__(args="%s", kwargs="%s")' % (args, kwargs))
        super().__init__(plugin_name='projector',
                         init_schema=self.init_schema)
        log.debug('ProjectorDB() Initialized using db url %s' % self.db_url)

    def init_schema(*args, **kwargs):
        """
        Setup the projector database and initialize the schema.

        Declarative uses table classes to define schema.
        """
        url = init_url('projector')
        session, metadata = init_db(url, base=Base)
        Base.metadata.create_all(checkfirst=True)
        return session

    def get_projector_by_id(self, dbid):
        """
        Locate a DB record by record ID.

        :param dbid: DB record id
        :returns: Projector() instance
        """
        log.debug('get_projector_by_id(id="%s")' % dbid)
        projector = self.get_object_filtered(Projector, Projector.id == dbid)
        if projector is None:
            # Not found
            log.warn('get_projector_by_id() did not find %s' % id)
            return None
        log.debug('get_projectorby_id() returning 1 entry for "%s" id="%s"' % (dbid, projector.id))
        return projector

    def get_projector_all(self):
        """
        Retrieve all projector entries.

        :returns: List with Projector() instances used in Manager() QListWidget.
        """
        log.debug('get_all() called')
        return_list = []
        new_list = self.get_all_objects(Projector)
        if new_list is None or new_list.count == 0:
            return return_list
        for new_projector in new_list:
            return_list.append(new_projector)
        log.debug('get_all() returning %s item(s)' % len(return_list))
        return return_list

    def get_projector_by_ip(self, ip):
        """
        Locate a projector by host IP/Name.

        :param ip: Host IP/Name
        :returns: Projector() instance
        """
        log.debug('get_projector_by_ip(ip="%s")' % ip)
        projector = self.get_object_filtered(Projector, Projector.ip == ip)
        if projector is None:
            # Not found
            log.warn('get_projector_by_ip() did not find %s' % ip)
            return None
        log.debug('get_projectorby_ip() returning 1 entry for "%s" id="%s"' % (ip, projector.id))
        return projector

    def get_projector_by_name(self, name):
        """
        Locate a projector by name field

        :param name: Name of projector
        :returns: Projector() instance
        """
        log.debug('get_projector_by_name(name="%s")' % name)
        projector = self.get_object_filtered(Projector, Projector.name == name)
        if projector is None:
            # Not found
            log.warn('get_projector_by_name() did not find "%s"' % name)
            return None
        log.debug('get_projector_by_name() returning one entry for "%s" id="%s"' % (name, projector.id))
        return projector

    def add_projector(self, projector):
        """
        Add a new projector entry

        :param projector: Projector() instance to add
        :returns: bool
                  True if entry added
                  False if entry already in DB or db error
        """
        old_projector = self.get_object_filtered(Projector, Projector.ip == projector.ip)
        if old_projector is not None:
            log.warn('add_new() skipping entry ip="%s" (Already saved)' % old_projector.ip)
            return False
        log.debug('add_new() saving new entry')
        log.debug('ip="%s", name="%s", location="%s"' % (projector.ip,
                                                         projector.name,
                                                         projector.location))
        log.debug('notes="%s"' % projector.notes)
        return self.save_object(projector)

    def update_projector(self, projector=None):
        """
        Update projector entry

        :param projector: Projector() instance with new information
        :returns: bool
                  True if DB record updated
                  False if entry not in DB or DB error
        """
        if projector is None:
            log.error('No Projector() instance to update - cancelled')
            return False
        old_projector = self.get_object_filtered(Projector, Projector.id == projector.id)
        if old_projector is None:
            log.error('Edit called on projector instance not in database - cancelled')
            return False
        log.debug('(%s) Updating projector with dbid=%s' % (projector.ip, projector.id))
        old_projector.ip = projector.ip
        old_projector.name = projector.name
        old_projector.location = projector.location
        old_projector.pin = projector.pin
        old_projector.port = projector.port
        old_projector.pjlink_name = projector.pjlink_name
        old_projector.manufacturer = projector.manufacturer
        old_projector.model = projector.model
        old_projector.other = projector.other
        old_projector.sources = projector.sources
        return self.save_object(old_projector)

    def delete_projector(self, projector):
        """
        Delete an entry by record id

        :param projector: Projector() instance to delete
        :returns: bool
                  True if record deleted
                  False if DB error
        """
        deleted = self.delete_object(Projector, projector.id)
        if deleted:
            log.debug('delete_by_id() Removed entry id="%s"' % projector.id)
        else:
            log.error('delete_by_id() Entry id="%s" not deleted for some reason' % projector.id)
        return deleted

    def get_source_list(self, projector):
        """
        Retrieves the source inputs pjlink code-to-text if available based on
        manufacturer and model.
        If not available, then returns the PJLink code to default text.

        :param projector: Projector instance
        :returns: dict
                  key: (str) PJLink code for source
                  value: (str) From ProjectorSource, Sources tables or PJLink default code list
        """
        # Get manufacturer-defined source text
        model_list = self.get_all_objects(Model, Model.name == projector.model)
        if model_list is None or len(model_list) < 1:
            # No entry for model, so see if there's a default entry
            default_list = self.get_object_filtered(Manufacturer, Manufacturer.name == projector.manufacturer)
            if default_list is None or len(default_list) < 1:
                # No entry for manufacturer, so can't check for default text
                model_list = {}
            else:
                model_list = default_list.models['DEFAULT']
        # Get user-defined source text
        local_list = self.get_all_objects(ProjectorSource, ProjectorSource.projector_id == projector.dbid)
        if local_list is None or len(local_list) < 1:
            local_list = {}
        source_dict = {}
        for source in projector.source_available:
            if source in local_list:
                # User defined source text
                source_dict[source] = local_list[source]
            elif source in model_list:
                # Default manufacturer defined source text
                source_dict[source] = model_list[source]
            else:
                # Default PJLink source text
                source_dict[source] = PJLINK_DEFAULT_CODES[source]
        return source_dict
