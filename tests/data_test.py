import os
import psycopg2
import pytest
import app.data as data



def setup_module():
    with data.PGConnection(dbname='postgres') as conn1:
        conn1.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn1.cursor()
        cur.execute(query="create database test_db;")

def teardown_module():
    with data.PGConnection(dbname='postgres') as conn1:
        conn1.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn1.cursor()
        cur.execute(query="drop database test_db;")


@pytest.fixture
def conn():
    with data.PGConnection(dbname='test_db') as conn:
        yield conn


def test_aslkdfhj(conn):
    print('-- test_aslkdfhj', conn)

def test_aslkasjhdf(conn):
    print('-- test_aslkasjhdf', conn)

def test_sdkfg7fghg(conn):
    print('-- test_sdkfg7fghg', conn)


# conn = psycopg2.connect(
#     host=os.getenv('DB_HOST'),
#     port=os.getenv('DB_PORT'),
#     dbname=os.getenv('DB_DBNAME'),
#     user=os.getenv('DB_USER'),
#     password=os.getenv('DB_PASSWORD'),
# )



# def _test_can_create_playlist():
#     title = 'test-playlist-01'
#     ytid = 'id-01'

#     data.create_playlist(
#         title=title,
#         ytid=ytid,
#     )

#     cur = conn.cursor()
#     cur.execute(query="""
#         SELECT
#             title,
#             youtubeid
#         FROM
#             playlist
#         WHERE
#             title = %s
#         ;
#     """, vars=(title,))
#     result = cur.fetchall()
#     cur.close()

#     assert len(result) == 1
#     assert result[0][0] == title
#     assert result[0][1] == ytid
