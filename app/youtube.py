import youtube_dl

playlists = [
    'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
]

plparams = {
    # 'simulate': True,
    'skip_download': True,
    # 'extract_flat': True,
    'get-title': True,
    'get-id': True,
    'get-title': True,
    'gettitle': True,
}
dlparams={

}


pl = youtube_dl.YoutubeDL(params=plparams)
extrainfo = {
    'gettitle': True,
    'title': True,
    'get-title': True,
}
pl.extract_info(
    url=playlists[0],
    download=False,
    ie_key=None,
    extra_info=extrainfo,
    process=True,
    force_generic_extractor=False)




# # pl.download(url_list=['https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32'])
# downloader = youtube_dl.downloader.FileDownloader(ydl=pl, params=dlparams)

# # print(dir(youtube_dl))
# # print(dir(youtube_dl.extractor))
# # print(dir(youtube_dl.extractor.youtube))

# extractor = youtube_dl.extractor.youtube.YoutubePlaylistIE(downloader=downloader)
# extractor.extract(url=playlists[0])
# # extractor.extract(url=playlists[0])
# # info = extractor.extract_videos_from_page(page=playlists[0])

# # for k in info:
# #     print(k)

