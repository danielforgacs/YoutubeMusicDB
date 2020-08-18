import pytest
import app.youtube
import tests.data_test
import tests.setup


YOUTUBE_PLAYLISTS = [
    'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'PL9YsudagsL6h0n4ew9ibbicfGFIPdUKMU',
]
YOUTUBE_VIDEOS = [
    'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
    'HJq-6y2IYEQ',
    'FIQ2F3T1ydM',
]

YOUTUBE_IDS = YOUTUBE_PLAYLISTS + YOUTUBE_VIDEOS



def setup_module():
    tests.data_test.setup_module()


def teardown_module():
    tests.data_test.teardown_module()




@pytest.mark.parametrize('ytid', YOUTUBE_IDS)
def test_can_init_youtube(ytid):
    youtube = app.youtube.Youtube(url=ytid)

    assert isinstance(youtube, app.youtube.Youtube)




def test_playlist_has_pk():
    youtube = app.youtube.Youtube(url=YOUTUBE_PLAYLISTS[0])

    assert hasattr(youtube.playlist, 'pk')



def test_youtube_playlist_has_videos():
    youtube = app.youtube.Youtube(url=YOUTUBE_PLAYLISTS[0])
    is_video = lambda x: isinstance(x, app.youtube.Video)

    assert len(youtube.playlist.videos) > 0
    assert all(filter(is_video, youtube.playlist.videos))
