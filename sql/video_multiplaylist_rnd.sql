delete from playlist_video;
delete from video;
delete from playlist;

insert into playlist
    (pk, id, title, uploader_id, added) values
    (1, 'plid1', 'pltitle1', 'user1', '2000-01-01 00:00:00'),
    (2, 'plid2', 'pltitle2', 'user2', '2000-01-01 00:00:00'),
    (3, 'plid3', 'pltitle3', 'user3', '2000-01-01 00:00:00'),
    (4, 'plid4', 'pltitle4', 'user4', '2000-01-01 00:00:00'),
    (5, 'plid5', 'pltitle5', 'user5', '2000-01-01 00:00:00')
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
    (2, 2),
    (3, 1),
    (3, 2),
    (3, 3),
    (3, 5)
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


EXPLAIN
select 1, 2, 3
;


select
    playlist.pk,
    playlist.id,
    playlist.title
from playlist
join playlist_video on playlist_video.playlistpk = playlist.pk
WHERE playlist_video.videopk = 2
;


select (
    playlist.pk,
    playlist.id,
    playlist.title
)
from playlist
join playlist_video on playlist_video.playlistpk = playlist.pk
WHERE playlist_video.videopk = 2
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
        WHERE playlist_video.videopk = video.pk ),
    (select (
        playlist.pk,
        playlist.id,
        playlist.title
    )
    from playlist
    join playlist_video on playlist_video.playlistpk = playlist.pk
    WHERE playlist_video.videopk = 2
    limit 1)

FROM video
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
        WHERE playlist_video.videopk = video.pk ),
    (select 
        (playlist.pk,
        playlist.id,
        playlist.title)
    
    from playlist
    join playlist_video on playlist_video.playlistpk = playlist.pk
    WHERE playlist_video.videopk = 2)

FROM video
;

select array_agg(n) from generate_series(1,10) n group by n%2;
select array_agg(n) from generate_series(1,10) n;
select n from generate_series(1,10) n ;


SELECT ARRAY[
    ARRAY[1, 2],
    ARRAY[3, 4]]
;
SELECT ARRAY[
    ARRAY[pk, pk],
    ARRAY[pk, pk]]
from video
;

SELECT ARRAY (
    SELECT ARRAY[i, i*2]
FROM generate_series(1,5) AS a(i)
);



select array[
    cast (playlist.pk as text),
    playlist.id,
    playlist.title]
from playlist
;

select array_agg (array[
    cast (playlist.pk as text),
    playlist.id,
    playlist.title])
from playlist
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
        WHERE playlist_video.videopk = video.pk ) as plist_pks,
    (
        select array_agg (array[
        cast (playlist.pk as text), playlist.id, playlist.title])
        from playlist
    )
FROM video
;



-- WORKS, WORKS, WORKS, WORKS, WORKS, WORKS, WORKS, 
-- WORKS, WORKS, WORKS, WORKS, WORKS, WORKS, WORKS, 
-- WORKS, WORKS, WORKS, WORKS, WORKS, WORKS, WORKS, 
-- WORKS, WORKS, WORKS, WORKS, WORKS, WORKS, WORKS, 

-- 
-- THIS IS IT +++++++++++++++++++++++++++++
-- THIS IS IT +++++++++++++++++++++++++++++
-- THIS IS IT +++++++++++++++++++++++++++++
-- 

SELECT
    video.pk,
    video.id,
    video.title,
    video.added,
    video.is_down,
    array (
        select playlistpk
        from playlist_video
        WHERE playlist_video.videopk = video.pk ) as plist_pks,
    (
        select array_agg (
            array [
                cast (playlist.pk as text),
                playlist.id,
                playlist.title
            ])
        from playlist
        join playlist_video on playlist_video.playlistpk = playlist.pk
        where playlist_video.videopk = video.pk
    )
FROM video
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
        WHERE playlist_video.videopk = video.pk ),
    (
        select array_agg (array[
        cast (playlist.pk as text), playlist.id, playlist.title])
        from playlist
        join playlist_video on playlist_video.playlistpk = playlist.pk
        where playlist_video.videopk = video.pk
    )
FROM video
;



SELECT
    video.pk,
    video.id,
    video.title,
    video.added,
    video.is_down,
    playlist.id as playlist_id,
    playlist.title as playlist_title
FROM video
LEFT JOIN playlist ON playlist.pk = video.playlistpk
ORDER BY video.pk
;

-- FINAL:

SELECT
    video.pk,
    video.id,
    video.title,
    video.added,
    video.is_down,
    NULL AS playlist_id,
    NULL AS playlist_title,
    array (
        SELECT playlistpk
        FROM playlist_video
        WHERE playlist_video.videopk = video.pk
    ) AS playlist_pks,
    (
        SELECT array_agg (array[
            playlist.id,
            playlist.title])
        FROM playlist
        JOIN playlist_video ON playlist_video.playlistpk = playlist.pk
        WHERE playlist_video.videopk = video.pk
    ) as playlists
FROM video
ORDER BY video.pk
;
