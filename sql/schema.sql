CREATE TABLE playlist (
	pk				SMALLSERIAL		PRIMARY KEY,
	id				TEXT			NOT NULL UNIQUE,
	title			TEXT			NOT NULL,
	uploader_id		TEXT			NOT NULL,
	added			TIMESTAMP		NOT NUll
)
;

CREATE TABLE video (
	pk				SMALLSERIAL		PRIMARY KEY,
	id				TEXT			NOT NULL UNIQUE,
	title			TEXT			NOT NULL,
	playlist_pk		INTEGER			REFERENCES playlist,
	added			TIMESTAMP		NOT NUll,
	is_down			BOOLEAN			NOT NULL DEFAULT false
)
;

CREATE TABLE playlist_video (
	playlist_pk		INTEGER			REFERENCES playlist,
	video_pk		INTEGER			REFERENCES video,
	UNIQUE (playlist_pk, video_pk)
)
;