import os
import pytest
import app.main as main
import app.youtube as ytdl
import tests.setup
import dbaccess.dbfuncs as dbf
from app import config


def setup():
    tests.setup.init_test_db()



def test_post_playlist_returns_error_json_on_missing_id():
    expected = {'error': 'missing id'}

    with main.app.test_client() as client:
        response = client.post('/api/createplaylist', json={'NOid': tests.setup.YOUTUBE_PLAYLISTS[0]})

    data = response.get_json()

    assert data == expected



@pytest.mark.parametrize('plst', tests.setup.YOUTUBE_PLAYLISTS)
def test_files_are_deleted_after_download(plst):
    with main.app.test_client() as client:
        response = client.post('/api/createplaylist', json={'id': plst})

    with main.app.test_client() as client:
        response = client.post('/api/download', json={'id': plst})

    ls = os.listdir(main.DOWNLOAD_DIR)

    for item in ls:
        assert item.startswith(config.DOWNLOAD_ZIP_PREFIX)





@pytest.mark.parametrize('plst', tests.setup.YOUTUBE_PLAYLISTS)
def test_download_set_videos_as_is_down_True(plst):
    with main.app.test_client() as client:
        response = client.post('/api/createplaylist', json={'id': plst})

    with main.app.test_client() as client:
        response = client.post('/api/download', json={'id': plst})

    videoids = response.json
    # videoids = tuple(vid['id'] for vid in response.json['videos'])
    videoids = tuple(videoids.keys())

    sql = """
        SELECT is_down
        FROM video
        WHERE id in %s;
    """

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars=(videoids,))
        rows = cur.fetchall()

    is_down_vals = [row[0] for row in rows]

    assert all(is_down_vals)




@pytest.mark.parametrize('plst', tests.setup.YOUTUBE_PLAYLISTS)
def test_download_returns_the_archive_name(plst):
    with main.app.test_client() as client:
        response = client.post('/api/createplaylist', json={'id': plst})

    with main.app.test_client() as client:
        response = client.post('/api/download', json={'id': plst})

    archivefile = os.path.join(main.DOWNLOAD_DIR, response.json['archive'])

    assert os.path.isfile(archivefile)




def test_archive_name_can_be_downloaded():
    pass



def test_archive_deletes_archive_after_some_time():
    pass




def test_downloaded_videos_are_converted_to_mp3():
    pass



def test_downloaded_videos_have_specific_file_name():
    pass




if __name__ == '__main__':
    pass
