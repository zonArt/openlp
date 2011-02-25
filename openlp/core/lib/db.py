# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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
The :mod:`db` module provides the core database functionality for OpenLP
"""
import logging
import os

from PyQt4 import QtCore
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exceptions import InvalidRequestError
from sqlalchemy.orm import scoped_session, sessionmaker

from openlp.core.utils import AppLocation, delete_file

log = logging.getLogger(__name__)

def init_db(url, auto_flush=True, auto_commit=False):
    """
    Initialise and return the session and metadata for a database

    ``url``
        The database to initialise connection with

    ``auto_flush``
        Sets the flushing behaviour of the session

    ``auto_commit``
        Sets the commit behaviour of the session
    """
    engine = create_engine(url)
    metadata = MetaData(bind=engine)
    session = scoped_session(sessionmaker(autoflush=auto_flush,
        autocommit=auto_commit, bind=engine))
    return session, metadata

def delete_database(plugin_name, db_file_name=None):
    """
    Remove a database file from the system.

    ``plugin_name``
        The name of the plugin to remove the database for

    ``db_file_name``
        The database file name.  Defaults to None resulting in the
        plugin_name being used.
    """
    db_file_path = None
    if db_file_name:
        db_file_path = os.path.join(
            AppLocation.get_section_data_path(plugin_name), db_file_name)
    else:
        db_file_path = os.path.join(
            AppLocation.get_section_data_path(plugin_name), plugin_name)
    return delete_file(db_file_path)

class BaseModel(object):
    """
    BaseModel provides a base object with a set of generic functions
    """
    @classmethod
    def populate(cls, **kwargs):
        """
        Creates an instance of a class and populates it, returning the instance
        """
        instance = cls()
        for key in kwargs:
            instance.__setattr__(key, kwargs[key])
        return instance

class Manager(object):
    """
    Provide generic object persistence management
    """
    def __init__(self, plugin_name, init_schema, db_file_name=None):
        """
        Runs the initialisation process that includes creating the connection
        to the database and the tables if they don't exist.

        ``plugin_name``
            The name to setup paths and settings section names

        ``init_schema``
            The init_schema function for this database

        ``db_file_name``
            The file name to use for this database.  Defaults to None resulting
            in the plugin_name being used.
        """
        settings = QtCore.QSettings()
        settings.beginGroup(plugin_name)
        self.db_url = u''
        self.is_dirty = False
        db_type = unicode(
            settings.value(u'db type', QtCore.QVariant(u'sqlite')).toString())
        if db_type == u'sqlite':
            if db_file_name:
                self.db_url = u'sqlite:///%s/%s' % (
                    AppLocation.get_section_data_path(plugin_name),
                    db_file_name)
            else:
                self.db_url = u'sqlite:///%s/%s.sqlite' % (
                    AppLocation.get_section_data_path(plugin_name), plugin_name)
        else:
            self.db_url = u'%s://%s:%s@%s/%s' % (db_type,
                unicode(settings.value(u'db username').toString()),
                unicode(settings.value(u'db password').toString()),
                unicode(settings.value(u'db hostname').toString()),
                unicode(settings.value(u'db database').toString()))
        settings.endGroup()
        self.session = init_schema(self.db_url)

    def save_object(self, object_instance, commit=True):
        """
        Save an object to the database

        ``object_instance``
            The object to save

        ``commit``
            Commit the session with this object
        """
        try:
            self.session.add(object_instance)
            if commit:
                self.session.commit()
            self.is_dirty = True
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Object save failed')
            return False

    def save_objects(self, object_list, commit=True):
        """
        Save a list of objects to the database

        ``object_list``
            The list of objects to save

        ``commit``
            Commit the session with this object
        """
        try:
            self.session.add_all(object_list)
            if commit:
                self.session.commit()
            self.is_dirty = True
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Object list save failed')
            return False

    def get_object(self, object_class, key=None):
        """
        Return the details of an object

        ``object_class``
            The type of object to return

        ``key``
            The unique reference or primary key for the instance to return
        """
        if not key:
            return object_class()
        else:
            return self.session.query(object_class).get(key)

    def get_object_filtered(self, object_class, filter_clause):
        """
        Returns an object matching specified criteria

        ``object_class``
            The type of object to return

        ``filter_clause``
            The criteria to select the object by
        """
        return self.session.query(object_class).filter(filter_clause).first()

    def get_all_objects(self, object_class, filter_clause=None,
        order_by_ref=None):
        """
        Returns all the objects from the database

        ``object_class``
            The type of objects to return

        ``filter_clause``
            The filter governing selection of objects to return.  Defaults to
            None.

        ``order_by_ref``
            Any parameters to order the returned objects by.  Defaults to None.
        """
        query = self.session.query(object_class)
        if filter_clause is not None:
            query = query.filter(filter_clause)
        if order_by_ref is not None:
            return query.order_by(order_by_ref).all()
        return query.all()

    def get_object_count(self, object_class, filter_clause=None):
        """
        Returns a count of the number of objects in the database.

        ``object_class``
            The type of objects to return.

        ``filter_clause``
            The filter governing selection of objects to return.  Defaults to
            None.
        """
        query = self.session.query(object_class)
        if filter_clause is not None:
            query = query.filter(filter_clause)
        return query.count()

    def delete_object(self, object_class, key):
        """
        Delete an object from the database

        ``object_class``
            The type of object to delete

        ``key``
            The unique reference or primary key for the instance to be deleted
        """
        if key != 0:
            object_instance = self.get_object(object_class, key)
            try:
                self.session.delete(object_instance)
                self.session.commit()
                self.is_dirty = True
                return True
            except InvalidRequestError:
                self.session.rollback()
                log.exception(u'Failed to delete object')
                return False
        else:
            return True

    def delete_all_objects(self, object_class, filter_clause=None):
        """
        Delete all object records

        ``object_class``
            The type of object to delete
        """
        try:
            query = self.session.query(object_class)
            if filter_clause is not None:
                query = query.filter(filter_clause)
            query.delete(synchronize_session=False)
            self.session.commit()
            self.is_dirty = True
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Failed to delete %s records', object_class.__name__)
            return False

    def finalise(self):
        """
        VACUUM the database on exit.
        """
        if self.is_dirty:
            engine = create_engine(self.db_url)
            if self.db_url.startswith(u'sqlite'):
                engine.execute("vacuum")
