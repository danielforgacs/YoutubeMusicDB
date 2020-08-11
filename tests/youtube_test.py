import pytest
import app.youtube
import tests.data_test



YOUTUBE_IDS = [
    'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
    'HJq-6y2IYEQ',
    'FIQ2F3T1ydM',
]

def setup_module():
    tests.data_test.setup_module()


def teardown_module():
    tests.data_test.teardown_module()




def test_can_init_youtube():
    youtube = app.youtube.Youtube(url=YOUTUBE_IDS[0])
    assert isinstance(youtube, app.youtube.Youtube)




def test_playlist_has_dbpk():
    youtube = app.youtube.Youtube(url='PL9YsudagsL6hicXrha4zBId875lRXxc32')

    assert hasattr(youtube.playlist, 'pk')

    # print(youtube.playlist)
    # assert hasattr(youtube.playlist, 'dbid')

