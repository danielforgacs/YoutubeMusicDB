import sys
import youtube_dl

url = 'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32'

sys.argv = ['']
sys.argv += [url]
sys.argv += ['--get-title']


# res = youtube_dl._real_main()

# print(res)

ytdl_opts = {
    # 'usenetrc': False,
    # 'username': None,
    # 'password': None,
    # 'twofactor': None,
    # 'videopassword': None,
    # 'ap_mso': None,
    # 'ap_username': None,
    # 'ap_password': None,
    'quiet': True,
    # 'no_warnings': False,
    'forceurl': False,
    'forcetitle': False,
    'forceid': False,
    # 'forcethumbnail': False,
    # 'forcedescription': False,
    # 'forceduration': False,
    # 'forcefilename': False,
    # 'forceformat': False,
    # 'forcejson': False,
    'dump_single_json': False,
    'simulate': True,
    'skip_download': False,
    # 'format': None,
    'listformats': None,
    'outtmpl': '%(title)s-%(id)s.%(ext)s',
    # 'autonumber_size': None,
    'autonumber_start': 1,
    'restrictfilenames': False,
    'ignoreerrors': False,
    # 'force_generic_extractor': False,
    # 'ratelimit': None,
    # 'nooverwrites': False,
    # 'retries': 10,
    # 'fragment_retries': 10,
    # 'skip_unavailable_fragments': True,
    # 'keep_fragments': False,
    # 'buffersize': 1024,
    # 'noresizebuffer': False,
    # 'http_chunk_size': None,
    'continuedl': True,
    'noprogress': False,
    # 'progress_with_newline': False,
    'playliststart': 1,
    'playlistend': None,
    'playlistreverse': None,
    'playlistrandom': None,
    'noplaylist': False,
    # 'logtostderr': False,
    'consoletitle': False,
    'nopart': False,
    'updatetime': True,
    'writedescription': False,
    'writeannotations': False,
    'writeinfojson': False,
    # 'writethumbnail': False,
    # 'write_all_thumbnails': False,
    # 'writesubtitles': False,
    # 'writeautomaticsub': False,
    # 'allsubtitles': False,
    # 'listsubtitles': False,
    # 'subtitlesformat': 'best',
    # 'subtitleslangs': [],
    'matchtitle': None,
    'rejecttitle': None,
    'max_downloads': None,
    # 'prefer_free_formats': False,
    # 'verbose': False,
    # 'dump_intermediate_pages': False,
    # 'write_pages': False,
    'test': False,
    'keepvideo': False,
    # 'min_filesize': None,
    # 'max_filesize': None,
    # 'min_views': None,
    # 'max_views': None,
    # 'cachedir': None,
    # 'youtube_print_sig_code': False,
    # 'age_limit': None,
    # 'download_archive': None,
    # 'cookiefile': None,
    # 'nocheckcertificate': False,
    # 'prefer_insecure': None,
    # 'proxy': None,
    # 'socket_timeout': None,
    # 'bidi_workaround': None,
    # 'debug_printtraffic': False,
    # 'prefer_ffmpeg': None,
    # 'include_ads': None,
    # 'default_search': None,
    'youtube_include_dash_manifest': True,
    'encoding': None,
    'extract_flat': False,
    # 'mark_watched': False,
    # 'merge_output_format': None,
    # 'postprocessors': [],
    # 'fixup': 'detect_or_warn',
    # 'source_address': None,
    # 'call_home': False,
    # 'sleep_interval': None,
    # 'max_sleep_interval': None,
    # 'external_downloader': None,
    # 'list_thumbnails': False,
    'playlist_items': None,
    # 'xattr_set_filesize': None,
    # 'match_filter': None,
    # 'no_color': False,
    # 'ffmpeg_location': None,
    # 'hls_prefer_native': None,
    # 'hls_use_mpegts': None,
    # 'external_downloader_args': None,
    # 'postprocessor_args': None,
    # 'cn_verification_proxy': None,
    # 'geo_verification_proxy': None,
    # 'config_location': None,
    # 'geo_bypass': True,
    # 'geo_bypass_country': None,
    # 'geo_bypass_ip_block': None,
    'autonumber': None,
    'usetitle': None,
}

ytdl = youtube_dl.YoutubeDL(params=ytdl_opts)
result = ytdl.extract_info(url=url)

print('\n>>> START...')

# print(result.keys())
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


# playlists = [
#     'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
# ]

# plparams = {
#     # 'simulate': True,
#     'skip_download': True,
#     # 'extract_flat': True,
#     'get-title': True,
#     'get-id': True,
#     'get-title': True,
#     'gettitle': True,
# }
# dlparams={

# }


# pl = youtube_dl.YoutubeDL(params=plparams)
# extrainfo = {
#     'gettitle': True,
#     'title': True,
#     'get-title': True,
# }
# pl.extract_info(
#     url=playlists[0],
#     download=False,
#     ie_key=None,
#     extra_info=extrainfo,
#     process=True,
#     force_generic_extractor=False)




# # # pl.download(url_list=['https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32'])
# # downloader = youtube_dl.downloader.FileDownloader(ydl=pl, params=dlparams)

# # # print(dir(youtube_dl))
# # # print(dir(youtube_dl.extractor))
# # # print(dir(youtube_dl.extractor.youtube))

# # extractor = youtube_dl.extractor.youtube.YoutubePlaylistIE(downloader=downloader)
# # extractor.extract(url=playlists[0])
# # # extractor.extract(url=playlists[0])
# # # info = extractor.extract_videos_from_page(page=playlists[0])

# # # for k in info:
# # #     print(k)

