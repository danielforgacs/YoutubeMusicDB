import sys
import youtube_dl

urls = [
    'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
    'HJq-6y2IYEQ',
]


ytdl_opts = {
    'autonumber': None,
    'autonumber_start': 1,
    'consoletitle': False,
    'continuedl': True,
    'dump_single_json': False,
    'encoding': None,
    'extract_flat': False,
    'forceid': False,
    'forcetitle': False,
    'forceurl': False,
    'ignoreerrors': False,
    'keepvideo': False,
    'listformats': None,
    'matchtitle': None,
    'max_downloads': None,
    'nopart': False,
    'noplaylist': False,
    'noprogress': False,
    'outtmpl': '%(title)s-%(id)s.%(ext)s',
    'playlist_items': None,
    'playlistend': None,
    'playlistrandom': None,
    'playlistreverse': None,
    'playliststart': 1,
    'quiet': True,
    'rejecttitle': None,
    'restrictfilenames': False,
    'simulate': True,
    'skip_download': False,
    'test': False,
    'updatetime': True,
    'usetitle': None,
    'writeannotations': False,
    'writedescription': False,
    'writeinfojson': False,
    'youtube_include_dash_manifest': True,
}


class Youtube(youtube_dl.YoutubeDL):
    def __init__(self, url=None):
        super().__init__(params=ytdl_opts, auto_init=True)
        self.url = url

    def fetch_info(self):
        result = None

        if self.url:
            result = self.extract_info(url=self.url)

        return result


for url in urls:
    print('\n', '>'*79)

    ytdl = Youtube()
    ytdl.url = url
    result = ytdl.fetch_info()

    print('\n>>> START...')

    if '_type' in result:
        print(result['_type'])
        print(result['id'])
        print(result['title'])
        print(result['uploader'])
        print(result['uploader_id'])
        print(result['uploader_url'])
        print(result['extractor'])
        print(result['webpage_url'])
        print(result['webpage_url_basename'])
        print(result['extractor_key'])

        entries = result['entries']
        attrs = [
            'album',
            'artist',
            # 'description',
            'duration',
            'ext',
            # 'formats',
            'id',
            'playlist',
            'playlist_id',
            'playlist_index',
            'playlist_title',
            'title',
            'track',
        ]

        for song in entries:
            print('-'*55)

            for key in attrs:
                print(song[key])

    else:
        print(result.keys())
