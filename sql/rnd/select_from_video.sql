select * from video order by pk;
select * from playlist_video order by video_pk;

select array [playlist.id, playlist.title]
from playlist
;

select array_agg ( array [playlist.id, playlist.title])
from playlist
;

SELECT
	video.pk,
	video.id AS youtube_id,
	video.title,
	playlist.id AS playlistid,
	video.added,
	video.is_down,
	playlist.title AS playlist
FROM video
LEFT JOIN playlist ON playlist.pk = video.playlist_pk
ORDER BY video.pk
;

SELECT
	video.pk,
	video.id AS youtube_id,
	video.title,
	playlist.id AS playlistid,
	video.added,
	video.is_down,
	playlist.title AS playlist,
	(
		SELECT array_agg ( array [ playlist.pk::text, playlist.id, playlist.title ])
		FROM playlist
		JOIN playlist_video ON playlist_video.playlist_pk = playlist.pk
		WHERE video.pk = playlist_video.video_pk
	) AS playlist_data
FROM video
LEFT JOIN playlist ON playlist.pk = video.playlist_pk
ORDER BY video.pk
;
