insert into playlist
    (pk, id, title, uploader_id, added) values
    (1, 'plid1', 'pltitle1', 'user1', '2000-01-01 00:00:00'),
    (2, 'plid2', 'pltitle2', 'user2', '2000-01-01 00:00:00')
;

insert into video
    (pk, id, title, added, is_down) values
    (1, 'id1', 'title1', '2000-01-01 00:00:00', True),
    (2, 'id2', 'title2', '2000-01-01 00:00:00', false),
    (3, 'id3', 'title3', '2000-01-01 00:00:00', false),
    (4, 'id4', 'title4', '2000-01-01 00:00:00', True),
    (5, 'id5', 'title5', '2000-01-01 00:00:00', false)
;

update video
set playlistpk = 1
where pk = 2
;

update video
set playlistpk = 2
where pk in (4, 5)
;
