SELECT abbr, region 
FROM noc
ORDER BY abbr ASC

SELECT athletes.name 
FROM athletes, noc, athletes_game-specific_info, athletes_games_events_noc_medals
WHERE athletes.id = athletes_game-specific_info.athlete_id
AND athletes_game-specific_info.id = athletes_games_events_noc_medals.athletes_game-specific_info_id
AND athletes_games_events_noc_medals.noc_id = noc.id 
AND noc.abbr = 'JAM'

SELECT events.event_name, games.game_name, medals.class
FROM events, games, medals, athletes, athletes_games_events_noc_medals, athletes_game-specific_info
WHERE athletes.name = "Greg Louganis"
AND atheletes.id = athletes_game-specific_info.athlete_id
AND athletes_game-specific_info.id = athletes_games_events_noc_medals.athletes_game-specific_info_id
AND athletes_games_events_noc_medals.medal_id = medals.id