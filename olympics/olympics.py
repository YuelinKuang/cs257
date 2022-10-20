'''
    olympics.py
    Yuelin Kuang, 18 October 2022

    Adapted from psycopg2-sample.py from the psycopg2 lab.
'''
import config
import sys
import psycopg2

def get_connection():
    ''' Returns a database connection object with which you can create cursors,
        issue SQL queries, etc. This function is extremely aggressive about
        failed connections--it just prints an error message and kills the whole
        program. Sometimes that's the right choice, but it depends on your
        error-handling needs. '''
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

def get_athletes_by_noc(search_noc):
    ''' Returns a list of the names of all athletes in the database
        who are from the specified search_noc. '''
    athletes = [] 
    # When there is a noc abbreviation entered: 
    if search_noc is not None:
        try:
            query = '''SELECT DISTINCT athletes.name 
                        FROM athletes, noc, athletes_game_specific_info
                        WHERE athletes.id = athletes_game_specific_info.athlete_id
                        AND athletes_game_specific_info.noc_id = noc.id
                        AND noc.abbr ILIKE CONCAT('%%', %s, '%%')
                        ORDER BY athletes.name'''
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, (search_noc,))
            for row in cursor:
                full_name = row[0]
                athletes.append(full_name)

        except Exception as e:
            print(e, file=sys.stderr)

        connection.close()
        return athletes

    # When no noc abbreviation is entered: 
    else: 
        try: 
            query = '''SELECT athletes.name 
                        FROM athletes
                        ORDER BY athletes.name'''
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, (search_noc,))
            for row in cursor:
                full_name = row[0]
                athletes.append(full_name)

        except Exception as e:
            print(e, file=sys.stderr)

        connection.close()
        return athletes

def get_noc_and_gold_medals():
    ''' Returns a list of the nocs that have won at least one gold medal and the number
        of gold medals they won.'''
    noc_medal = []
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = '''SELECT noc.abbr, noc.region, COUNT(medals.class)
                   FROM noc, medals, athletes_games_events_medals
                   WHERE noc.id = athletes_games_events_medals.noc_id
                   AND athletes_games_events_medals.medal_id = medals.id
                   AND medals.class = 'Gold'
                   GROUP BY noc.abbr, noc.region
                   ORDER BY COUNT(medals.class) DESC'''
        cursor.execute(query)

        for row in cursor:
            noc_abbr = row[0]
            noc_region = row[1]
            number_of_gold_medals = row[2]
            noc_medal.append(f'{noc_abbr}, {noc_region}: {number_of_gold_medals}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return noc_medal

def get_games():
    ''' Returns a list of all Olympic games and the cities in which they happened.'''
    games = []
    try:
        query = '''SELECT games.year, games.season, games.city 
                   FROM games
                   ORDER BY games.year ASC, games.season DESC'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        
        for row in cursor:
            year = row[0]
            season = row[1]
            city = row[2]
            games.append(f'{year} {season} in {city}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return games

def invalid_args_and_print_help_page(invalid):
    if invalid: 
        print('\n\nThis is not a valid input. Please refer to the help page below. \n\n')
        with open('usage.txt', 'r') as file:
            print(file.read())
            print()
    else: 
        print('\n\nPlease refer to the help page below about how to use this program. \n\n')
        with open('usage.txt', 'r') as file:
            print(file.read())
            print()


def main(arguments):
    # args is a list of arguments excluding python3 and olympics.py
    args = arguments[1:]
    
    # When no argument is entered
    if len(args) == 0: 
        invalid_args_and_print_help_page(invalid=False)

    # When there is one argument
    elif len(args) == 1: 
        arg = args[0]
        if arg ==  '-h' or arg == '--help':
            invalid_args_and_print_help_page(invalid=False)
        elif arg == 'athletes': 
            print('============= All athletes =============')
            athletes = get_athletes_by_noc(None)
            for athlete in athletes:
                print(athlete)
            print()
        elif arg == 'noc':
            print('============= NOCs and the number of gold medals they won =============')
            nocs = get_noc_and_gold_medals()
            for noc in nocs: 
                print(noc)
            print()
        elif arg == 'games':
            print('============= All Olympic Games =============')
            games = get_games()
            for game in games: 
                print(game)
            print()
        else: 
            invalid_args_and_print_help_page(invalid=True)

    # When there are two arguments
    elif len(args) == 2: 
        if args[0] == 'athletes': 
            athletes = get_athletes_by_noc(args[1])
            if len(athletes) == 0: 
                print('There is no athlete from this NOC.')
            else: 
                print(f'============= All athletes from "{args[1].upper()}" =============')
                for athlete in athletes:
                    print(athlete)
        else: 
            invalid_args_and_print_help_page(invalid=True)
    
    else: 
        invalid_args_and_print_help_page(invalid=True)

if __name__ == '__main__':
    main(sys.argv)