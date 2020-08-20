import logging

import app as application
from db import db_connection


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
                    datefmt='%Y-%m-%dT%H:%M:%S')
logger = logging.getLogger(__name__)


def init():
    try:
        db_connection.test_connection()
        db_connection.create_tables()
    except Exception as e:
        logger.error(e)
        raise e

    logger.info("Application initialized")
    return application.start()


app = init()
