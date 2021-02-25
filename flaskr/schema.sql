DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE song (
    id INTEGER PRIMARY KEY,
    name_of_song VARCHAR(100) NOT NULL,
    duration INTEGER NOT NULL CHECK (duration >= 0),
    uploaded_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE podcast (
    id INTEGER PRIMARY KEY,
    name_of_podcast CHAR(100) NOT NULL,
    duration INTEGER NOT NULL CHECK (duration >= 0),
    uploaded_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    host VARCHAR(100) NOT NULL,
    participant VARCHAR
);

CREATE TABLE audiobook (
    id INTEGER PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    narrator VARCHAR(100) NOT NULL,
    duration INTEGER NOT NULL CHECK (duration >= 0),
    uploaded_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
    

