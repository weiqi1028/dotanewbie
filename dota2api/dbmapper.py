__author__ = 'wzhang'

import mysql.connector
import dota2api


def insert_items_into_database(key):
    """get items information from the Valve server and store it into the local database

    :param key: the API key
    :return: null
    """

    api = dota2api.Dota2api(key)
    items = api.get_game_items()

    cnx = mysql.connector.connect(user='root', password='871028',
                                  host='127.0.0.1', database='dota2')
    cursor = cnx.cursor()

    for item in items:
        item_id = item['id']
        name = item['name']
        insert_items = 'INSERT INTO items (itemId, itemName) VALUES (%s, %s)'
        data_items = (item_id, name)
        cursor.execute(insert_items, data_items)

    cnx.commit()
    cursor.close()
    cnx.close()
    print('Insert items into database successfully.')


def insert_heroes_into_database(key):
    """get heroes information from the Valve server and store it into the local database

    :param key: the API key
    :return: null
    """

    api = dota2api.Dota2api(key)
    heroes = api.get_heroes()

    cnx = mysql.connector.connect(user='root', password='871028',
                                  host='127.0.0.1', database='dota2')
    cursor = cnx.cursor()

    for hero in heroes:
        hero_id = hero['id']
        name = hero['name']
        insert_heroes = 'INSERT INTO heroes (heroId, heroName) VALUES (%s, %s)'
        data_heroes = (hero_id, name)
        cursor.execute(insert_heroes, data_heroes)

    cnx.commit()
    cursor.close()
    cnx.close()
    print('Insert heroes into database successfully.')


def get_items_from_database():
    """get items dictionary from the local database

    :return: the dictionary contains items ids and item names. e.g. {1: 'blink_dagger'}
    """

    cnx = mysql.connector.connect(user='root', password='871028',
                                  host='127.0.0.1', database='dota2')
    cursor = cnx.cursor()
    query = 'SELECT * FROM items'
    cursor.execute(query)
    items = {}

    for (itemId, itemName) in cursor:
        items[itemId] = itemName

    return items


def get_heroes_from_database():
    """get heroes dictionary from the local database

    :return: the dictionary contains heroes ids and hero names. e.g. {1: 'tinker'}
    """

    cnx = mysql.connector.connect(user='root', password='871028',
                                  host='127.0.0.1', database='dota2')
    cursor = cnx.cursor()
    query = 'SELECT * FROM heroes'
    cursor.execute(query)
    heroes = {}

    for (heroId, heroName) in cursor:
        heroes[heroId] = heroName

    return heroes


