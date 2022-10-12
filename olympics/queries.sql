SELECT abbr AS noc_abbreviation, region 
FROM noc
ORDER BY abbr ASC;

SELECT DISTINCT athletes.name 
FROM athletes, noc, athletes_game_specific_info
WHERE athletes.id = athletes_game_specific_info.athlete_id
AND athletes_game_specific_info.noc_id = noc.id
AND noc.abbr = 'JAM';

SELECT athletes.name AS athlete_name, events.event_name, games.game_name AS game, medals.class AS result
FROM events, games, medals, athletes, athletes_games_events_medals
WHERE athletes.name LIKE '%Greg% %Louganis%'
AND medals.class != ''
AND athletes.id = athletes_games_events_medals.athlete_id
AND medals.id = athletes_games_events_medals.medal_id
AND events.id = athletes_games_events_medals.event_id
AND games.id = athletes_games_events_medals.game_id
ORDER BY games.year ASC;

SELECT noc.abbr AS noc_abbreviation, noc.region, COUNT(medals.class) AS count_of_gold_medals
FROM noc, medals, athletes_games_events_medals
WHERE noc.id = athletes_games_events_medals.noc_id
AND athletes_games_events_medals.medal_id = medals.id
AND medals.class LIKE '%Gold%'
GROUP BY noc.abbr, noc.region
ORDER BY COUNT(medals.class) DESC;