import sys
import youtube_dl

urls = [
    'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
    'HJq-6y2IYEQ',
]

# url = 'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32'
# url = 'PL9YsudagsL6hicXrha4zBId875lRXxc32'


ytdl_opts = {
    # 'age_limit': None,
    # 'allsubtitles': False,
    # 'ap_mso': None,
    # 'ap_password': None,
    # 'ap_username': None,
    # 'autonumber_size': None,
    # 'bidi_workaround': None,
    # 'buffersize': 1024,
    # 'cachedir': None,
    # 'call_home': False,
    # 'cn_verification_proxy': None,
    # 'config_location': None,
    # 'cookiefile': None,
    # 'debug_printtraffic': False,
    # 'default_search': None,
    # 'download_archive': None,
    # 'dump_intermediate_pages': False,
    # 'external_downloader': None,
    # 'external_downloader_args': None,
    # 'ffmpeg_location': None,
    # 'fixup': 'detect_or_warn',
    # 'force_generic_extractor': False,
    # 'forcedescription': False,
    # 'forceduration': False,
    # 'forcefilename': False,
    # 'forceformat': False,
    # 'forcejson': False,
    # 'forcethumbnail': False,
    # 'format': None,
    # 'fragment_retries': 10,
    # 'geo_bypass': True,
    # 'geo_bypass_country': None,
    # 'geo_bypass_ip_block': None,
    # 'geo_verification_proxy': None,
    # 'hls_prefer_native': None,
    # 'hls_use_mpegts': None,
    # 'http_chunk_size': None,
    # 'include_ads': None,
    # 'keep_fragments': False,
    # 'list_thumbnails': False,
    # 'listsubtitles': False,
    # 'logtostderr': False,
    # 'mark_watched': False,
    # 'match_filter': None,
    # 'max_filesize': None,
    # 'max_sleep_interval': None,
    # 'max_views': None,
    # 'merge_output_format': None,
    # 'min_filesize': None,
    # 'min_views': None,
    # 'no_color': False,
    # 'no_warnings': False,
    # 'nocheckcertificate': False,
    # 'nooverwrites': False,
    # 'noresizebuffer': False,
    # 'password': None,
    # 'postprocessor_args': None,
    # 'postprocessors': [],
    # 'prefer_ffmpeg': None,
    # 'prefer_free_formats': False,
    # 'prefer_insecure': None,
    # 'progress_with_newline': False,
    # 'proxy': None,
    # 'ratelimit': None,
    # 'retries': 10,
    # 'skip_unavailable_fragments': True,
    # 'sleep_interval': None,
    # 'socket_timeout': None,
    # 'source_address': None,
    # 'subtitlesformat': 'best',
    # 'subtitleslangs': [],
    # 'twofactor': None,
    # 'usenetrc': False,
    # 'username': None,
    # 'verbose': False,
    # 'videopassword': None,
    # 'write_all_thumbnails': False,
    # 'write_pages': False,
    # 'writeautomaticsub': False,
    # 'writesubtitles': False,
    # 'writethumbnail': False,
    # 'xattr_set_filesize': None,
    # 'youtube_print_sig_code': False,
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
