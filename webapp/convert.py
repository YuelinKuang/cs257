'''
Lucie Wolf and Yuelin Kuang
'''

import csv
import json


with open('steam.csv') as game_o,\
        open('steam_media_data.csv') as media_o,\
        open('steam_description_data.csv') as desc_o,\
        open('steam_support_info.csv') as support_o,\
        open('game.csv', 'w') as game_n,\
        open('developer.csv', 'w') as developer_n,\
        open('publisher.csv', 'w') as publisher_n,\
        open('category.csv', 'w') as category_n,\
        open('genre.csv', 'w') as genre_n,\
        open('game_developer.csv', 'w') as game_developer_n,\
        open('game_publisher.csv', 'w') as game_publisher_n,\
        open('game_category.csv', 'w') as game_category_n,\
        open('game_genre.csv', 'w') as game_genre_n:
        #o stands for original, n stands for new in variable names

    game_reader = csv.reader(game_o)
    media_reader = csv.reader(media_o)
    desc_reader = csv.reader(desc_o)
    support_reader = csv.reader(support_o)

    game_writer = csv.writer(game_n)
    developer_writer = csv.writer(developer_n)
    publisher_writer = csv.writer(publisher_n)
    category_writer = csv.writer(category_n)
    genre_writer = csv.writer(genre_n)
    game_developer_writer = csv.writer(game_developer_n)
    game_publisher_writer = csv.writer(game_publisher_n)
    game_category_writer = csv.writer(game_category_n)
    game_genre_writer = csv.writer(game_genre_n)

    next(game_reader) # eat up and ignore the heading row of the data file
    next(media_reader)
    next(desc_reader)
    next(support_reader)


    media = {}

    for media_row in media_reader:
        game_id = int(media_row[0])

        media_instance = {'header_image':media_row[1]}
        screenshots = media_row[2].replace("'", '"')
        media_instance['background'] = media_row[3]

        if screenshots:
            screenshots = json.loads(screenshots)
            for i in range(len(screenshots)): #parses screenshot data
                screenshots[i] = screenshots[i]['path_full'] 
        
        media_instance['screenshots'] = screenshots
        media[game_id] = media_instance



    desc = {}

    for desc_row in desc_reader:
        game_id = int(desc_row[0])
        desc_instance = desc_row[3]

        desc[game_id] = desc_instance


    link = {}
    
    for support_row in support_reader:
        game_id = int(support_row[0])
        link_instance = support_row[1]

        if not link_instance:
            link_instance = support_row[2]

            if not link_instance:
                link_instance = 'N/A'

        link[game_id] = link_instance
    

    all_developers = {}
    all_publishers = {}
    all_categories = {}
    all_genres = {}

    def add_list(game_id, small_dict, big_dict, item_writer, game_item_writer):
        for item in small_dict:
            if item in big_dict:
                item_id = big_dict[item]
            
            else:
                item_id = len(big_dict)
                big_dict[item] = item_id
                item_writer.writerow([item_id, item])

            game_item_writer.writerow([game_id, item_id])


    for game_row in game_reader:
        game_id = int(game_row[0])
        title = game_row[1]
        date = game_row[2]
        english_support = bool(game_row[3])
        developers = game_row[4].split(';')
        publishers = game_row[5].split(';')
        platforms = game_row[6].split(';')
        min_age = int(game_row[7])
        categories = game_row[8].split(';')
        genres = game_row[9].split(';')
        pos_ratings = int(game_row[12])
        neg_ratings = int(game_row[13])
        price = float(game_row[17])

        windows_support = 'windows' in platforms
        mac_support = 'mac' in platforms
        linux_support = 'linux' in platforms

        if game_id not in desc:
            desc[game_id] = 'N/A'
        
        if game_id not in link:
            link[game_id] = 'N/A'

        if game_id not in media:
            media[game_id] = {}
            media[game_id]['header_image'] = ''
            media[game_id]['screenshots'] = ''
            media[game_id]['background'] = ''
        
        game_writer.writerow([game_id, title, date, english_support, windows_support, mac_support, linux_support, \
                            min_age, pos_ratings, neg_ratings, price, desc[game_id], link[game_id], media[game_id]])
    
        add_list(game_id, developers, all_developers, developer_writer, game_developer_writer)
        add_list(game_id, publishers, all_publishers, publisher_writer, game_publisher_writer)
        add_list(game_id, categories, all_categories, category_writer, game_category_writer)
        add_list(game_id, genres, all_genres, genre_writer, game_genre_writer)
        
        