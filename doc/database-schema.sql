/*  Written by Lucie Wolf and Yuelin Kuang
    database-schema.sql
    Nov 6, 2022 
    */

CREATE TABLE game (
    id SERIAL,
    title TEXT,
    release_date DATE, 
    english_support BOOLEAN,
    windows_support BOOLEAN,
    mac_support BOOLEAN,
    linux_support BOOLEAN,
    minimum_age INTEGER,
    pos_ratings INTEGER,
    neg_ratings INTEGER,
    price FLOAT,
    described TEXT,
    website TEXT
);

CREATE TABLE developer (
    id SERIAL,
    developer_name TEXT
);

CREATE TABLE publisher (
    id SERIAL,
    publisher_name TEXT
);

CREATE TABLE category (
    id SERIAL,
    category_name TEXT
);

CREATE TABLE genre (
    id SERIAL,
    genre_name TEXT
);

CREATE TABLE media (
    id SERIAL,
    media_link, TEXT
);

CREATE TABLE game_developer (
    game_id, INTEGER,
    developer_id INTEGER
);

CREATE TABLE game_publisher (
    game_id, INTEGER,
    publisher_id INTEGER
);

CREATE TABLE game_category (
    game_id, INTEGER,
    category_id INTEGER
);

CREATE TABLE game_genre (
    game_id, INTEGER,
    genre_id INTEGER
);

CREATE TABLE game_media (
    game_id, INTEGER,
    media_id INTEGER
);
