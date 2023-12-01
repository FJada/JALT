import pytest

import data.db_connect as dbc

TEST_DB = dbc.METRO_DB
TEST_COLLECT = 'test_collect'
# can be used for field and value:
TEST_NAME = 'test'


@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    dbc.insert_one(TEST_COLLECT, {TEST_NAME: TEST_NAME}, TEST_DB)
    # yield to our test function
    yield
    dbc.del_one(TEST_COLLECT, {TEST_NAME: TEST_NAME}, TEST_DB)


def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: TEST_NAME}, TEST_DB)
    assert ret is not None


def test_fetch_one_not_there(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: 'not a field value in db!'}, TEST_DB)
    assert ret is None
