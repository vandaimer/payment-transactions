import logging

from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


log = logging.getLogger(__name__)


class DB:
    def __init__(self):
        self.connection_string = 'postgresql://%s:%s@%s:%s/%s' % (DB_USER,
                                                                  DB_PASSWORD,
                                                                  DB_HOST,
                                                                  DB_PORT,
                                                                  DB_NAME)
        self.engine = create_engine(self.connection_string)

    def session(self):
        return SessionContext(sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)).session

    def test_connection(self):
        session = self.session()
        session.execute("SELECT 1")
        session.close()

    def create_tables(self):
        return BaseSQLAlchemy.metadata.create_all(self.engine)


class SessionContext:
    """
    This class is a simple context manager
    around to session to take care of commit/rollback
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
            log.error("""
                Error during db session, rolling back pending operations
            """)
            self.session.rollback()


db_connection = DB()


@as_declarative()
class BaseSQLAlchemy:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def async_session():
    try:
        session = db_connection.session()
        yield session
    finally:
        session.close()
