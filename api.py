'''
    api.py
    Lucie Wolf and Yuelin Kuang
    9 Nov 2022

    Web application project for CS257.
'''
import sys
import flask
import json
import config
import psycopg2
import queries

api = flask.Blueprint('api', __name__)

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)

@api.route('/genres/') 
def get_genres():
    #Returns a list of all the genres in our database

    query = queries.get_genres

    genres_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            genre = {'id':row[0], 'genre_name':row[1]}
            genres_list.append(genre)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(genres_list)

@api.route('/developers/') 
def get_developers():
    #Returns a list of all the developers in our database

    query = queries.get_developers

    developers_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            genre = {'id':row[0], 'developer_name':row[1]}
            developers_list.append(genre)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(developers_list)

@api.route('/games/') 
def get_games():
    # Returns a list of all the games in our database, based on input parameters

    query = queries.all_game_information_search

    additional_arguments = []

    if 'genre_id' in flask.request.args: 
        query += ' AND genre.id = %s'
        game_genre_id = flask.request.args.get('genre_id')
        additional_arguments.append(str(game_genre_id))
    if 'title' in flask.request.args:
        query += " AND game.title ILIKE CONCAT('%%', %s, '%%')"
        title = flask.request.args.get('title')
        additional_arguments.append(str(title))
    if 'min_age_above' in flask.request.args: 
        query += ' AND game.minimum_age >= %s'
        min_age_above = flask.request.args.get('min_age_above')
        additional_arguments.append(str(min_age_above))
    if 'min_age_below' in flask.request.args: 
        query += ' AND game.minimum_age <= %s'
        min_age_below = flask.request.args.get('min_age_below')
        additional_arguments.append(str(min_age_below))  
    if 'start_date' in flask.request.args: 
        query += ' AND game.release_date >= %s'
        start_date = flask.request.args.get('start_date')
        additional_arguments.append(str(start_date))
    if 'end_date' in flask.request.args: 
        query += ' AND game.release_date <= %s'
        end_date = flask.request.args.get('end_date')
        additional_arguments.append(str(end_date))
    if 'developer_id' in flask.request.args: 
        query += ' AND developer.id = %s'
        developer_id = flask.request.args.get('developer_id')
        additional_arguments.append(str(developer_id))
    if 'platforms' in flask.request.args: 
        # "w, m, l"
        platforms = flask.request.args.get('platforms').split(',')
        if len(platforms) == 1: 
            if 'w' in platforms: 
                query += ' AND game.windows_support = true'
            if 'm' in platforms: 
                query += ' AND game.mac_support = true'
            if 'l' in platforms: 
                query += ' AND game.linux_support = true'
        elif len(platforms) == 2: 
            if 'w' in platforms and 'm' in platforms: 
                query += ' AND (game.windows_support = true AND game.mac_support = true)'
            if 'w' in platforms and 'l' in platforms: 
                query += ' AND (game.windows_support = true AND game.linux_support = true)'
            if 'm' in platforms and 'l' in platforms: 
                query += ' AND (game.mac_support = true AND game.linux_support = true)'
        elif len(platforms) == 3: 
            query += ' AND (game.windows_support = true AND game.mac_support = true AND game.linux_support = true)'
        else: 
            pass
    if 'price_above' in flask.request.args: 
        query += ' AND game.price >= %s'
        price_above = flask.request.args.get('price_above')
        additional_arguments.append(str(price_above))
    if 'price_below' in flask.request.args: 
        query += ' AND game.price <= %s'
        price_below = flask.request.args.get('price_below')
        additional_arguments.append(str(price_below))
    if 'pos_ratings_above' in flask.request.args: 
        query += ' AND game.pos_ratings >= %s'
        pos_ratings_above = flask.request.args.get('pos_ratings_above')
        additional_arguments.append(str(pos_ratings_above))
    if 'pos_ratings_below' in flask.request.args: 
        query += ' AND game.pos_ratings <= %s'
        pos_ratings_below = flask.request.args.get('pos_ratings_below')
        additional_arguments.append(str(pos_ratings_below))
    if 'total_ratings_above' in flask.request.args:
        query += ' AND SUM(game.pos_ratings + game.neg_ratings) >= %s'
        total_ratings_above = flask.request.args.get('total_ratings_above')
        additional_arguments.append(str(total_ratings_above))
    if 'total_ratings_below' in flask.request.args:
        query += ' AND SUM(game.pos_ratings + game.neg_ratings) <= %s'
        total_ratings_below = flask.request.args.get('total_ratings_below')
        additional_arguments.append(str(total_ratings_below))
    # if 'neg_ratings_higher_than' in flask.request.args: 
    #     query += ' AND game.neg_ratings >= %s'
    #     neg_ratings_higher_than = flask.request.args.get('neg_ratings_higher_than')
    #     additional_arguments.append(str(neg_ratings_higher_than))
    # if 'neg_ratings_lower_than' in flask.request.args: 
    #     query += ' AND game.neg_ratings <= %s'
    #     neg_ratings_lower_than = flask.request.args.get('neg_ratings_lower_than')
    #     additional_arguments.append(str(neg_ratings_lower_than))

    # implementation not complete
    if 'sort_by' in flask.request.args:
        sort = flask.request.args.get('sort_by')
        query += " ORDER BY game.title;"
        # additional_arguments.append(str(sort))
    else: 
        query += " ORDER BY game.title;"

    game_list = []

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, additional_arguments)
        # cursor.execute(query, (user_input,))

        game = {'id': 0,
                'title': '',
                'description': '',
                'media': {}}
        game_ids = []

        # indices: 
        # 0 game.id, 1 game.title, 2 game.release_date, 
        # 3 game.english_support, 4 game.windows_support, 
        # 5 game.mac_support, 6 game.linux_support, 
        # 7 game.minimum_age, 8 game.pos_ratings, 
        # 9 game.neg_ratings, 10 game.price, 11 game.described, 
        # 12 game.website, 13 game.media, 14 developer.developer_name, 
        # 15 publisher.publisher_name, 16 category.category_name,
        # 17 genre.genre_name

        for row in cursor: 
            game_id = row[0]
            game_title = row[1]
            game_description = row[11]
            game_media = row[13]
            if game_id not in game_ids: 
                images = json.loads(game_media.replace("'", '"'))
                if images['header_image'] == '':
                    images['header_image'] = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.simplystamps.com%2Fmedia%2Fcatalog%2Fproduct%2F5%2F8%2F5802-n-a-stock-stamp-hcb.png&f=1&nofb=1&ipt=4c91608ffabe756cef98c89e32321f03e9ae4c3ab4a92fb4b68453801fd7cf7e&ipo=images'
                game = {'id': str(game_id),
                        'title': game_title,
                        'description': game_description,
                        'media': images}
                game_ids.append(game_id)
                game_list.append(game)
            
        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(game_list)


