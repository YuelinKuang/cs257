SELECT abbr, region 
FROM noc
ORDER BY abbr ASC

SELECT DISTINCT athletes.name 
FROM athletes, noc, athletes_game-specific_info
WHERE athletes.id = athletes_game-specific_info.athlete_id
AND athletes_game-specific_info.noc_id = noc.id
AND noc.abbr = 'JAM'

SELECT events.event_name, games.game_name, medals.class
FROM events, games, medals, athletes, athletes_games_events_medals
WHERE athletes.name = "Greg Louganis"
AND medals.class != 'NA'
AND atheletes.id = athletes_games_events_medals.athlete_id
AND athletes_games_events_medals.medal_id = medals.id
ORDER BY game.year ASC

SELECT noc.abbr, COUNT(medals.class)
FROM noc, medals, athletes_game-specific_info, athletes_games_events_medals
WHERE medals.class = 'Gold'
AND athletes_games_events_medals.medal_id = medals.id
AND noc.id = athletes_game-specific_info.noc_id
AND athletes_game-specific_info.athlete_id = athletes_games_events_medals.athlete_id
AND athletes_game-specific_info.game_id = athletes_games_events_medals.game_id
GROUP BY noc.abbr
ORDER BY COUNT(medals.class) DESC
