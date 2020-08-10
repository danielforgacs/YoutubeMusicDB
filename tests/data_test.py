import os
import psycopg2
import pytest
import app.data as data
import app.youtube as youtube


print('\n[IMPORT]', os.environ['DB_DBNAME'])

os.environ['DB_DBNAME'] = 'ymdb_test'
print('\n[IMPORT AFTER UPDATE]', os.environ['DB_DBNAME'])



# def setup_module():
#     print('\n[SETUP]', os.environ['DB_DBNAME'])

#     with data.PGConnection(dbname='postgres') as conn1:
#         conn1.set_isolation_level(
#             psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#         cur = conn1.cursor()
#         cur.execute(query="create database ymdb_test;")

#     with data.PGConnection() as conn1:
#         conn1.set_isolation_level(
#             psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#         cur = conn1.cursor()
#         cur.execute(query="""
# CREATE TABLE playlist (
#     id              SMALLSERIAL     PRIMARY KEY,
#     youtubeid       TEXT            NOT NULL UNIQUE,
#     title           TEXT            NOT NULL,
#     uploaderid      TEXT            NOT NULL
# )
# ;

# CREATE TABLE song (
#     id              SMALLSERIAL     PRIMARY KEY,
#     title           TEXT            NOT NULL,
#     youtubeid       TEXT            NOT NULL UNIQUE,
#     playlist        INTEGER         REFERENCES playlist
# )
# ;
# """
#     )




# def teardown_module():
#     print('\n[TEARDOWN]', os.environ['DB_DBNAME'])

#     with data.PGConnection(dbname='postgres') as conn1:
#         conn1.set_isolation_level(
#             psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#         cur = conn1.cursor()
#         cur.execute(query="drop database ymdb_test;")






@pytest.fixture
def conn():
    print('\n[CONN]', os.environ['DB_DBNAME'])

    # with data.PGConnection(dbname='ymdb_test') as conn:
    with data.PGConnection() as conn:
        yield conn




def test_insert_playlist(conn):
    print('\n[TEST001]', os.environ['DB_DBNAME'])
    playlist = youtube.Playlist(attrs={})
    playlist.id = 'youtube-id-01'
    playlist.title = 'playlist-title-01'
    playlist.uploader_id = 'updloader-id-01'

    data.insert_playlist(playlist=playlist)

    cur = conn.cursor()
    cur.execute(query="""
        SELECT
            youtubeid,
            title,
            uploaderid
        FROM
            playlist
        WHERE
            youtubeid = %s
        ;
    """, vars=('youtube-id-01',))
    result = cur.fetchall()
    cur.close()

    assert result[0][0] == 'youtube-id-01'
    assert result[0][1] == 'playlist-title-01'
    assert result[0][2] == 'updloader-id-01'




if __name__ == '__main__':
    pass
