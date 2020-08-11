-- CREATE DATABASE ymdb;

-- \c ymdb

CREATE TABLE playlist (
	pk				SMALLSERIAL		PRIMARY KEY,
	id				TEXT			NOT NULL UNIQUE,
	title			TEXT			NOT NULL,
	uploader_id		TEXT			NOT NULL
)
;

CREATE TABLE video (
	pk				SMALLSERIAL		PRIMARY KEY,
	id				TEXT			NOT NULL UNIQUE,
	title			TEXT			NOT NULL,
	playlist		INTEGER			REFERENCES playlist
)
;
