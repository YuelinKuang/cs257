SELECT DISTINCT game.title, game.release_date, 
game.english_support, game.windows_support, 
game.mac_support, game.linux_support, 
game.minimum_age, game.pos_ratings, 
game.neg_ratings, game.price, game.described, 
game.link, game.media, developer.developer_name, 
publisher.publisher_name, category.category_name,
genre.genre_name
FROM game, developer, publisher, category, genre, 
game_developer, game_category, game_genre, game_publisher
WHERE game.id = game_developer.game_id 
AND game.id = game_category.game_id
AND game.id = game_genre.game_id
AND game.id = game_publisher.game_id