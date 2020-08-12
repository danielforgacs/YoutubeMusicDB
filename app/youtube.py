import sys
import youtube_dl
import app.data as datab



YOUTUBEDL_VIDEO_ATTRS = [
    'id',
    'uploader',
    'uploader_id',
    'upload_date',
    'title',
    'alt_title',
    'duration',
]
YOUTUBEDL_PLAYLIST_ATTRS = [
    'entries',
    'id',
    'title',
    'uploader_id',
]




class BaseEntity:
    def __init__(self, attrs):
        for attr in attrs:
            if attr in self._attrs:
                setattr(self, attr, attrs[attr])

        self.youtube = attrs['youtube']



    def print_info(self):
        for attr in ['pk']+self._attrs:
            print('{:<50}{}'.format(attr, getattr(self, attr)))



    @property
    def as_dict(self):
        result = {}

        for attr, value in self.__dict__.items():
            if attr in self._attrs:
                result[attr] = value

        return result




class Video(BaseEntity):
    _attrs = YOUTUBEDL_VIDEO_ATTRS

    def __init__(self, attrs):
        super().__init__(attrs=attrs)
        self.pk = datab.insert_video(vdata=self.as_dict)


    def print_info(self):
        super().print_info()
        print('{:<50}{}'.format('playlist', self.playlist))


    def set_playlist(self, playlist):
        vpk, vid, plpk = datab.set_video_playlist(self.id, plpk=playlist.pk)




class Playlist(BaseEntity):
    _attrs = YOUTUBEDL_PLAYLIST_ATTRS

    def __init__(self, attrs):
        super().__init__(attrs=attrs)
        self._videos = []
        self.pk = datab.insert_playlist(pldict=self.as_dict)

        for video in self.videos:
            video.set_playlist(playlist=self)



    @property
    def videos(self):
        for item in self.entries:
            yout = Youtube(
                url=item['url'],
                params=self.youtube.params,
                do_download=self.youtube.do_download,
            )
            yout.video.playlist = self
            self._videos.append(yout.video)

        return self._videos


    @property
    def as_dict(self):
        data = super().as_dict
        data['videos'] = [video.as_dict for video in self.videos]
        del data['entries']

        return data






class Youtube(youtube_dl.YoutubeDL):
    def __init__(self, url, params=None, do_download=False):
        self.params = params
        self.url = url
        self.do_download = do_download
        self.playlist = None
        self.video = None

        if params:
            params.update({'quiet': True})
        else:
            params = {'quiet': True}

        super().__init__(params=params, auto_init=True)

        self.fetch_info()



    def fetch_info(self):
        if self.url:
            result = self.extract_info(
                url=self.url,
                download=self.do_download,
                process=self.do_download,
            )
            result['youtube'] = self

            if '_type' in result.keys():
                self.playlist = Playlist(attrs=result)
            else:
                result['playlist'] = None
                self.video = Video(attrs=result)



if __name__ == '__main__':
    pass
