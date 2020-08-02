CREATE DATABASE ymdb;

\c ymdb

CREATE TABLE playlist (
	id				SMALLSERIAL		PRIMARY KEY,
	title			TEXT			NOT NULL,
	youtubeid		TEXT			NOT NULL UNIQUE
)
;

CREATE TABLE song (
	id				SMALLSERIAL		PRIMARY KEY,
	title			TEXT			NOT NULL,
	youtubeid		TEXT			NOT NULL UNIQUE,
	playlist		INTEGER			REFERENCES playlist
)
;
