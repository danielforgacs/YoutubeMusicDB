import sys
import youtube_dl
import app.data as datab




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
    _attrs = [
        'id',
        'uploader',
        'uploader_id',
        # 'uploader_url',
        # 'channel_id',
        # 'channel_url',
        'upload_date',
        # 'license',
        # 'creator',
        'title',
        'alt_title',
        # 'thumbnails',
        # 'description',
        # 'categories',
        # 'tags',
        # 'subtitles',
        # 'automatic_captions',
        'duration',
        # 'age_limit',
        # 'annotations',
        # 'chapters',
        # 'webpage_url',
        # 'view_count',
        # 'like_count',
        # 'dislike_count',
        # 'average_rating',
        # 'formats',
        # 'is_live',
        # 'start_time',
        # 'end_time',
        # 'series',
        # 'season_number',
        # 'episode_number',
        # 'track',
        # 'artist',
        # 'album',
        # 'release_date',
        # 'release_year',
        # 'extractor',
        # 'webpage_url_basename',
        # 'extractor_key'
    ]

    def __init__(self, attrs):
        self.playlist = None
        super().__init__(attrs=attrs)
        self.pk = datab.insert_video(vdata=self.as_dict)


    def print_info(self):
        super().print_info()
        print('{:<50}{}'.format('playlist', self.playlist))




class Playlist(BaseEntity):
    _attrs = [
        # '_type',
        'entries',
        'id',
        'title',
        # 'uploader',
        'uploader_id',
        # 'uploader_url',
        # 'extractor',
        # 'webpage_url',
        # 'webpage_url_basename',
        # 'extractor_key'
    ]

    def __init__(self, attrs):
        super().__init__(attrs=attrs)
        self._videos = []
        self.pk = datab.insert_playlist(pldict=self.as_dict)
        # self.dbid = None



    @property
    def videos(self):
        for item in self.entries:
            yout = Youtube(
                url=item['url'],
                params=self.youtube.params,
                do_download=self.youtube.do_download
            )
            # ytdl.fetch_info()
            # video = ytdl.video
            # video.pldbid = self.dbid
            yout.video.playlist = self
            self._videos.append(yout.video)

        return self._videos


    @property
    def as_dict(self):
        data = super().as_dict
        # data['videos'] = [video.as_dict for video in self.videos]
        data['videos'] = [{}]
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
                # self.playlist.youtube = self
                # playlist.pk = datab.insert_playlist(playlist=self.playlist)
                # self.playlist.videos


            else:
                self.video = Video(attrs=result)
                # self.video.youtube = self
                # datab.insert_video(video=self.video)




if __name__ == '__main__':
    pass

    urls = [
        'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
        # 'PL9YsudagsL6hicXrha4zBId875lRXxc32',
        # 'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
        # 'HJq-6y2IYEQ',
        'FIQ2F3T1ydM',
    ]

    for url in urls:
        print('\n', '-'*79)

        yout = Youtube(url=url)
        print(yout.playlist)

        if yout.playlist:
            yout.playlist.print_info()

            for vid in yout.playlist.videos:
                print('\t', vid)
                vid.print_info()

        else:
            yout.video.print_info()
        # yout.fetch_info()
        # yout.video.print_info()
        # ytdl.url = url
        # ytdl.fetch_info()

        # if ytdl.playlist:
        #     ytdl.playlist.print_info()

        #     print('\nas_dict:')
        #     print(ytdl.playlist.as_dict)

        #     for video in ytdl.playlist.videos:
        #         print('\n..playlist video:')
        #         video.print_info()
        #         print(video.as_dict)

        # else:
        #     ytdl.video.print_info()
        #     print(ytdl.video.as_dict)
