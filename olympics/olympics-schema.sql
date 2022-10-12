CREATE TABLE noc (
    id SERIAL,
    abbr char(3),
    region TEXT,
    notes TEXT
);

CREATE TABLE teams (
    id INTEGER,
    team_name TEXT
);

CREATE TABLE games (
    id SERIAL,
    game_name TEXT,
    year INTEGER,
    season TEXT,
    city TEXT
);

CREATE TABLE athletes (
    id SERIAL,
    name TEXT
);

CREATE TABLE athletes_game_specific_info (
    id SERIAL,
    athlete_id INTEGER,
    game_id INTEGER,
    sex TEXT,
    age INTEGER,
    height REAL,
    weight REAL,
    team_id INTEGER,
    noc_id INTEGER
);

CREATE TABLE medals (
    id SERIAL,
    class TEXT
);

CREATE TABLE sports (
    id SERIAL,
    sport_name TEXT
);

CREATE TABLE events (
    id SERIAL,
    sport_id INTEGER,
    event_name TEXT
);

CREATE TABLE athletes_games_events_medals (
    athletes_game_specific_info_id INTEGER,
    athlete_id INTEGER,
    game_id INTEGER,
    event_id INTEGER,
    medal_id INTEGER,
    noc_id INTEGER
);