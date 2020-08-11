import os
import psycopg2
import pytest
import app.data as data
import app.youtube as youtube




TEST_DB_NAME = 'ymdb_test'
os.environ['PGDATABASE'] = TEST_DB_NAME
SCHEMA_FILE = os.path.join(os.getcwd(), 'sql', 'schema.sql')
PLAYLIST_DATA = [{
        'youtubeid': 'youtubeid_{}'.format(idx),
        'title': 'title_{}'.format(idx),
        'uploaderid': 'uploaderid_{}'.format(idx),
    } for idx in range(1)
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
        yield conn



def test_test_db_is_ready(conn):
    pass


# @pytest.mark.parametrize('pldata', PLAYLIST_DATA)
# def test_insert_playlist(conn, pldata):
#     playlist = youtube.Playlist(attrs={})
#     playlist.id = pldata[0]
#     playlist.title = pldata[1]
#     playlist.uploader_id = pldata[2]
#     playlist.entries = []

#     plid = data.insert_playlist(playlist=playlist)

#     assert isinstance(plid, int)

#     cur = conn.cursor()
#     cur.execute(query="""
#         SELECT
#             youtubeid,
#             title,
#             uploaderid
#         FROM
#             playlist
#         WHERE
#             youtubeid = %s
#         ;
#     """, vars=(pldata[0],))
#     result = cur.fetchall()
#     cur.close()

#     assert result[0][0] == pldata[0]
#     assert result[0][1] == pldata[1]
#     assert result[0][2] == pldata[2]




if __name__ == '__main__':
    pass
