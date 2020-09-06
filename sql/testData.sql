insert into playlist
    (pk, id, title, uploader_id, added) values
    (1, 'plid1', 'pltitle1', 'user1', '2000-01-01 00:00:00'),
    (2, 'plid2', 'pltitle2', 'user2', '2000-01-01 00:00:00'),
    (3, 'plid3', 'pltitle3', 'user3', '2000-01-01 00:00:00'),
    (4, 'plid4', 'pltitle4', 'user4', '2000-01-01 00:00:00'),
    (5, 'plid5', 'pltitle5', 'user5', '2000-01-01 00:00:00'),
    (6, 'plid6', 'pltitle6', 'user6', '2000-01-01 00:00:00'),
    (7, 'plid7', 'pltitle7', 'user7', '2000-01-01 00:00:00'),
    (8, 'plid8', 'pltitle8', 'user8', '2000-01-01 00:00:00'),
    (9, 'plid9', 'pltitle9', 'user9', '2000-01-01 00:00:00'),
    (10, 'plid10', 'pltitle10', 'user10', '2000-01-01 00:00:00')
;

insert into video
    (pk, id, title, added, is_down) values
    (1, 'id1', 'title1', '2000-01-01 00:00:00', false),
    (2, 'id2', 'title2', '2000-01-01 00:00:00', false),
    (3, 'id3', 'title3', '2000-01-01 00:00:00', false),
    (4, 'id4', 'title4', '2000-01-01 00:00:00', false),
    (5, 'id5', 'title5', '2000-01-01 00:00:00', false),
    (6, 'id6', 'title6', '2000-01-01 00:00:00', false),
    (7, 'id7', 'title7', '2000-01-01 00:00:00', false),
    (8, 'id8', 'title8', '2000-01-01 00:00:00', false),
    (9, 'id9', 'title9', '2000-01-01 00:00:00', false),
    (10, 'id10', 'title10', '2000-01-01 00:00:00', false)
;

insert into playlist_video
    (playlist_pk, video_pk) values
    (1, 1),

    (2, 1),
    (2, 2),

    (3, 1),
    (3, 2),
    (3, 3),

    (4, 3),
    (4, 4),
    (4, 5),
    (4, 6),
    (4, 7),

    (10, 10)
;

update video
set playlist_pk = 1
where pk = 2
;

update video
set playlist_pk = 2
where pk in (4, 5)
;
