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
# quesries.py contains all the queries used in api.py

api = flask.Blueprint('api', __name__)

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)



@api.route('/help')
def get_help():
    # Returns api-design.txt as straightforward text
    # api-design.txt contains documentation of all the endpoints implemented in api.py
    f = open('doc/api-design.txt','r')
    text = f.read()
    f.close()
    return text


@api.route('/genres') 
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


@api.route('/developers') 
def get_developers():
    # Returns a list of all the developers in our database

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


@api.route('/main_page_images')
def get_main_images():
    # Returns a list of 98 games randomly selected from our database 
    # (only their id's and media included)

    query = queries.get_main_page_images

    games_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            images = json.loads(row[2].replace("'", '"'))
            if images['header_image'] == '':
                images['header_image'] = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.simplystamps.com%2Fmedia%2Fcatalog%2Fproduct%2F5%2F8%2F5802-n-a-stock-stamp-hcb.png&f=1&nofb=1&ipt=4c91608ffabe756cef98c89e32321f03e9ae4c3ab4a92fb4b68453801fd7cf7e&ipo=images'
            game = {'id':row[0], 'title':row[1], 'media':images, 'website':row[3]}
            games_list.append(game)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(games_list)


@api.route('/games') 
def get_games():
    # Returns a list of all the games in our database, based on input parameters

    # Get initial filters
    result_query, query_args = add_args_to_query(flask.request.args, False)[:2]
    query = queries.all_game_information_search + result_query

    # Add sort_by information to query
    sort_params = flask.request.args.get('sort_by').split('-')
    sort_by = sort_params[0]
    sort_order = sort_params[1]
    if sort_by == 'title': 
        query += ' ORDER BY game.title'
    elif sort_by == 'date':
        query += ' ORDER BY game.release_date'
    elif sort_by == 'price':
        query += ' ORDER BY game.price'
    elif sort_by == 'age':
        query += ' ORDER BY game.minimum_age'
    elif sort_by == 'pos_ratings':
        query += ' ORDER BY game.pos_ratings'
    
    query += ' ' + sort_order + ';'

    game_list = []
    game_ids = []

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, query_args)
        
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
            game_description = row[2]
            game_media = row[3]
            website = row[4]
            if game_id not in game_ids: 
                header_image = json.loads(game_media.replace("'", '"'))['header_image']
                if header_image == '':
                    header_image = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.simplystamps.com%2Fmedia%2Fcatalog%2Fproduct%2F5%2F8%2F5802-n-a-stock-stamp-hcb.png&f=1&nofb=1&ipt=4c91608ffabe756cef98c89e32321f03e9ae4c3ab4a92fb4b68453801fd7cf7e&ipo=images'
                game = {'id': str(game_id),
                        'title': game_title,
                        'description': game_description,
                        'header_image': header_image,
                        'website': website}
                game_ids.append(game_id)
                game_list.append(game)
            
        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(game_list)


@api.route('/games/specific/<game_id>') 
def get_a_specific_game(game_id):
    # Returns a dictionary of a particular game in our database, based on game_id

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


@api.route('/stats') 
def get_stats():
    # Returns a chart charted the requested data, as well as a name of the chart

    # Set up query, what is it being sorted by
    output = flask.request.args.get('output')
    if output == 'devs': 
        chart_type = 'pie'
        output_sql_value = 'developer.developer_name'
        chart_title = 'Developers of Games Released'
    elif output == 'dates':
        chart_type = 'bar'
        output_sql_value = 'game.release_date'
        chart_title = 'Histogram of Dates when Games were Released'
    elif output == 'ratings':
        chart_type = 'bar'
        output_sql_value = '(100.0 * game.pos_ratings / (game.pos_ratings + game.neg_ratings))'
        chart_title = 'Histogram of Game Ratings'
    else:
        chart_type = 'pie'
        output_sql_value = 'genre.genre_name'
        chart_title = 'Genres of Games Released'
    
    # Create query and finish building chart title
    result_query, query_args, result_chart_title = add_args_to_query(flask.request.args, True)

    query_sum_arg = f'SUM(CASE WHEN (1=1{result_query}) THEN 1 ELSE 0 END)'
    query = f'SELECT {output_sql_value}, {query_sum_arg} {queries.statistics_after_sum_statement} {output_sql_value} '
    if chart_type == 'pie':
        query += f'ORDER BY {query_sum_arg} DESC;'
        query_args = query_args + query_args
    else:
        query += f'ORDER BY {output_sql_value} DESC;'
    
    if len(result_chart_title) > 0:
        chart_title += result_chart_title[1:]

    #get results
    results = {}

    try:
        connection = get_connection()
        cursor = connection.cursor()
        print(query)
        print(query_args)
        cursor.execute(query, tuple(query_args))

        results['OBJECTIVE_TITLE'] = chart_title
        for row in cursor: 
            if output == 'ratings':
                results[float(row[0])] = row[1]
            else:
                results[row[0]] = row[1]
        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(results)