@api.route('/games/specific/<game_id>') 
def get_a_specific_game(game_id):
    # Returns a dictionary of a particular game in our database, based on game id

    query = queries.specific_game_info

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (game_id,))

        # indices: 
        #     0 game.title, 1 game.release_date, 
        #     2 game.english_support, 3 game.windows_support, 
        #     4 game.mac_support, 5 game.linux_support, 
        #     6 game.minimum_age, 7 game.pos_ratings, 
        #     8 game.neg_ratings, 9 game.price, 10 game.described, 
        #     11 game.link, 12 game.media, 13 developer.developer_name, 
        #     14 publisher.publisher_name, 15 category.category_name,
        #     16 genre.genre_name

        game = {'title': '',
                'release_date': '', 
                'english_support': False,
                'windows_support': False,
                'mac_support': False,
                'linux_support': False, 
                'minimum_age': 0,
                'pos_ratings': 0,
                'neg_ratings': 0,
                'price': 0.0,
                'description': '',
                'website': '',
                'media': '',
                'developers': [],
                'publishers': [], 
                'categories': [],
                'genres': []}

        count = 0
        for row in cursor:
            if count == 0: 
                images = json.loads(row[12].replace("'", '"'))
                if images['header_image'] == '':
                    images['header_image'] = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.simplystamps.com%2Fmedia%2Fcatalog%2Fproduct%2F5%2F8%2F5802-n-a-stock-stamp-hcb.png&f=1&nofb=1&ipt=4c91608ffabe756cef98c89e32321f03e9ae4c3ab4a92fb4b68453801fd7cf7e&ipo=images'

                game = {'title': row[0],
                        'release_date': str(row[1]), 
                        'english_support': row[2],
                        'windows_support': row[3],
                        'mac_support': row[4],
                        'linux_support': row[5], 
                        'minimum_age': row[6],
                        'pos_ratings': row[7],
                        'neg_ratings': row[8],
                        'price': row[9],
                        'description': row[10],
                        'website': row[11],
                        'media': images,
                        'developers': [row[13]],
                        'publishers': [row[14]], 
                        'categories': [row[15]],
                        'genres': [row[16]]
                        }
                count += 1
            else: 
                game['developers'].append(row[13])
                game['publishers'].append(row[14])
                game['categories'].append(row[15])
                game['genres'].append(row[16])
            
        game['developers'] = ', '.join(set(game['developers']))
        game['publishers'] = ', '.join(set(game['publishers']))
        game['categories'] = ', '.join(set(game['categories']))
        game['genres'] = ', '.join(set(game['genres']))

        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(game)