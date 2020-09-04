import pytest
import dbaccess.dbfuncs as dbf
import tests.setup


VIDEO_ROW_FIELDS = [
    dbf.VIDEO_ROW_NAME__pk,
    dbf.VIDEO_ROW_NAME__id,
    dbf.VIDEO_ROW_NAME__title,
    dbf.VIDEO_ROW_NAME__added,
    dbf.VIDEO_ROW_NAME__is_down,
    dbf.VIDEO_ROW_NAME__playlist_pks,
    dbf.VIDEO_ROW_NAME__playlists,
]



def setup():
    tests.setup.init_test_db()



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
    vpk = [video for video in result3.values()][0]

    assert isinstance(vpk, dict)

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars=videdict)
        row = cur.fetchone()

    is_downloaded = row[0]

    assert is_downloaded is True



@pytest.mark.parametrize('sql', [
    """
    INSERT INTO public.video (id,  title, added, is_down)
    VALUES ('a', 'vid01', '2020-08-18 14:53:22.697986', false);
    """,
    """
    INSERT INTO public.video (id,  title, added, is_down) VALUES
    ('a', 'vid01', '2020-08-18 14:53:22.697986', false),
    ('b', 'vid02', '2020-08-18 14:53:24.035011', false),
    ('c', 'vid03', '2020-08-18 14:58:58.980937', false);
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
        INSERT INTO public.video (id,  title, added, is_down) VALUES
            ('id_aa', 'title_aa', '2020-01-01 12:12:12.12', false),
            ('id_bb', 'title_bb', '2020-01-01 12:12:12.12', false),
            ('id_cc', 'title_cc', '2020-01-01 12:12:12.12', false),
            ('id_dd', 'title_dd', '2020-01-01 12:12:12.12', false),
            ('id_ff', 'title_ff', '2020-01-01 12:12:12.12', false)
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
        INSERT INTO public.video (id,  title, added, is_down) VALUES
            ('id_aa', 'title_aa', '2020-01-01 12:12:12.12', false),
            ('id_bb', 'title_bb', '2020-01-01 12:12:12.12', false),
            ('id_cc', 'title_cc', '2020-01-01 12:12:12.12', false),
            ('id_dd', 'title_dd', '2020-01-01 12:12:12.12', false),
            ('id_ff', 'title_ff', '2020-01-01 12:12:12.12', false)
    """

    with dbf.PGConnection() as conn:
        curs = conn.cursor()
        curs.execute(sql)
        conn.commit()

    videos = dbf.select_videos_by_id(vids=vids)
    allvideos = dbf.select_all_videos()

    assert len(videos[0]) == len(allvideos[0])




def test_select_all_videos_empty_db():
    data = dbf.select_all_videos()
    expected = []

    assert data == expected




def test_set_video_as_downloaded():
    tests.setup.run_sql_file(sqlfile='testData')
    initvideo = dbf.select_videos_by_id(vids=['id_5'])

    assert initvideo[0]['is_down'] == False

    result = dbf.set_video_as_downloaded(vid='id_5')

    assert result[0]['is_down'] is True




@pytest.mark.skip(reason='OUTDATED EXPECTED DATA AFTER UPDATE')
def test_set_video_playlist():
    tests.setup.run_sql_file(sqlfile='testData')
    vid = 'id_10'
    video = dbf.select_videos_by_id(vids=(vid,))

    assert video[0]['playlist_pks'] is None
    assert video[0]['playlists'] is None

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




@pytest.mark.skip(reason='OUTDATED EXPECTED DATA AFTER UPDATE')
@pytest.mark.parametrize('plid, expected', (
    ('plid0', []),
    ('plid1', ['id2']),
    ('plid2', ['id4', 'id5']),
))
def test_select_videos_by_playlistid(plid, expected):
    tests.setup.run_sql_file(sqlfile='testData_03')
    result = dbf.select_videos_by_playlistid(playlistid=plid)
    vids = [video['id'] for video in result.values()]

    assert vids == expected


@pytest.mark.skip(reason='OUTDATED EXPECTED DATA AFTER UPDATE')
def test_insert_video():
    video = {
        'id': 'new_vid_id_1',
        'title': 'new_vid_title_1',
    }
    result = dbf.insert_video(vdata=video)

    assert list(result.keys()) == [video['id']]
    assert list(result[video['id']].keys()) == [
        'pk', 'id', 'title',  'added', 'is_down', 'playlistid', 'playlisttitle']
    assert result[video['id']]['id'] == video['id']
    assert result[video['id']]['title'] == video['title']




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
def test_insert_playlist_05(pldict):
    result = dbf.insert_playlist(pldict=pldict)

    assert len(result.keys()) == 1
    assert list(result.keys()) == [pldict['id']]
    assert list(result[pldict['id']].keys()) == [
        'pk', 'id', 'title', 'uploader_id', 'added']
    assert result[pldict['id']]['id'] == pldict['id']
    assert result[pldict['id']]['title'] == pldict['title']
    assert result[pldict['id']]['uploader_id'] == pldict['uploader_id']




def test_video_row_returns_fields():
    tests.setup.run_sql_file(sqlfile='testData')
    allvideos = dbf.select_all_videos()

    for row in allvideos:
        assert list(row.keys()) == VIDEO_ROW_FIELDS
