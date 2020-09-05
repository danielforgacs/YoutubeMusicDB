import pytest
import dbaccess.dbfuncs as dbf
import tests.setup


VIDEO_COLUMNS = [
    dbf.VIDEO_COLUMN_NAME__pk,
    dbf.VIDEO_COLUMN_NAME__id,
    dbf.VIDEO_COLUMN_NAME__title,
    dbf.VIDEO_COLUMN_NAME__playlist_id,
    dbf.VIDEO_COLUMN_NAME__added,
    dbf.VIDEO_COLUMN_NAME__is_down,
    dbf.VIDEO_COLUMN_NAME__playlist_title,
    dbf.VIDEO_COLUMN_NAME__playlist_data,
]


def setup():
    tests.setup.init_test_db()



def test_select_all_videos_empty_db():
    data = dbf.select_all_videos()
    expected = []

    assert data == expected



def test_select_all_videos_03():
    tests.setup.run_sql_file(sqlfile='testData')
    expected = [
        {
            'pk': index,
            'id': 'id{}'.format(index),
            'title': 'title{}'.format(index),
            'playlistid': None,
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': None,
        } for index in range(1, 11)
    ]
    expected[1]['playlistid'] = 'plid1'
    expected[1]['playlisttitle'] = 'pltitle1'
    expected[3]['playlistid'] = 'plid2'
    expected[3]['playlisttitle'] = 'pltitle2'
    expected[4]['playlistid'] = 'plid2'
    expected[4]['playlisttitle'] = 'pltitle2'

    data = dbf.select_all_videos()

    assert len(data) == len(expected)
    assert data == expected




def test_select_videos_by_id():
    tests.setup.run_sql_file(sqlfile='testData')
    expected = [
        {
            'pk': index,
            'id': 'id{}'.format(index),
            'title': 'title{}'.format(index),
            'playlistid': None,
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': None,
        } for index in [2, 4, 5]
    ]
    expected[0]['playlistid'] = 'plid1'
    expected[0]['playlisttitle'] = 'pltitle1'
    expected[1]['playlistid'] = 'plid2'
    expected[1]['playlisttitle'] = 'pltitle2'
    expected[2]['playlistid'] = 'plid2'
    expected[2]['playlisttitle'] = 'pltitle2'

    data = dbf.select_videos_by_id(vids=('id2', 'id4','id5'))

    assert data == expected



def test_set_video_as_downloaded():
    tests.setup.run_sql_file(sqlfile='testData')
    expected = {'id5': {
        'pk': 5,
        'id': 'id5',
        'title': 'title5',
        'playlistid': 'plid2',
        'added': '2000-01-01 00:00:00',
        'is_down': True,
        'playlisttitle': 'pltitle2',
    }}
    data = dbf.set_video_as_downloaded(vid='id5')

    assert data == expected




def test_set_video_playlist():
    tests.setup.run_sql_file(sqlfile='testData')
    vid = 'id1'
    video = dbf.select_videos_by_id(vids=(vid,))

    assert video[0]['playlistid'] is None
    assert video[0]['playlisttitle'] is None

    plpk = 1
    result = dbf.set_video_playlist(vid=vid, plpk=plpk)
    video = dbf.select_videos_by_id(vids=(vid,))

    assert video[0]['playlistid'] == 'plid1'
    assert video[0]['playlisttitle'] == 'pltitle1'

    plpk = 2
    result = dbf.set_video_playlist(vid=vid, plpk=plpk)
    video = dbf.select_videos_by_id(vids=(vid,))

    assert video[0]['playlistid'] == 'plid2'
    assert video[0]['playlisttitle'] == 'pltitle2'




@pytest.mark.parametrize('plid, expected', (
    ('plid0', []),
    ('plid1', ['id2']),
    ('plid2', ['id4', 'id5']),
))
def test_select_videos_by_playlistid(plid, expected):
    tests.setup.run_sql_file(sqlfile='testData')
    result = dbf.select_videos_by_playlistid(playlistid=plid)
    vids = [video['id'] for video in result]

    assert vids == expected




def test_insert_video():
    video = {
        'id': 'new_vid_id_1',
        'title': 'new_vid_title_1',
    }
    result = dbf.insert_video(vdata=video)

    assert list(result.keys()) == [video['id']]
    assert list(result[video['id']].keys()) == [
        'pk', 'id', 'title', 'playlistid', 'added', 'is_down', 'playlisttitle']
    assert result[video['id']]['id'] == video['id']
    assert result[video['id']]['title'] == video['title']




