import os
import pytest
import app.data
import app.main as main
import app.youtube as ytdl
import tests.data_test
import tests.setup
from app import config



youtubeids = [
    'PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
    'HJq-6y2IYEQ',
    'FIQ2F3T1ydM',
    'PL9YsudagsL6h0n4ew9ibbicfGFIPdUKMU',
]


def setup_module():
    tests.data_test.setup_module()


def teardown_module():
    tests.data_test.teardown_module()



@pytest.fixture
def client():
    with main.app.test_client() as test_client:
        yield test_client




@pytest.mark.parametrize('ytid', youtubeids)
def test_post_playlist(client, ytid):
    youtube = ytdl.Youtube(url=ytid)

    if youtube.playlist:
        expected = youtube.playlist.as_dict
    else:
        expected = youtube.video.as_dict

    response = client.post('/', json={'id': ytid})
    data = response.get_json()

    assert data == expected



def test_post_playlist_returns_error_json_on_missing_id(client):
    expected = {'error': 'missing id'}
    response = client.post('/', json={'NOid': youtubeids[0]})
    data = response.get_json()

    assert data == expected





@pytest.mark.parametrize('plst', tests.setup.YOUTUBE_PLAYLISTS)
def test_files_are_deleted_after_download(client, plst):
    response = client.post('/', json={'id': plst})
    response = client.post('/download', json=response.json)

    ls = os.listdir(main.DOWNLOAD_DIR)

    for item in ls:
        assert item.startswith(config.DOWNLOAD_ZIP_PREFIX)





# @pytest.mark.parametrize('plst', tests.setup.YOUTUBE_PLAYLISTS)
@pytest.mark.parametrize('plst', [tests.setup.YOUTUBE_PLAYLISTS[0]])
def test_download_set_videos_as_is_down_True(client, plst):
    response = client.post('/', json={'id': plst})
    response = client.post('/download', json=response.json)

    sql = """
        SELECT is_down
        FROM video
        WHERE id in %s
        ;
    """

    videoids = response.json
    # videoids = response.json['videos']
    videoids = tuple(response.json['videos'])
    print(response.json)
    print(videoids)

    with app.data.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars=(videoids,))
        rows = cur.fetchall()

    is_down_vals = [row[0] for row in rows]
    
    assert all(is_down_vals)




def test_download_returns_the_archive_name():
    pass




def test_archive_name_can_be_downloaded():
    pass



def test_archive_deletes_archive_after_some_time():
    pass


    



if __name__ == '__main__':
    pass
