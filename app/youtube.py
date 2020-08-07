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




class Video(BaseEntity):
    _attrs = [
        'id',
        'title',
        'upload_date',
        'alt_title',
    ]
    # ['id', 'uploader', 'uploader_id', 'uploader_url',
    #  'channel_id', 'channel_url', 'upload_date', 'license',
    #   'creator', 'title', 'alt_title', 'thumbnails',
    #    'description', 'categories', 'tags', 'subtitles',
    #     'automatic_captions', 'duration', 'age_limit',
    #     'annotations', 'chapters', 'webpage_url', 'view_count',
    #      'like_count', 'dislike_count', 'average_rating', 'formats',
    #       'is_live', 'start_time', 'end_time', 'series',
    #        'season_number', 'episode_number', 'track', 'artist',
    #         'album', 'release_date', 'release_year', 'extractor',
    #          'webpage_url_basename', 'extractor_key'])


    def print_info(self):
        print('id:              {}'.format(self.id))
        print('title:           {}'.format(self.title))
        print('upload_date:     {}'.format(self.upload_date))
        print('alt_title:       {}'.format(self.alt_title))
        # print(self.alt_title)
        # print(self.duration)
        # print(self.start_time)
        # print(self.end_time)
        # print(self.track)
        # print(self.artist)
        # print(self.artist)
        # print(self.album)



class Playlist(BaseEntity):
    _attrs = [
        'id',
        'title',
    ]
    # ['_type', 'entries', 'id', 'title', 'uploader',
    #  'uploader_id', 'uploader_url', 'extractor',
    #   'webpage_url', 'webpage_url_basename', 'extractor_key'])

    def print_info(self):
        print('id:      {}'.format(self.id))
        print('title:   {}'.format(self.title))



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

            if '_type' in result.keys():
                self.playlist = Playlist(attrs=result)
            else:
                self.videos.append(Video(attrs=result))





for url in urls:
    print('\n', '-'*79)

    ytdl = Youtube()
    ytdl.url = url
    ytdl.fetch_info()

    if ytdl.playlist:
        ytdl.playlist.print_info()

    else:
        for video in ytdl.videos:
            video.print_info()

    # result.print_info()


    # print('\n>>> START...')

    # if '_type' in result:
    #     print(result['_type'])
    #     print(result['id'])
    #     print(result['title'])
    #     print(result['uploader'])
    #     print(result['uploader_id'])
    #     print(result['uploader_url'])
    #     print(result['extractor'])
    #     print(result['webpage_url'])
    #     print(result['webpage_url_basename'])
    #     print(result['extractor_key'])

    #     entries = result['entries']
    #     attrs = [
    #         'album',
    #         'artist',
    #         # 'description',
    #         'duration',
    #         'ext',
    #         # 'formats',
    #         'id',
    #         'playlist',
    #         'playlist_id',
    #         'playlist_index',
    #         'playlist_title',
    #         'title',
    #         'track',
    #     ]

    #     for song in entries:
    #         print('-'*55)

    #         for key in attrs:
    #             print(song[key])

    # else:
    #     print(result.keys())
