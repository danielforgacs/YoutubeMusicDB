import pytest
import app.main as main
import app.youtube as ytdl



youtubeids = [
    'PL9YsudagsL6hicXrha4zBId875lRXxc32',
]



@pytest.fixture
def client():
    with main.app.test_client() as test_client:
        yield test_client




@pytest.mark.parametrize('ytid', youtubeids)
def test_post_playlist(client, ytid):
    expected = {
        'id': 'PL9YsudagsL6hicXrha4zBId875lRXxc32',
        'title': 'AAAA',
        'uploader_id': 'forgacsdaniel',
        'videos': [
        {
            'alt_title': None,
            'duration': 281,
            'id': 'HJq-6y2IYEQ',
            'title': 'Drop D Funk - Dr Funk Original - Blast Inspired - Street Sessions Newquay',
            'upload_date': '20191105',
            'uploader': 'Dr Funk',
            'uploader_id': 'UCW8tq_mhu8pVDH2UIGRwuSg'
        },
        {
            'alt_title': None,
            'duration': 153,
            'id': 'FIQ2F3T1ydM',
            'title': 'los pollos hermanos commercial HD',
            'upload_date': '20111008',
            'uploader': 'ibsuser1',
            'uploader_id': 'ibsuser1'
        }
        ]
    }
    response = client.post('/', json={'id': ytid})
    data = response.get_json()

    assert data == expected



@pytest.mark.parametrize('ytid', youtubeids)
def test_post_playlist_02(client, ytid):
    youtube = ytdl.Youtube()
    youtube.url = ytid
    youtube.fetch_info()

    response = client.post('/', json={'id': ytid})
    data = response.get_json()

    assert youtube.playlist.as_dict == data




if __name__ == '__main__':
    pass
