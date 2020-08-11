import pytest
import app.main as main
import app.youtube as ytdl
import tests.data_test



youtubeids = [
    # 'PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
    # 'HJq-6y2IYEQ',
    'FIQ2F3T1ydM',
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
    # youtube.url = ytid
    # youtube.fetch_info()

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





if __name__ == '__main__':
    pass
