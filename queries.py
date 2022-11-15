get_genres='''SELECT genre.id, genre.genre_name
               FROM genre
               ORDER BY genre.genre_name;'''

get_developers='''SELECT developer.id, developer.developer_name
               FROM developer
               ORDER BY developer.developer_name;'''

all_game_information_search='''
SELECT game.id, game.title, game.described, game.media, game.website

FROM game, developer, publisher, category, genre, 
game_developer, game_category, game_genre, game_publisher

WHERE game.id = game_developer.game_id 
AND game_developer.developer_id = developer.id
AND game.id = game_category.game_id
AND game_category.category_id = category.id
AND game.id = game_genre.game_id
AND game_genre.genre_id = genre.id
AND game.id = game_publisher.game_id
AND game_publisher.publisher_id = publisher.id
'''

specific_game_info='''
SELECT game.title, game.release_date, 
game.english_support, game.windows_support, 
game.mac_support, game.linux_support, 
game.minimum_age, game.pos_ratings, 
game.neg_ratings, game.price, game.described, 
game.website, game.media, developer.developer_name, 
publisher.publisher_name, category.category_name,
genre.genre_name

FROM game, developer, publisher, category, genre, 
game_developer, game_category, game_genre, game_publisher

WHERE game.id = game_developer.game_id 
AND game_developer.developer_id = developer.id
AND game.id = game_category.game_id
AND game_category.category_id = category.id
AND game.id = game_genre.game_id
AND game_genre.genre_id = genre.id
AND game.id = game_publisher.game_id
AND game_publisher.publisher_id = publisher.id
AND game.id = %s
'''

statistics_after_sum_statement='''
FROM game, developer, publisher, category, genre, 
game_developer, game_category, game_genre, game_publisher

WHERE game.id = game_developer.game_id 
AND game_developer.developer_id = developer.id
AND game.id = game_category.game_id
AND game_category.category_id = category.id
AND game.id = game_genre.game_id
AND game_genre.genre_id = genre.id
AND game.id = game_publisher.game_id
AND game_publisher.publisher_id = publisher.id
GROUP BY'''

get_genre_from_genre_id = '''
SELECT genre.genre_name
FROM genre
WHERE genre.id = %s;
'''

get_developer_from_developer_id = '''
SELECT developer.developer_name
FROM developer
WHERE developer.id = %s;
'''