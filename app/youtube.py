import os
import sys
import youtube_dl
# import app.data as datab
import app.config
import xmlrpc.client


DB_ACCESS_HOST = os.environ['DBACCESS_RPC_HOST']
DB_ACCESS_PORT = int(os.environ['DBACCESS_RPC_PORT'])
DB_ACCESS_URL = 'http://{host}:{port}'.format(host=DB_ACCESS_HOST, port=DB_ACCESS_PORT)
RPC_CLIENT_KWARGS = {
    'uri': DB_ACCESS_URL,
    'allow_none': True,
}


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
        # self.pk = datab.insert_video(vdata=self.as_dict)

        with xmlrpc.client.ServerProxy(**RPC_CLIENT_KWARGS) as dbacces_svr:
            response = dbacces_svr.insert_video(self.as_dict)

        self.pk = response[0]['pk']


    def set_playlist(self, playlist):
        # datab.set_video_playlist(self.id, plpk=playlist.pk)
        # dbacces_svr = xmlrpc.client.ServerProxy(uri=DB_ACCESS_URL)
        with xmlrpc.client.ServerProxy(**RPC_CLIENT_KWARGS) as dbacces_svr:
            dbacces_svr.set_video_playlist(self.id, playlist.pk)





class Playlist(BaseEntity):
    _attrs = YOUTUBEDL_PLAYLIST_ATTRS

    def __init__(self, attrs):
        super().__init__(attrs=attrs)
        self._videos = []
        # result = datab.insert_playlist(pldict=self.as_dict)
        # self.pk = result['pk']
        with xmlrpc.client.ServerProxy(**RPC_CLIENT_KWARGS) as dbacces_svr:
            response = dbacces_svr.insert_playlist(self.as_dict)

        plid = response[0]
        self.pk = response[0]['pk']

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
            if not yout.video:
                print('--> [ERROR] can`t youtube video: {}'.format(item['url']))
                continue

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
        self.error = None

        if params:
            params.update({'quiet': True})
        else:
            params = {'quiet': True}

        if app.config.YOUTUBE_DL_FORMAT:
            params['format'] = app.config.YOUTUBE_DL_FORMAT

        if app.config.YOUTUBE_DL_OUTPUT_TEMPLATE:
            params['outtmpl'] = app.config.YOUTUBE_DL_OUTPUT_TEMPLATE

        super().__init__(params=params, auto_init=True)

        self.fetch_info()



    def fetch_info(self):
        if self.url:
            try:
                result = self.extract_info(
                    url=self.url,
                    download=self.do_download,
                    process=self.do_download,
                )
            except youtube_dl.utils.DownloadError as err:
                self.error = ''.join(err.args)

                return

            result['youtube'] = self

            if '_type' in result.keys():
                self.playlist = Playlist(attrs=result)
            else:
                result['playlist'] = None
                self.video = Video(attrs=result)



if __name__ == '__main__':
    pass
