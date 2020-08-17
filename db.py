from typing import Any, Generator
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr


from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


class DB:
    def __init__(self):
        self.connection_string = 'postgresql://%s:%s@%s:%s/%s' % (DB_USER,
                                                                  DB_PASSWORD,
                                                                  DB_HOST,
                                                                  DB_PORT,
                                                                  DB_NAME)
        self.engine = create_engine(self.connection_string)

    def session(self):
        session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return session()

    def test_connection(self):
        session = self.session()
        session.execute("SELECT 1")
        session.close()

    def create_tables(self):
        return BaseSQLAlchemy.metadata.create_all(self.engine)


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
