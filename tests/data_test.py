import os
import psycopg2
import pytest
import app.data as data
import app.youtube as youtube




TEST_DB_NAME = 'ymdb_test'
os.environ['PGDATABASE'] = TEST_DB_NAME
SCHEMA_FILE = os.path.join(os.getcwd(), 'sql', 'schema.sql')
PLAYLIST_DATA = [{
        'id': 'youtubeid_{}'.format(idx),
        'title': 'title_{}'.format(idx),
        'uploader_id': 'uploaderid_{}'.format(idx),
    } for idx in range(3)
]






def setup_module():
    with open(SCHEMA_FILE, 'r') as schemafile:
        schemasql = schemafile.read()

    with data.PGConnection(dbname='postgres') as conn1:
        conn1.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn1.cursor()
        try:
            cur.execute(query="drop database %s;" % TEST_DB_NAME)
        except psycopg2.errors.InvalidCatalogName:
            pass
        cur.execute(query="create database %s;" % TEST_DB_NAME)

    with data.PGConnection() as conn2:
        conn2.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn2.cursor()
        cur.execute(query=schemasql)




def teardown_module():
    with data.PGConnection(dbname='postgres') as conn1:
        conn1.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn1.cursor()
        cur.execute(query="drop database %s;" % TEST_DB_NAME)




@pytest.fixture
def conn():
    with data.PGConnection() as conn:
        assert conn.info.dbname == TEST_DB_NAME
        yield conn



def test_test_db_is_ready(conn):
    pass


@pytest.mark.parametrize('pldata', PLAYLIST_DATA)
def test_insert_playlist(conn, pldata):
    plid = data.insert_playlist(pldict=pldata)

    assert isinstance(plid, int)

    cur = conn.cursor()
    cur.execute(query="""
        SELECT youtubeid, title, uploaderid
        FROM playlist
        WHERE youtubeid = %(id)s
        ;
    """, vars=pldata)
    result = cur.fetchone()
    cur.close()

    assert result[0] == pldata['id']
    assert result[1] == pldata['title']
    assert result[2] == pldata['uploader_id']




if __name__ == '__main__':
    pass