def insert_match_into_database(match):
    """insert the match details into the local database

    :param match: the match details
    :return: null
    """

    radiant_win = match['radiant_win']
    duration = match['duration']
    start_time = match['start_time']
    match_id = match['match_id']
    match_seq_num = match['match_seq_num']
    tower_status_radiant = match['tower_status_radiant']
    tower_status_dire = match['tower_status_radiant']
    barracks_status_radiant = match['barracks_status_radiant']
    barracks_status_dire = match['barracks_status_dire']
    cluster = match['cluster']
    first_blood_time = match['first_blood_time']
    lobby_type = match['lobby_type']
    game_mode = match['game_mode']

    players = match['players']

    # connect to database
    cnx = mysql.connector.connect(user='root', password='871028',
                                  host='127.0.0.1', database='dota2')
    cursor = cnx.cursor()

    # insert into table matches
    insert_into_matches = 'INSERT INTO matches (matchId, duration, startTime, matchSeqNum, towerStatusRadiant, towerStatusDire,' \
                          'barracksStatusRadiant, barracksStatusDire, cluster, firstBloodTime, lobbyType, gameMode,' \
                          'player1Id, player2Id, player3Id, player4Id, player5Id, player6Id, player7Id, player8Id, player9Id,' \
                          'player10Id)' \
                          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,' \
                          '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    insert_into_matches_data = (match_id, duration, start_time, match_seq_num, tower_status_radiant, tower_status_dire,
                                barracks_status_radiant, barracks_status_dire, cluster, first_blood_time, lobby_type,
                                game_mode, __validate_player_id(players[0]['account_id']),
                                __validate_player_id(players[1]['account_id']),
                                __validate_player_id(players[2]['account_id']),
                                __validate_player_id(players[3]['account_id']),
                                __validate_player_id(players[4]['account_id']),
                                __validate_player_id(players[5]['account_id']),
                                __validate_player_id(players[6]['account_id']),
                                __validate_player_id(players[7]['account_id']),
                                __validate_player_id(players[8]['account_id']),
                                __validate_player_id(players[9]['account_id']))
    cursor.execute(insert_into_matches, insert_into_matches_data)

    for player in players:
        hero_id = player['hero_id']
        item_1 = player['item_0']
        item_2 = player['item_1']
        item_3 = player['item_2']
        item_4 = player['item_3']
        item_5 = player['item_4']
        item_6 = player['item_5']
        radiant = 0
        player_slot = player['player_slot']
        if player_slot & 128 == 0:
            radiant = 1
        win = 0
        if (radiant == 1 and radiant_win) or (radiant == 0 and not radiant_win):
            win = 1

        # insert into table hero_item_ties
        insert_into_hero_item_ties = 'INSERT INTO hero_item_ties (heroId, matchId, item1Id, item2Id, item3Id,' \
                                     'item4Id, item5Id, item6Id, win)' \
                                     'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        insert_into_hero_item_ties_data = (hero_id, match_id, item_1, item_2, item_3, item_4, item_5, item_6, win)
        cursor.execute(insert_into_hero_item_ties, insert_into_hero_item_ties_data)

        if player['account_id'] == 4294967295:
            continue

        # insert into table players_match_ties
        insert_into_players_match_ties = 'INSERT INTO player_match_ties (playerId, matchId, playerSlot, radiant, win,' \
                                         'heroId, kills, deaths, assists, leaverStatus, gold, lastHits, denies, gpm, xpm,' \
                                         'goldSpent, heroDamage, towerDamage, heroHealing, heroLevel)' \
                                         'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,' \
                                         '%s, %s)'
        player_id = player['account_id']
        kills = player['kills']
        deaths = player['deaths']
        assists = player['assists']
        leaver_status = player['leaver_status']
        gold = player['gold']
        last_hits = player['last_hits']
        denies = player['denies']
        gpm = player['gold_per_min']
        xpm = player['xp_per_min']
        gold_spent = player['gold_spent']
        hero_damage = player['hero_damage']
        tower_damage = player['tower_damage']
        hero_healing = player['hero_healing']
        hero_level = player['level']
        insert_into_players_match_ties_data = (player_id, match_id, player_slot, radiant, win, hero_id, kills, deaths,
                                               assists, leaver_status, gold, last_hits, denies, gpm, xpm, gold_spent,
                                               hero_damage, tower_damage, hero_healing, hero_level)
        cursor.execute(insert_into_players_match_ties, insert_into_players_match_ties_data)

    cnx.commit()
    cursor.close()
    cnx.close()


def delete_all_data_from_database():
    """delete all the data from the local database (use this carefully!)

    :return: null
    """

    cnx = mysql.connector.connect(user='root', password='871028',
                                  host='127.0.0.1', database='dota2')
    cursor = cnx.cursor()

    query = 'DELETE from hero_item_ties'
    cursor.execute(query)
    query = 'DELETE from player_match_ties'
    cursor.execute(query)
    query = 'DELETE from matches'
    cursor.execute(query)

    cnx.commit()
    cursor.close()
    cnx.close()


def __validate_player_id(player_id):
    """validate the player id

    :param player_id: the player's id
    :return: -1 if player's profile is set to private(4294967295), returns the player's id otherwise
    """

    if player_id == 4294967295:
        return -1
    return player_id
