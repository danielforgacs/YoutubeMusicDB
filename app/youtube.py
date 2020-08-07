import sys
import youtube_dl

urls = [
    'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
    'HJq-6y2IYEQ',
]



class BaseEntity:
    def __init__(self, attrs):
        for attr in attrs:
            if attr in self._attrs:
                setattr(self, attr, attrs[attr])



    def print_info(self):
        for attr in self._attrs:
            print('{:<50}{}'.format(attr, getattr(self, attr)))




class Video(BaseEntity):
    _attrs = [
        'id',
        'uploader',
        'uploader_id',
        'uploader_url',
        'channel_id',
        'channel_url',
        'upload_date',
        'license',
        'creator',
        'title',
        'alt_title',
        'thumbnails',
        'description',
        'categories',
        'tags',
        'subtitles',
        'automatic_captions',
        'duration',
        'age_limit',
        'annotations',
        'chapters',
        'webpage_url',
        'view_count',
        'like_count',
        'dislike_count',
        'average_rating',
        'formats',
        'is_live',
        'start_time',
        'end_time',
        'series',
        'season_number',
        'episode_number',
        'track',
        'artist',
        'album',
        'release_date',
        'release_year',
        'extractor',
        'webpage_url_basename',
        'extractor_key'
    ]


    # def print_info(self):
    #     print('id:              {}'.format(self.id))
    #     print('title:           {}'.format(self.title))
    #     print('upload_date:     {}'.format(self.upload_date))
    #     print('alt_title:       {}'.format(self.alt_title))



class Playlist(BaseEntity):
    _attrs = [
        '_type',
        'entries',
        'id',
        'title',
        'uploader',
        'uploader_id',
        'uploader_url',
        'extractor',
        'webpage_url',
        'webpage_url_basename',
        'extractor_key'
    ]

    def __init__(self, attrs):
        super().__init__(attrs=attrs)
        self.videos = []

    # def print_info(self):
    #     print('id:      {}'.format(self.id))
    #     print('title:   {}'.format(self.title))





class Youtube(youtube_dl.YoutubeDL):
    def __init__(self, url=None, params=None, do_download=False):
        self.url = url
        self.do_download = do_download
        self.playlist = None
        self.videos = []

        if params:
            params.update({'quiet': True})
        else:
            params = {}

        super().__init__(params=params, auto_init=True)



    def fetch_info(self):
        if self.url:
            result = self.extract_info(
                url=self.url,
                download=self.do_download,
                process=self.do_download,
            )

            print('RESULT:', result.keys())

            if '_type' in result.keys():
                self.playlist = Playlist(attrs=result)
                self.playlist.youtube = self
            else:
                self.videos.append(Video(attrs=result))





for url in urls:
    print('\n', '-'*79)

    ytdl = Youtube()
    ytdl.url = url
    ytdl.fetch_info()

    if ytdl.playlist:
        ytdl.playlist.print_info()

        for video in ytdl.playlist.videos:
            video.print_info()

    else:
        for video in ytdl.videos:
            video.print_info()

