\set plistid '\'PL9YsudagsL6hicXrha4zBId875lRXxc32\''

select * from video;

SELECT video.id
FROM video
JOIN playlist ON playlist.pk = video.playlist
WHERE playlist.id = :plistid
;
