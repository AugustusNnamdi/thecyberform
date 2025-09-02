
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TEXT  DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    content TEXT NOT NULL
);

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    member_since TEXT  DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

DROP TABLE IF EXISTS comments;

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    author TEXT NOT NULL,
    content TEXT NOT NULL,
    created TEXT  DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);