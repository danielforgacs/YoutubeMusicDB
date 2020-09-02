-- CREATE DATABASE ymdb;
-- \c ymdb

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
	playlistpk		INTEGER			REFERENCES playlist,
	added			TIMESTAMP		NOT NUll,
	is_down			BOOLEAN			NOT NULL DEFAULT false
)
;
