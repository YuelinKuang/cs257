'''
    Yuelin Kuang,
    9 October 2022, written for the olympics project for CS257-fall-22. 

    Data files athlete_events.csv and noc_regions.csv come from Kaggle: 
    https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results
'''

import csv

all_noc = {}

with open('noc_regions.csv') as noc_regions:
    noc_reader = csv.reader(noc_regions, delimiter=',')
    next(noc_reader)
    with open('noc.csv', 'w', newline='') as noc:
        noc_writer = csv.writer(noc)
        noc_writer.writerow(["id", "abbr", "region", "notes"])
        id_count = 1
        for noc in noc_reader:
            all_noc[noc[0]] = id_count
            noc_writer.writerow([id_count, noc[0], noc[1], noc[2]])
            id_count += 1


with open('athlete_events.csv', 'r') as athlete_events:
    athlete_events_reader = csv.reader(athlete_events, delimiter=',')

    with open('games.csv', 'w') as games, open('athletes.csv', 'w') as athletes, \
        open('sports.csv', 'w') as sports, open('events.csv', 'w') as events, \
        open('athletes_game_specific_info.csv', 'w') as athletes_game_specific_info, \
        open('medals.csv', 'w') as medals, open('athletes_games_events_medals.csv', 'w') as athletes_games_events_medals: 

        games_writer = csv.writer(games)
        games_writer.writerow(['id', 'game_name', 'year', 'season', 'city'])

        athletes_writer = csv.writer(athletes)
        athletes_writer.writerow(['id','name'])

        sports_writer = csv.writer(sports)
        sports_writer.writerow(['id', 'sport_name'])

        events_writer = csv.writer(events)
        events_writer.writerow(['id', 'sport_id', 'event_name'])

        athletes_game_specific_info_writer = csv.writer(athletes_game_specific_info)
        athletes_game_specific_info_writer.writerow(['id', 'athlete_id', 'game_id', 'sex', \
            'age', 'height', 'weight', 'team', 'noc_id'])

        athletes_games_events_medals_writer = csv.writer(athletes_games_events_medals)
        athletes_games_events_medals_writer.writerow(['athletes_game_specific_info_id', 'athlete_id', 'game_id', 'event_id', 'medal_id'])

        medals_writer = csv.writer(medals)
        medals_writer.writerow(['id', 'class'])
        
        # my_dic['text'] = id -> look up id using name
        all_games = {}
        all_sports = {}
        all_events = {}
        all_medals = {}
        # all_athletes[id] = 'name'
        all_athletes = {}

        next(athlete_events_reader)

        counter = 1

        for row in athlete_events_reader:
            athlete_id = row[0]
            athlete_name = row[1]
            sex = row[2]
            age = row[3]
            height = row[4]
            weight = row[5]
            team = row[6] 
            noc = row[7]
            game = row[8] 
            year = row[9]
            season = row[10]
            city = row[11]
            sport = row[12]
            event = row[13]
            medal = row[14]

            if game not in all_games:
                # id starts at 1
                game_id = len(all_games) + 1
                all_games[game] = game_id
                games_writer.writerow([game_id, game, year, season, city])

            if athlete_id not in all_athletes:
                # id starts at 1
                all_athletes[athlete_id] = athlete_name
                athletes_writer.writerow([athlete_id, athlete_name])

            if sport not in all_sports:
                # id starts at 1
                sport_id = len(all_sports) + 1
                all_sports[sport] = sport_id
                sports_writer.writerow([sport_id, sport])

            if event not in all_events:
                # id starts at 1
                event_id = len(all_events) + 1
                all_events[event] = event_id
                events_writer.writerow([event_id, all_sports[sport], event])

            if medal not in all_medals:
                #id starts at 1
                medal_id = len(all_medals) + 1
                all_medals[medal] = medal_id
                medals_writer.writerow([medal_id, medal])

            athletes_game_specific_info_writer.writerow([counter, athlete_id, \
                all_games[game], sex, age, height, weight, team, all_noc[noc]])

            athletes_games_events_medals_writer.writerow([counter, athlete_id, \
                all_games[game], all_events[event], all_medals[medal]])

            counter += 1

            