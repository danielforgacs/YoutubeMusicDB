select * from video order by pk;
select * from playlist_video order by video_pk;

select array [playlist.id, playlist.title]
from playlist
;

select array_agg( array [playlist.id, playlist.title])
from playlist
;

select
    video.pk,
    video.id,
    video.title,
    video.playlist_pk,
    video.added,
    video.is_down,
    array (
        select playlist_video.playlist_pk
        from playlist_video
        where playlist_video.video_pk = video.pk
    ) as playlist_pks,
    (
        select array_agg ( array [ playlist.id, playlist.title ])
        from playlist
        join playlist_video on playlist_video.playlist_pk = playlist.pk
        where video.pk = playlist_video.video_pk
    ) as playlist_data
from video
order by video.pk
;
