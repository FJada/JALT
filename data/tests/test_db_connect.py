import pytest
import logging

import data.db_connect as dbc

TEST_DB = dbc.METRO_DB
TEST_COLLECT = 'test_collect'
# can be used for field and value:
TEST_NAME = 'test'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def temp_rec():
    try:
        dbc.connect_db()
        dbc.insert_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
        # yield to our test function
        yield
    finally:
        dbc.del_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})

def test_fetch_one(temp_rec):
    try:
        ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
        assert ret is not None
    except Exception as e:
        logger.error(f"Error in test_fetch_one: {e}")
        raise

def test_fetch_one_not_there(temp_rec):
    try:
        ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: 'not a field value in db!'})
        assert ret is None
    except Exception as e:
        logger.error(f"Error in test_fetch_one_not_there: {e}")
        raise
