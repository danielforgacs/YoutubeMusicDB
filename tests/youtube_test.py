import pytest
import app.youtube
import tests.setup



def setup():
    tests.setup.init_test_db()



@pytest.mark.parametrize('ytid', tests.setup.YOUTUBE_IDS)
def test_can_init_youtube(ytid):
    youtube = app.youtube.Youtube(url=ytid)

    assert isinstance(youtube, app.youtube.Youtube)




def test_playlist_has_pk():
    youtube = app.youtube.Youtube(url=tests.setup.YOUTUBE_PLAYLISTS[0])

    assert hasattr(youtube.playlist, 'pk')



def test_youtube_playlist_has_videos():
    youtube = app.youtube.Youtube(url=tests.setup.YOUTUBE_PLAYLISTS[0])
    is_video = lambda x: isinstance(x, app.youtube.Video)

    assert len(youtube.playlist.videos) > 0
    assert all(filter(is_video, youtube.playlist.videos))
