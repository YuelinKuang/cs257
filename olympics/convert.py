'''
    Yuelin Kuang,
    9 October 2022, written for the olympics project for CS257-fall-22. 

    Data files athlete_events.csv and noc_regions.csv come from Kaggle: 
    https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results
'''

import csv

all_noc = []

with open('noc_regions.csv') as noc_regions:
    noc_reader = csv.reader(noc_regions, delimiter=',')
    next(noc_reader)
    with open('noc.csv', 'w', newline='') as noc:
        noc_writer = csv.writer(noc)
        noc_writer.writerow(["id", "abbr", "region", "notes"])
        id_count = 1
        for noc in noc_reader:
            all_noc.append(noc[0])
            noc_writer.writerow([id_count, noc[0], noc[1], noc[2]])
            id_count += 1


with open('athlete_events.csv', 'r') as athlete_events:
    athlete_events_reader = csv.reader(athlete_events, delimiter=',')

    with open('games.csv', 'w') as games, open('athletes.csv', 'w') as athletes, \
        open('sports.csv', 'w') as sports, open('events.csv', 'w') as events, \
        open('athletes_game-specific_info.csv', 'w') as athletes_game_specific_info, \
        open('medals.csv', 'w') as medals, open('athletes_games_events_medals.csv', 'w') as athletes_games_events_medals: 

        games_writer = csv.writer(games)
        games_writer.writerow(['id', 'game_name', 'year', 'season', 'city'])

        athletes_writer = csv.writer(athletes)
        athletes_writer.writerow(['id','name','sex'])

        sports_writer = csv.writer(sports)
        sports_writer.writerow(['id', 'sport_name'])

        events_writer = csv.writer(events)
        events_writer.writerow(['id', 'event_name', 'sport_id'])

        athletes_game_specific_info_writer = csv.writer(athletes_game_specific_info)
        athletes_game_specific_info_writer.writerow(['id', 'athlete_id', 'game_id', 'sex', \
            'age', 'height', 'weight', 'team'])

        athletes_games_events_medals_writer = csv.writer(athletes_games_events_medals)
        athletes_games_events_medals_writer.writerow(['athlete_id', 'game_id', 'event_id', 'noc_id', 'medal_id'])

        medals_writer = csv.writer(medals)
        medals_writer.writerow(['id', 'class'])
        
        all_games = []
        all_athletes = []
        all_sports = []
        all_events = []
        all_medals = []

        next(athlete_events_reader)

        counter = 1

        for row in athlete_events_reader:
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
                all_games.append(game)
                games_writer.writerow([len(all_games), game, year, season, city])

            if athlete_name not in all_athletes:
                # id starts at 1
                all_athletes.append(athlete_name)
                athletes_writer.writerow([len(all_athletes), athlete_name])

            if sport not in all_sports:
                # id starts at 1
                all_sports.append(sport)
                sports_writer.writerow([len(all_sports), sport])

            if event not in all_events:
                # id starts at 1
                all_events.append(event)
                events_writer.writerow([len(all_events), event, all_sports.index(sport) + 1])

            if medal not in all_medals:
                #id starts at 1
                all_medals.append(medal)
                medals_writer.writerow([len(all_medals), medal])

            athletes_game_specific_info_writer.writerow([counter, all_athletes.index(athlete_name) + 1, \
                all_games.index(game) + 1, sex, age, height, weight, team])

            athletes_games_events_medals_writer.writerow([all_athletes.index(athlete_name) + 1, \
                all_games.index(game) + 1, all_events.index(event) + 1, all_noc.index(noc) + 1, all_medals.index(medal) + 1])

            counter += 1

            