@pytest.mark.parametrize('plids', (
    ('plid1',),
    ('plid2',),
    ('plid1', 'plid2'),
))
def test_select_playlists_by_id(plids):
    tests.setup.run_sql_file(sqlfile='testData')
    expected = list(plids)
    result = dbf.select_playlists_by_id(plids=plids)

    assert [pl['id'] for pl in result] == expected




@pytest.mark.parametrize('pldict', (
    {
        'id': 'pl_id_1',
        'title': 'pl_title_1',
        'uploader_id': 'pl_uploader_id_1',
    },
    {
        'id': 'pl_id_2',
        'title': 'pl_title_2',
        'uploader_id': 'pl_uploader_id_2',
    },
))
def test_insert_playlist(pldict):
    result = dbf.insert_playlist(pldict=pldict)

    assert len(result) == 1
    assert list(result.keys()) == [pldict['id']]
    assert list(result[pldict['id']].keys()) == [
        'pk', 'id', 'title', 'uploader_id', 'added']
    assert result[pldict['id']]['id'] == pldict['id']
    assert result[pldict['id']]['title'] == pldict['title']
    assert result[pldict['id']]['uploader_id'] == pldict['uploader_id']




@pytest.mark.parametrize('pldata', tests.setup.PLAYLIST_DATA)
def test_insert_playlist(pldata):
    newplist = dbf.insert_playlist(pldict=pldata)
    plpk = newplist[0]

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query="""
            SELECT pk, id, title, uploader_id
            FROM playlist
            WHERE id = %(id)s
            ;
        """, vars=pldata)
        result = cur.fetchone()

    assert result[dbf.PLAYLIST_COLUMNT_IDX__pk] == plpk['pk']
    assert result[dbf.PLAYLIST_COLUMNT_IDX__id] == pldata['id']
    assert result[dbf.PLAYLIST_COLUMNT_IDX__title] == pldata['title']
    assert result[dbf.PLAYLIST_COLUMNT_IDX__uploader_id] == pldata['uploader_id']



def test_playlist_insert_updates_data_if_playlist_extsts():
    playlist = dict(tests.setup.PLAYLIST_DATA[0])
    newtitle = 'new_title'
    result = dbf.insert_playlist(pldict=playlist)
    plpk = result[0]['pk']

    playlist['title'] = newtitle
    result2 = dbf.insert_playlist(pldict=playlist)
    plpk2 = result[0]['pk']

    assert plpk == plpk2

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query="""
            SELECT pk, id, title, uploader_id
            FROM playlist
            WHERE id = %(id)s
            ;
        """, vars=playlist)
        result = cur.fetchall()

    assert len(result) == 1
    assert result[0][dbf.PLAYLIST_COLUMNT_IDX__title] == newtitle



