import pytest
import app.main as main



@pytest.fixture
def client():
    with main.app.test_client() as test_client:
        yield test_client




def test_post_playlist(client):
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
    response = client.post('/', json={'id': 'PL9YsudagsL6hicXrha4zBId875lRXxc32'})
    data = response.get_json()

    assert data == expected




if __name__ == '__main__':
    pass
