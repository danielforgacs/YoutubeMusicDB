import os
import psycopg2
import pytest
import app.data as data
import app.youtube as youtube




TEST_DB_NAME = 'ymdb_test'
os.environ['PGDATABASE'] = TEST_DB_NAME
SCHEMA_FILE = os.path.join(os.getcwd(), 'sql', 'schema.sql')
PLAYLIST_DATA = [{
        'id': 'pl-id_{}'.format(idx),
        'title': 'pl-title_{}'.format(idx),
        'uploader_id': 'pl-uploader_id_{}'.format(idx),
    } for idx in range(3)
]
VIDEO_DATA = [
    {
        'id': 'v-id_{}'.format(idx),
        'title': 'v-title_{}'.format(idx),
        # 'playlist': 1,
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




# def teardown_module():
#     with data.PGConnection(dbname='postgres') as conn1:
#         conn1.set_isolation_level(
#             psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#         cur = conn1.cursor()
#         cur.execute(query="drop database %s;" % TEST_DB_NAME)




@pytest.fixture
def conn():
    with data.PGConnection() as conn:
        assert conn.info.dbname == TEST_DB_NAME
        yield conn



def test_test_db_is_ready(conn):
    pass


@pytest.mark.parametrize('pldata', PLAYLIST_DATA)
def test_insert_playlist(conn, pldata):
    plpk = data.insert_playlist(pldict=pldata)

    assert isinstance(plpk, int)

    cur = conn.cursor()
    cur.execute(query="""
        SELECT pk, id, title, uploader_id
        FROM playlist
        WHERE id = %(id)s
        ;
    """, vars=pldata)
    result = cur.fetchone()
    cur.close()

    assert result[data.IDX_PLAYLIST__pk] == plpk
    assert result[data.IDX_PLAYLIST__id] == pldata['id']
    assert result[data.IDX_PLAYLIST__title] == pldata['title']
    assert result[data.IDX_PLAYLIST__uploader_id] == pldata['uploader_id']



def test_playlist_insert_updates_data_if_playlist_extsts(conn):
    playlist = PLAYLIST_DATA[0]
    newtitle = 'new_title'
    plpk = data.insert_playlist(pldict=playlist)

    playlist['title'] = newtitle
    plpk2 = data.insert_playlist(pldict=playlist)

    assert plpk == plpk2

    cur = conn.cursor()
    cur.execute(query="""
        SELECT pk, id, title, uploader_id
        FROM playlist
        WHERE id = %(id)s
        ;
    """, vars=playlist)
    result = cur.fetchall()
    cur.close()

    assert len(result) == 1
    assert result[0][data.IDX_PLAYLIST__title] == newtitle



@pytest.mark.parametrize('vdata', VIDEO_DATA)
def test_insert_video(conn, vdata):
    vpk = data.insert_video(vdata=vdata)

    assert isinstance(vpk, int)

    cur = conn.cursor()
    cur.execute("""
        SELECT pk, id, title, playlist
        FROM video
        WHERE id = %(id)s
    ;
    """, vars=vdata)
    result = cur.fetchall()
    cur.close()

    assert len(result) == 1
    assert result[0][data.IDX_VIDEO__pk] == vpk
    assert result[0][data.IDX_VIDEO__id] == vdata['id']
    assert result[0][data.IDX_VIDEO__title] == vdata['title']
    assert result[0][data.IDX_VIDEO__playlist] == vdata['playlist']




def test_get_video_ids_by_playlist(conn):
    plpk1 = data.insert_playlist(pldict=PLAYLIST_DATA[0])
    plpk2 = data.insert_playlist(pldict=PLAYLIST_DATA[1])
    videodata1 = VIDEO_DATA[0]
    videodata2 = VIDEO_DATA[1]
    videodata3 = VIDEO_DATA[2]
    videodata1['playlist'] = plpk1
    videodata2['playlist'] = plpk1
    videodata3['playlist'] = plpk2
    vpk1 = data.insert_video(vdata=videodata1)
    vpk2 = data.insert_video(vdata=videodata2)
    vpk3 = data.insert_video(vdata=videodata3)
    videoids1 = data.query_videos_by_playlistid(
        playlistid=PLAYLIST_DATA[0]['id'])
    videoids2 = data.query_videos_by_playlistid(
        playlistid=PLAYLIST_DATA[1]['id'])

    assert videoids1 == [videodata1['id'], videodata2['id']]
    assert videoids2 == [videodata3['id']]





def test_set_video_playlist_sets_updates(conn):
    sql = """
        SELECT pk, id, title, playlist
        FROM video
        WHERE video.id = %(vid)s
        ;
    """
    cur = conn.cursor()
    videodata = VIDEO_DATA[0]
    plpk1 = data.insert_playlist(pldict=PLAYLIST_DATA[0])
    plpk2 = data.insert_playlist(pldict=PLAYLIST_DATA[1])
    data.insert_video(vdata=videodata)

    vpk, plpk = data.set_video_playlist(vid=videodata['id'], plpk=plpk1)

    cur.execute(query=sql, vars={'vid': videodata['id']})
    result = cur.fetchone()
    print('## test:', result)
    # print(result, )
    # print(result, )
    # print(result, )

    assert result[data.IDX_VIDEO__playlist] == plpk1

    vpk, plpk = data.set_video_playlist(vid=videodata['id'], plpk=plpk2)

    cur.execute(query=sql, vars={'vid': videodata['id']})
    result = cur.fetchone()

    assert result[data.IDX_VIDEO__playlist] == plpk2

    plpk3 = None

    vpk, plpk = data.set_video_playlist(vid=videodata['id'], plpk=plpk3)

    cur.execute(query=sql, vars={'vid': videodata['id']})
    result = cur.fetchone()

    assert result[data.IDX_VIDEO__playlist] == plpk3






if __name__ == '__main__':
    pass