@pytest.mark.parametrize('vdata', tests.setup.VIDEO_DATA)
def test_insert_video(vdata):
    result = dbf.insert_video(vdata=vdata)
    vpk = [video for video in result][0]

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT pk, id, title, playlist_pk
            FROM video
            WHERE id = %(id)s
        ;
        """, vars=vdata)
        result = cur.fetchall()

    assert len(result) == 1
    assert result[0][dbf.VIDEO_COLUMN_IDX__pk] == vpk['pk']
    assert result[0][dbf.VIDEO_COLUMN_IDX__id] == vdata['id']
    assert result[0][dbf.VIDEO_COLUMN_IDX__title] == vdata['title']
    assert result[0][dbf.VIDEO_COLUMN_IDX__playlist_id] == vdata['playlist_pk']




def test_get_video_ids_by_playlist():
    result1 = dbf.insert_playlist(pldict=dict(tests.setup.PLAYLIST_DATA[0]))
    plpk1 = result1[0]
    result2 = dbf.insert_playlist(pldict=dict(tests.setup.PLAYLIST_DATA[1]))
    plpk2 = result2[0]
    videodata1 = dict(tests.setup.VIDEO_DATA[0])
    videodata2 = dict(tests.setup.VIDEO_DATA[1])
    videodata3 = dict(tests.setup.VIDEO_DATA[2])
    videodata1['playlist_pk'] = plpk1['pk']
    videodata2['playlist_pk'] = plpk1['pk']
    videodata3['playlist_pk'] = plpk2['pk']
    vpk1 = dbf.insert_video(vdata=videodata1)
    vpk2 = dbf.insert_video(vdata=videodata2)
    vpk3 = dbf.insert_video(vdata=videodata3)
    videoids1_raw = dbf.select_videos_by_playlistid(
        playlistid=dict(tests.setup.PLAYLIST_DATA[0])['id'])
    videoids1 = [video for video in videoids1_raw]
    videoids2_raw = dbf.select_videos_by_playlistid(
        playlistid=dict(tests.setup.PLAYLIST_DATA[1])['id'])
    videoids2 = [video for video in videoids2_raw]

    assert [vid['id'] for vid in videoids1] == [videodata1['id'], videodata2['id']]
    assert [vid['id'] for vid in videoids2] == [videodata3['id']]





def test_set_video_playlist_sets_updates():
    sql = """
        SELECT pk, id, title, playlist_pk
        FROM video
        WHERE video.id = %(vid)s
        ;
    """
    videodata = dict(tests.setup.VIDEO_DATA[0])

    res1 = dbf.insert_playlist(pldict=tests.setup.PLAYLIST_DATA[0])
    plpk1 = res1[0]
    res2 = dbf.insert_playlist(pldict=tests.setup.PLAYLIST_DATA[1])
    plpk2 = res2[0]
    vpk = dbf.insert_video(vdata=videodata)

    res3 = dbf.set_video_playlist(vid=videodata['id'], plpk=plpk1['pk'])
    result = [video for video in res3][0]
    vpk = result['pk']
    vid = result['id']
    plpk = result['playlistid']

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars={'vid': videodata['id']})
        result = cur.fetchone()

    assert result[dbf.VIDEO_COLUMN_IDX__playlist_id] == plpk1['pk']
    assert result[dbf.VIDEO_COLUMN_IDX__pk] == vpk

    result5 = dbf.set_video_playlist(vid=videodata['id'], plpk=plpk2['pk'])
    result = [video for video in result5][0]
    vpk = result['pk']
    vid = result['id']
    plpk = result['playlistid']

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars={'vid': videodata['id']})
        result = cur.fetchone()

    assert result[dbf.VIDEO_COLUMN_IDX__playlist_id] == plpk2['pk']
    assert result[dbf.VIDEO_COLUMN_IDX__pk] == vpk

    plpk3 = None

    result6 = dbf.set_video_playlist(vid=videodata['id'], plpk=plpk3)
    result = [video for video in result6][0]
    vpk = result['pk']
    vid = result['id']
    plpk = result['playlistid']

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars={'vid': videodata['id']})
        result = cur.fetchone()

    assert result[dbf.VIDEO_COLUMN_IDX__playlist_id] == plpk3
    assert result[dbf.VIDEO_COLUMN_IDX__pk] == vpk



def test_set_video_as_downloaded():
    videdict = {
        'id': 'id_test',
        'title': 'title_test',
    }
    video1 = dbf.insert_video(vdata=videdict)

    sql = """
        SELECT is_down
        FROM video
        WHERE video.id = %(id)s
        ;
    """
    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars=videdict)
        row = cur.fetchone()

    is_downloaded = row[0]

    assert is_downloaded is False

    result3 = dbf.set_video_as_downloaded(vid=videdict['id'])
    vpk = [video for video in result3][0]

    assert isinstance(vpk, dict)

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars=videdict)
        row = cur.fetchone()

    is_downloaded = row[0]

    assert is_downloaded is True



@pytest.mark.parametrize('sql', [
    """
    INSERT INTO public.video (id,  title, playlist_pk, added, is_down)
    VALUES ('a', 'vid01', NULL, '2020-08-18 14:53:22.697986', false);
    """,
    """
    INSERT INTO public.video (id,  title, playlist_pk, added, is_down) VALUES
    ('a', 'vid01', NULL, '2020-08-18 14:53:22.697986', false),
    ('b', 'vid02', NULL, '2020-08-18 14:53:24.035011', false),
    ('c', 'vid03', NULL, '2020-08-18 14:58:58.980937', false);
    """,
])
def test_select_all_videos_returns_all_video_rows_once(sql):
    with dbf.PGConnection() as conn:
        curs = conn.cursor()
        curs.execute(sql)
        conn.commit()

        curs.execute("""
            SELECT count (pk)
            FROM video;
        """)
        rows = curs.fetchone()

    rowcount = rows[0]
    allvids = dbf.select_all_videos()

    assert rowcount == len(allvids)





@pytest.mark.parametrize('vids, count', (
    [('id_aa',), 1],
    [('id_aa', 'id_aa', 'id_aa',), 1],
    [('id_aa', 'id_cc', 'id_dd'), 3],
    [('id_aa', '--id_cc', '--id_dd'), 1],
    [('--id_aa', '--id_cc', '--id_dd'), 0],
))
def test_select_videos_by_id_retursn_videos_by_video_id_list(vids, count):
    sql = """
        INSERT INTO public.video (id,  title, playlist_pk, added, is_down) VALUES
            ('id_aa', 'title_aa', NULL, '2020-01-01 12:12:12.12', false),
            ('id_bb', 'title_bb', NULL, '2020-01-01 12:12:12.12', false),
            ('id_cc', 'title_cc', NULL, '2020-01-01 12:12:12.12', false),
            ('id_dd', 'title_dd', NULL, '2020-01-01 12:12:12.12', false),
            ('id_ff', 'title_ff', NULL, '2020-01-01 12:12:12.12', false)
    """

    with dbf.PGConnection() as conn:
        curs = conn.cursor()
        curs.execute(sql)
        conn.commit()

    videos = dbf.select_videos_by_id(vids=vids)

    assert len(videos) == count




@pytest.mark.parametrize('vids', (
    ('id_aa',),
    ('id_aa', 'id_aa', 'id_aa',),
    ('id_aa', 'id_cc', 'id_dd'),
    ('id_aa', '--id_cc', '--id_dd'),
))
def test_select_videos_by_id_retursn_returns_same_columns_as_all_videos(vids):
    sql = """
        INSERT INTO public.video (id,  title, playlist_pk, added, is_down) VALUES
            ('id_aa', 'title_aa', NULL, '2020-01-01 12:12:12.12', false),
            ('id_bb', 'title_bb', NULL, '2020-01-01 12:12:12.12', false),
            ('id_cc', 'title_cc', NULL, '2020-01-01 12:12:12.12', false),
            ('id_dd', 'title_dd', NULL, '2020-01-01 12:12:12.12', false),
            ('id_ff', 'title_ff', NULL, '2020-01-01 12:12:12.12', false)
    """

    with dbf.PGConnection() as conn:
        curs = conn.cursor()
        curs.execute(sql)
        conn.commit()

    videos = dbf.select_videos_by_id(vids=vids)
    allvideos = dbf.select_all_videos()

    assert len(videos[0]) == len(allvideos[0])





@pytest.mark.parametrize('pldata', tests.setup.PLAYLIST_DATA)
def test_insert_playlist_returns_dict(pldata):
    result = dbf.insert_playlist(pldict=pldata)

    assert isinstance(result, list)
    assert isinstance(result[0]['pk'], int)




@pytest.mark.parametrize('vdata', tests.setup.VIDEO_DATA)
def test_insert_video_returns_dict(vdata):
    result = dbf.insert_video(vdata=vdata)
    video = list(result)[0]

    assert isinstance(result, list)
    assert [result[0]['id']] == [video['id']]
    assert isinstance(video['pk'], int)



def test_set_video_playlist_returns_dict():
    sql = """
        SELECT pk, id, title, playlist_pk
        FROM video
        WHERE video.id = %(vid)s
        ;
    """
    videodata = dict(tests.setup.VIDEO_DATA[0])

    res1 = dbf.insert_playlist(pldict=tests.setup.PLAYLIST_DATA[0])
    plpk1 = res1[0]
    res2 = dbf.insert_playlist(pldict=tests.setup.PLAYLIST_DATA[1])
    plpk2 = res2[0]
    vpk = dbf.insert_video(vdata=videodata)

    result = dbf.set_video_playlist(vid=videodata['id'], plpk=plpk1['pk'])

    assert isinstance(result, list)




@pytest.mark.parametrize('vdata', tests.setup.VIDEO_DATA)
def test_select_all_videos_returns_dict_of_dicts(vdata):
    vpk = dbf.insert_video(vdata=vdata)
    vpk = dbf.insert_video(vdata=tests.setup.VIDEO_DATA[0])
    result = dbf.select_all_videos()

    assert isinstance(result, list)
    assert all(map(lambda x: isinstance(x, dict), result))




def test_video_has_comlumns():
    tests.setup.run_sql_file(sqlfile='testData')
    allvideos = dbf.select_all_videos()
    videoid = allvideos[0][dbf.VIDEO_COLUMN_NAME__id]
    videos = dbf.select_videos_by_id(vids=[videoid])
    video = videos[0]

    assert video == allvideos[0]
    assert list(video.keys()) == VIDEO_COLUMNS
