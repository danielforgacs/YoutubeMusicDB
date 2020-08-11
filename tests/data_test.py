import os
import psycopg2
import pytest
import app.data as data
import app.youtube as youtube


# print('\n[IMPORT]', os.environ['PGDATABASE'])

os.environ['PGDATABASE'] = 'ymdb_test'
# print('\n[IMPORT AFTER UPDATE]', os.environ['PGDATABASE'])



PLAYLIST_DATA = [
    ['youtube-id-01', 'playlist-title-01', 'updloader-id-01'],
    ['youtube-id-01', 'playlist-title-01-B', 'updloader-id-01'],
    ['youtube-id-01', 'playlist-title-01', 'updloader-id-01-C'],
    ['youtube-id-01', 'playlist-title-01-D', 'updloader-id-01-D'],

    ['youtube-id-02', 'playlist-title-02', 'updloader-id-02'],
]



# def setup_module():
#     print('\n[SETUP]', os.environ['PGDATABASE'])

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
#     print('\n[TEARDOWN]', os.environ['PGDATABASE'])

#     with data.PGConnection(dbname='postgres') as conn1:
#         conn1.set_isolation_level(
#             psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#         cur = conn1.cursor()
#         cur.execute(query="drop database ymdb_test;")






@pytest.fixture
def conn():
    print('\n[CONN]', os.environ['PGDATABASE'])

    # with data.PGConnection(dbname='ymdb_test') as conn:
    with data.PGConnection() as conn:
        yield conn




@pytest.mark.parametrize('pldata', PLAYLIST_DATA)
def test_insert_playlist(conn, pldata):
    print('\n[TEST001]', os.environ['PGDATABASE'])
    playlist = youtube.Playlist(attrs={})
    playlist.id = pldata[0]
    playlist.title = pldata[1]
    playlist.uploader_id = pldata[2]
    playlist.entries = []

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
    """, vars=(pldata[0],))
    result = cur.fetchall()
    cur.close()

    assert result[0][0] == pldata[0]
    assert result[0][1] == pldata[1]
    assert result[0][2] == pldata[2]




if __name__ == '__main__':
    pass