# This is a utility function that helps parse the GET parameters for endpoints /games and /stats
def add_args_to_query(args, get_genre_dev_name = False):
    query = ''
    query_args = []
    chart_title = ''

    if 'title' in args:
        game_title = str(args.get('title'))
        query_args.append(game_title)
        query += " AND game.title ILIKE CONCAT('%%', %s, '%%')"
        chart_title += f', with "{game_title}" in Game Title' 

    if 'min_age_above' in args: 
        min_age_above = str(args.get('min_age_above'))
        query_args.append(min_age_above)
        query += ' AND game.minimum_age >= %s'
        chart_title += f', Minimum Age Above {min_age_above}' 

    if 'min_age_below' in args: 
        min_age_below = str(args.get('min_age_below'))
        query_args.append(min_age_below)
        query += ' AND game.minimum_age <= %s'
        chart_title += f', Minimum Age Below {min_age_below}' 

    if 'start_date' in args: 
        start_date = str(args.get('start_date'))
        query_args.append(start_date)
        query += ' AND game.release_date >= %s'
        chart_title += f', Released After {start_date}' 

    if 'end_date' in args: 
        end_date = str(args.get('end_date'))
        query_args.append(end_date)
        query += ' AND game.release_date <= %s'
        chart_title += f', Released Before {end_date}' 

    if 'platforms' in args: 
        # "w, m, l"
        platforms = args.get('platforms').split(',')
        if 'w' in platforms: 
            query += ' AND game.windows_support = true'
            chart_title += ', with Windows Support' 
        if 'm' in platforms: 
            query += ' AND game.mac_support = true'
            chart_title += ', with Mac Support' 
        if 'l' in platforms: 
            query += ' AND game.linux_support = true'
            chart_title += ', with Linux Support' 

    if 'price_above' in args: 
        price_above = str(args.get('price_above'))
        query_args.append(price_above)
        query += ' AND game.price >= %s'
        chart_title += f', Costing Above ${price_above}' 

    if 'price_below' in args: 
        price_below = str(args.get('price_below'))
        query_args.append(price_below)
        query += ' AND game.price <= %s'
        chart_title += f', Costing Below ${price_below}' 

    if 'percent_pos_ratings_above' in args: 
        percent_pos_ratings_above = str(args.get('percent_pos_ratings_above'))
        query_args.append(percent_pos_ratings_above)
        query += ' AND (100.0 * game.pos_ratings / (game.pos_ratings + game.neg_ratings)) >= %s'
        chart_title += f', With at Least {percent_pos_ratings_above}% Positive Ratings' 

    if 'percent_pos_ratings_below' in args: 
        percent_pos_ratings_below = str(args.get('percent_pos_ratings_below'))
        query_args.append(percent_pos_ratings_below)
        query += ' AND (100.0 * game.pos_ratings / (game.pos_ratings + game.neg_ratings)) <= %s'
        chart_title += f', With at Most {percent_pos_ratings_below}% Positive Ratings' 

    if 'total_ratings_above' in args:
        total_ratings_above = str(args.get('total_ratings_above'))
        query_args.append(total_ratings_above)
        query += ' AND (game.pos_ratings + game.neg_ratings) >= %s'
        chart_title += f', With at Least {total_ratings_above} Ratings' 

    if 'total_ratings_below' in args:
        total_ratings_below = str(args.get('total_ratings_below'))
        query_args.append(total_ratings_below)
        query += ' AND (game.pos_ratings + game.neg_ratings) <= %s'
        chart_title += f', With at Most {total_ratings_below} Ratings' 

    if 'genre_id' in args: 
        genre_id = str(args.get('genre_id'))
        query_args.append(genre_id)
        query += ' AND genre.id = %s'
        
        if get_genre_dev_name:
            try:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(queries.get_genre_from_genre_id, (genre_id, ))
                for row in cursor:
                    genre_name = row[0]
            except Exception as e:
                print(e, file=sys.stderr)
            chart_title += f', in the Genre {genre_name}' 

    if 'developer_id' in args: 
        developer_id = str(args.get('developer_id'))
        query_args.append(developer_id)
        query += ' AND developer.id = %s'
        
        if get_genre_dev_name:
            try:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(queries.get_developer_from_developer_id, (developer_id, ))
                for row in cursor:
                    developer_name = row[0]
            except Exception as e:
                print(e, file=sys.stderr)
            chart_title += f', Developed by {developer_name}' 

    return query, query_args, chart_title