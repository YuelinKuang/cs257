'''
    api.py
    Lucie Wolf and Yuelin Kuang
    8 Nov 2022

    Web application project for CS257.
'''

import sys
import flask
import json
import config
import psycopg2

api = flask.Blueprint('api', __name__)

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)

@api.route('/games') 
def get_games():
    ''' Returns a list of all the authors in our database. See
        get_author_by_id below for description of the author
        resource representation.

        By default, the list is presented in alphabetical order
        by surname, then given_name. You may, however, use
        the GET parameter sort to request sorting by birth year.

            http://.../authors/?sort=birth_year

        Returns an empty list if there's any database failure.
    '''

    query = ''' SELECT game.title, game.release_date, 
                    game.english_support, game.windows_support, 
                    game.mac_support, game.linux_support, 
                    game.minimum_age, game.pos_ratings, 
                    game.neg_ratings, game.price, game.described, 
                    game.link, game.media, developer.developer_name, 
                    publisher.publisher_name, category.category_name,
                    genre.genre_name, game.media
                    FROM game, developer, publisher, category, genre, 
                    game_developer, game_category, game_genre, game_publisher
                    WHERE game.id = game_developer.game_id 
                    AND game.id = game_category.game_id
                    AND game.id = game_genre.game_id
                    AND game.id = game_publisher.game_id
                    ORDER BY game.title'''

            # indices: 
            #     0 game.title, 1 game.release_date, 
            #     2 game.english_support, 3 game.windows_support, 
            #     4 game.mac_support, 5 game.linux_support, 
            #     6 game.minimum_age, 7 game.pos_ratings, 
            #     8 game.neg_ratings, 9 game.price, 10 game.described, 
            #     11 game.link, 12 game.media, 13 developer.developer_name, 
            #     14 publisher.publisher_name, 15 category.category_name,
            #     16 genre.genre_name,

    # sort_argument = flask.request.args.get('sort_by')
    # if sort_argument == 'title_a':
    #     query += 'game.title'
    # else:
    #     query += 'game.title DESCENDING'

    game_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())

        current_game_title = 'NA'
        current_desc = 'NA'
        current_images = 'NA'
        current_date = ''
        current_age = 0
        current_eng = None
        current_win = None
        current_mac = None
        current_lin = None
        current_website = 'NA'

        current_developers = []
        current_publishers = []
        current_genres = []
        current_categories = []

        for row in cursor:
            if row[0] == current_game_title: 
                current_developers.append(row[13])
                current_publishers.append(row[14])
                current_categories.append(row[15])
                current_genres.append(row[16])

            else: 
                developers = ', '.join(set(current_developers))
                publishers = ', '.join(set(current_publishers))
                genres = ', '.join(set(current_genres))
                categories = ', '.join(set(current_categories))

                game = {'title':current_game_title,
                        'description':current_desc,
                        'links_to_images':current_images,
                        'developers':developers,
                        'publisher':publishers, 
                        'release_date': current_date, 
                        'minimum_age': current_age,
                        'english_support': current_eng,
                        'windows_support': current_win,
                        'mac_support': current_mac,
                        'linux_support': current_lin, 
                        'genres': genres, 
                        'categories': categories,
                        'website': current_website 
                        }
                game_list.append(game)

                current_game_title = row[0]
                current_desc = row[10]
                current_images = row[12]
                current_date = row[1]
                current_age = row[6]
                current_eng = row[2]
                current_win = row[3]
                current_mac = row[4]
                current_lin = row[5]
                current_website = row[11]
                current_developers = [row[13]]
                current_publishers = [row[14]]
                current_categories = [row[15]]
                current_genres = [row[16]]

        game_list.pop(0)

        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return flask.render_template('games_main.html', data=json.dumps(game_list))


