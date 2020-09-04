insert into playlist
    (pk, id, title, uploader_id, added) values
    ( 1, 'plid_1', 'pltitle_1', 'user_1', '2000-01-01 00:00:00'),
    ( 2, 'plid_2', 'pltitle_2', 'user_2', '2000-01-01 00:00:00'),
    ( 3, 'plid_3', 'pltitle_3', 'user_3', '2000-01-01 00:00:00'),
    ( 4, 'plid_4', 'pltitle_4', 'user_4', '2000-01-01 00:00:00'),
    ( 5, 'plid_5', 'pltitle_5', 'user_5', '2000-01-01 00:00:00'),
    ( 6, 'plid_6', 'pltitle_6', 'user_6', '2000-01-01 00:00:00'),
    ( 7, 'plid_7', 'pltitle_7', 'user_7', '2000-01-01 00:00:00'),
    ( 8, 'plid_8', 'pltitle_8', 'user_8', '2000-01-01 00:00:00'),
    ( 9, 'plid_9', 'pltitle_9', 'user_9', '2000-01-01 00:00:00'),
    (10, 'plid_10', 'pltitle_10', 'user_10', '2000-01-01 00:00:00')
;

insert into video
    (pk, id, title, added, is_down) values
    ( 1, 'id_1', 'title_1', '2000-01-01 00:00:00', false), --playlists: 1
    ( 2, 'id_2', 'title_2', '2000-01-01 00:00:00', false), --playlists: 1, 2
    ( 3, 'id_3', 'title_3', '2000-01-01 00:00:00', false), --playlists: 1, 2, 3
    ( 4, 'id_4', 'title_4', '2000-01-01 00:00:00', false), --playlists: 1, 2, 3, 4
    ( 5, 'id_5', 'title_5', '2000-01-01 00:00:00', false), --playlists:
    ( 6, 'id_6', 'title_6', '2000-01-01 00:00:00', false), --playlists:
    ( 7, 'id_7', 'title_7', '2000-01-01 00:00:00', false), --playlists:
    ( 8, 'id_8', 'title_8', '2000-01-01 00:00:00', false), --playlists:
    ( 9, 'id_9', 'title_9', '2000-01-01 00:00:00', false), --playlists:
    (10, 'id_10', 'title_10', '2000-01-01 00:00:00', false) --playlists:
;

insert into playlist_video
    (playlistpk, videopk) values
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),

    (2, 2),
    (2, 3),
    (2, 4),

    (3, 3),
    (3, 4)
;
