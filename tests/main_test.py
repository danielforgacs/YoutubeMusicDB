import pytest
import app.main as main
import app.youtube as ytdl



youtubeids = [
    'PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
    # 'https://www.youtube.com/playlist?list=PL9YsudagsL6glHSHNASig_nyaU5zyrBJD',
    'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
    'HJq-6y2IYEQ',
    'FIQ2F3T1ydM',
]




@pytest.fixture
def client():
    with main.app.test_client() as test_client:
        yield test_client




@pytest.mark.parametrize('ytid', youtubeids)
def test_post_playlist(client, ytid):
    youtube = ytdl.Youtube()
    youtube.url = ytid
    youtube.fetch_info()

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
