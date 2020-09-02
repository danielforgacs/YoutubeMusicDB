delete from playlist_video;
delete from video;
delete from playlist;

insert into playlist
    (pk, id, title, uploader_id, added) values
    (1, 'plid1', 'pltitle1', 'user1', '2000-01-01 00:00:00'),
    (2, 'plid2', 'pltitle2', 'user2', '2000-01-01 00:00:00'),
    (3, 'plid3', 'pltitle3', 'user3', '2000-01-01 00:00:00')
;

insert into video
    (pk, id, title, added, is_down) values
    (1, 'id1', 'title1', '2000-01-01 00:00:00', True),
    (2, 'id2', 'title2', '2000-01-01 00:00:00', True),
    (3, 'id3', 'title3', '2000-01-01 00:00:00', True),
    (4, 'id4', 'title4', '2000-01-01 00:00:00', True),
    (5, 'id5', 'title5', '2000-01-01 00:00:00', True)
;

insert into playlist_video
    (playlistpk, videopk) values
    (1, 1),
    (2, 1),
    (2, 2)
;

SELECT
    video.pk,
    video.id,
    video.title,
    video.added,
    video.is_down,
    array (
        select playlistpk
        from playlist_video
        WHERE playlist_video.videopk = video.pk
    )
FROM video
;