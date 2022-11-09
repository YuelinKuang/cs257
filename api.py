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
import queries

api = flask.Blueprint('api', __name__)

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)

@api.route('/games/') 
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

    query = queries.games
    

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

        game = {'title':'',
                'description':'',
                'links_to_images':'',
                'developers':[],
                'publishers':[], 
                'release_date': '', 
                'minimum_age': 0,
                'english_support': False,
                'windows_support': False,
                'mac_support': False,
                'linux_support': False, 
                'genres': [], 
                'categories': [],
                'website': '' 
                }

        for row in cursor:
            if row[0] == game['title']: 
                game['developers'].append(row[13])
                game['publishers'].append(row[14])
                game['categories'].append(row[15])
                game['genres'].append(row[16])

            else: 
                game['developers'] = ', '.join(set(game['developers']))
                game['publishers'] = ', '.join(set(game['publishers']))
                game['genres'] = ', '.join(set(game['genres']))
                game['categories'] = ', '.join(set(game['categories']))

                game_list.append(game)

                images = json.loads(row[12].replace("'", '"'))
                if images['header_image'] == '':
                    images['header_image'] = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.simplystamps.com%2Fmedia%2Fcatalog%2Fproduct%2F5%2F8%2F5802-n-a-stock-stamp-hcb.png&f=1&nofb=1&ipt=4c91608ffabe756cef98c89e32321f03e9ae4c3ab4a92fb4b68453801fd7cf7e&ipo=images'

                game = {'title':row[0],
                        'description':row[10],
                        'links_to_images':images,
                        'developers':[row[13]],
                        'publishers':[row[14]], 
                        'release_date': str(row[1]), 
                        'minimum_age': row[6],
                        'english_support': row[2],
                        'windows_support': row[3],
                        'mac_support': row[4],
                        'linux_support': row[5], 
                        'genres': [row[16]], 
                        'categories': [row[15]],
                        'website': row[11] 
                        }

        game_list.append(game)
        game_list.pop(0)

        cursor.close()
        connection.close()


    except Exception as e:
        print(e, file=sys.stderr)

    return flask.render_template('games_main.html', data=game_list)