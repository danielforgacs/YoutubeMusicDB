select * from video order by pk;
select * from playlist_video order by video_pk;

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
    ) as playlist_pks
from video
left join playlist_video on playlist_video.video_pk = video.pk
group by pk
order by pk
;