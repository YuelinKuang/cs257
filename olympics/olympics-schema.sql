CREATE TABLE noc (
    id SERIAL,
    abbr char(3),
    region text,
    notes text
);

CREATE TABLE games (
    id SERIAL,
    game_name text,
    year integer,
    season text,
    city text
);

CREATE TABLE athletes (
    id SERIAL,
    name text,
);

CREATE TABLE athletes_game-specific_info (
    id SERIAL,
    athlete_id integer,
    game_id integer,
    sex text,
    age integer,
    height integer,
    weight integer,
    team text
);

CREATE TABLE medals (
    id SERIAL,
    class text
);

CREATE TABLE sports (
    id SERIAL,
    sport_name text
);

CREATE TABLE events (
    id SERIAL,
    event_name text,
    sport_id integer
);

CREATE TABLE athletes_games_events_noc_medals (
    athletes_id integer,
    game_id integer,
    event_id integer,
    noc_id integer,
    medal_id integer
);