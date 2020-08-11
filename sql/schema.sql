-- CREATE DATABASE ymdb;

-- \c ymdb

CREATE TABLE playlist (
	id				SMALLSERIAL		PRIMARY KEY,
	youtubeid		TEXT			NOT NULL UNIQUE,
	title			TEXT			NOT NULL,
	uploaderid		TEXT			NOT NULL
)
;

CREATE TABLE video (
	id				SMALLSERIAL		PRIMARY KEY,
	youtubeid		TEXT			NOT NULL UNIQUE,
	title			TEXT			NOT NULL,
	playlist		INTEGER			REFERENCES playlist
)
;
