\pset pager off

-- select * from playlist;
select * from video;


select video.pk, video.title, playlist.title as playlist, video.is_down, video.added, video.id as youtube_id
from video
join playlist on playlist.pk = video.playlist
;