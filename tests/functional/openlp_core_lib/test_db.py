"""
Package to test the openlp.core.lib package.
"""
from unittest import TestCase

from mock import MagicMock, patch
from sqlalchemy.pool import NullPool
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy import MetaData

from openlp.core.lib.db import init_db, get_upgrade_op


class TestDB(TestCase):
    """
    A test case for all the tests for the :mod:`~openlp.core.lib.db` module.
    """
    def init_db_calls_correct_functions_test(self):
        """
        Test that the init_db function makes the correct function calls
        """
        # GIVEN: Mocked out SQLAlchemy calls and return objects, and an in-memory SQLite database URL
        with patch('openlp.core.lib.db.create_engine') as mocked_create_engine, \
            patch('openlp.core.lib.db.MetaData') as MockedMetaData, \
            patch('openlp.core.lib.db.sessionmaker') as mocked_sessionmaker, \
            patch('openlp.core.lib.db.scoped_session') as mocked_scoped_session:
            mocked_engine = MagicMock()
            mocked_metadata = MagicMock()
            mocked_sessionmaker_object = MagicMock()
            mocked_scoped_session_object = MagicMock()
            mocked_create_engine.return_value = mocked_engine
            MockedMetaData.return_value = mocked_metadata
            mocked_sessionmaker.return_value = mocked_sessionmaker_object
            mocked_scoped_session.return_value = mocked_scoped_session_object
            db_url = 'sqlite://'

            # WHEN: We try to initialise the db
            session, metadata = init_db(db_url)

            # THEN: We should see the correct function calls
            mocked_create_engine.assert_called_with(db_url, poolclass=NullPool)
            MockedMetaData.assert_called_with(bind=mocked_engine)
            mocked_sessionmaker.assert_called_with(autoflush=True, autocommit=False, bind=mocked_engine)
            mocked_scoped_session.assert_called_with(mocked_sessionmaker_object)
            self.assertIs(session, mocked_scoped_session_object, 'The ``session`` object should be the mock')
            self.assertIs(metadata, mocked_metadata, 'The ``metadata`` object should be the mock')

    def init_db_defaults_test(self):
        """
        Test that initialising an in-memory SQLite database via ``init_db`` uses the defaults
        """
        # GIVEN: An in-memory SQLite URL
        db_url = 'sqlite://'

        # WHEN: The database is initialised through init_db
        session, metadata = init_db(db_url)

        # THEN: Valid session and metadata objects should be returned
        self.assertIsInstance(session, ScopedSession, 'The ``session`` object should be a ``ScopedSession`` instance')
        self.assertIsInstance(metadata, MetaData, 'The ``metadata`` object should be a ``MetaData`` instance')

    def get_upgrade_op_test(self):
        """
        Test that the ``get_upgrade_op`` function creates a MigrationContext and an Operations object
        """
        # GIVEN: Mocked out alembic classes and a mocked out SQLAlchemy session object
        with patch('openlp.core.lib.db.MigrationContext') as MockedMigrationContext, \
                patch('openlp.core.lib.db.Operations') as MockedOperations:
            mocked_context = MagicMock()
            mocked_op = MagicMock()
            mocked_connection = MagicMock()
            MockedMigrationContext.configure.return_value = mocked_context
            MockedOperations.return_value = mocked_op
            mocked_session = MagicMock()
            mocked_session.bind.connect.return_value = mocked_connection

            # WHEN: get_upgrade_op is executed with the mocked session object
            op = get_upgrade_op(mocked_session)

            # THEN: The op object should be mocked_op, and the correction function calls should have been made
            self.assertIs(op, mocked_op, 'The return value should be the mocked object')
            mocked_session.bind.connect.assert_called_with()
            MockedMigrationContext.configure.assert_called_with(mocked_connection)
            MockedOperations.assert_called_with(mocked_context)
