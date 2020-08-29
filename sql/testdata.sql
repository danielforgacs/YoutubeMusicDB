\c ymdb

delete from playlist;
delete from song;

insert into playlist (title, youtubeid)
	values 
		('playlist 01', 'plid-01')
		,('playlist 02', 'plid-02')
		,('playlist 03', 'plid-03')
	
;

select * from playlist;

insert into song (title, youtubeid, playlist)
	values
		('song 01', 'sid 01', 1)
		,('song 02', 'sid 02', (select id from playlist order by id desc limit 1))
		,('song 03', 'sid 03', null)
;
