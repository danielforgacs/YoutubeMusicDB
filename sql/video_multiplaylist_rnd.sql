delete from video;
delete from playlist;

insert into playlist
    (pk, id, title, uploader_id, added) values
    (1, 'plid1', 'pltitle1', 'user1', '2000-01-01 00:00:00'),
    (2, 'plid2', 'pltitle2', 'user2', '2000-01-01 00:00:00')
;

insert into video
    (pk, id, title, added, is_down) values
    (1, 'id1', 'title1', '2000-01-01 00:00:00', True)
;

insert into playlist_video
    (playlistpk, videopk) values
    (1, 1),
    (2, 1)
;

SELECT
    video.pk,
    video.id,
    video.title,
    video.added,
    video.is_down
FROM video
;