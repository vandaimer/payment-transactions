import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

log = logging.getLogger(__name__)
BaseSQLAlchemy = declarative_base()


class DB:
    def __init__(self):
        self.connection_string = 'postgresql://%s:%s@%s:%s/%s' % (DB_USER,
                                                                  DB_PASSWORD,
                                                                  DB_HOST,
                                                                  DB_PORT,
                                                                  DB_NAME)
        self.engine = create_engine(self.connection_string)

    def create_tables(self):
        BaseSQLAlchemy.metadata.create_all(self.engine)

    def session(self):
        """
        Creates a new SessionContext - not a SQLAlchemy Session.

        To get the SQLAlchemy session the session context should be used with a context_manager
        or access the SessionContext.session object
        """
        return SessionContext(sessionmaker(self.engine))


class SessionContext:
    """
    This class is a simple context manager around to session to take care of commit/rollback
    pending operations.
    """
    def __init__(self, session):
        self.session = session()

    def __enter__(self):
        log.info("Entering session context")
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        if not traceback:
            log.info("Committing db session pending operations")
            self.session.commit()
        else:
            log.error("Error during db session, rolling back pending operations")
            self.session.rollback()
