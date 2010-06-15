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
"""
The :mod:`db` module provides the core database functionality for OpenLP
"""
import logging

from PyQt4 import QtCore
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exceptions import InvalidRequestError
from sqlalchemy.orm import scoped_session, sessionmaker

from openlp.core.utils import AppLocation

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

class BaseModel(object):
    """
    BaseModel provides a base object with a set of generic functions
    """

    @classmethod
    def populate(cls, **kwargs):
        """
        Creates an instance of a class and populates it, returning the instance
        """
        me = cls()
        for key in kwargs:
            me.__setattr__(key, kwargs[key])
        return me

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

    def delete_database(self, plugin_name, db_file_name=None):
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
        try:
            os.remove(db_file_path)
            return True
        except OSError:
            return False

    def insert_object(self, object_instance):
        """
        Save an object to the database

        ``object_instance``
            The object to save
        """
        try:
            self.session.add(object_instance)
            self.session.commit()
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Object save failed')
            return False

    def get_object(self, object_class, id=None):
        """
        Return the details of an object

        ``object_class``
            The type of object to return

        ``id``
            The unique reference for the class instance to return
        """
        if not id:
            return object_class()
        else:
            return self.session.query(object_class).get(id)

    def get_object_filtered(self, object_class, filter_string):
        """
        Returns an object matching specified criteria

        ``object_class``
            The type of object to return

        ``filter_string``
            The criteria to select the object by
        """
        return self.session.query(object_class).filter(filter_string).first()

    def get_all_objects(self, object_class, order_by_ref=None):
        """
        Returns all the objects from the database

        ``object_class``
            The type of objects to return

        ``order_by_ref``
            Any parameters to order the returned objects by.  Defaults to None.
        """
        if order_by_ref:
            return self.session.query(object_class).order_by(order_by_ref).all()
        return self.session.query(object_class).all()

    def get_all_objects_filtered(self, object_class, filter_string):
        """
        Returns a selection of objects from the database

        ``object_class``
            The type of objects to return

        ``filter_string``
            The filter governing selection of objects to return
        """
        return self.session.query(object_class).filter(filter_string).all()

    def delete_object(self, object_class, id):
        """
        Delete an object from the database

        ``object_class``
            The type of object to delete

        ``id``
            The unique reference for the class instance to be deleted
        """
        if id != 0:
            object = self.get_object(object_class, id)
            try:
                self.session.delete(object)
                self.session.commit()
                return True
            except InvalidRequestError:
                self.session.rollback()
                log.exception(u'Failed to delete object')
                return False
        else:
            return True

    def delete_all_objects(self, object_class):
        """
        Delete all object records

        ``object_class``
            The type of object to delete
        """
        try:
            self.session.query(object_class).delete(synchronize_session=False)
            self.session.commit()
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Failed to delete all %s records',
                object_class.__name__)
            return False
