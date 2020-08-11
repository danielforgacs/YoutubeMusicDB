import pytest
import app.youtube



YOUTUBE_IDS = [
    'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
    'HJq-6y2IYEQ',
    'FIQ2F3T1ydM',
]





def test_can_init_youtube():
    youtube = app.youtube.Youtube()
    assert isinstance(youtube, app.youtube.Youtube)




def test_playlist_has_dbid():
    youtube = app.youtube.Youtube()
    youtube.url = 'PL9YsudagsL6hicXrha4zBId875lRXxc32'
    youtube.fetch_info()

    # print(youtube.playlist)
    # assert hasattr(youtube.playlist, 'dbid')

