__author__ = 'wzhang'

# the module to retrieve match details from the Valve server and store them into the local database

import time
import dota2api
from dota2api import dbmapper


def __retrieve_subroutine(start_from_match, to_match, key):
    """get matches details in a range

    :param start_from_match: the match id to start from
    :param to_match: the match id that ends up with
    :return: null
    """

    start_time = time.time()

    last_retrieved_id = start_from_match
    api = dota2api.Dota2api(key)

    # write the retrieved match ids into a log file
    file = open('matches.log', 'a')
    while True:
        # matches are the first 100 results from last_retrieved_id, descending
        while True:
            try:
                matches = api.get_match_history(start_at_match_id=last_retrieved_id, min_players=10, game_mode=1,
                                                matches_requested=100)['matches']
            except Exception:
                print('exception occurred, retry get_match_history after 5 seconds...')
                time.sleep(5)
                continue
            break

        match_ids = []
        for match in matches:
            match_ids.append(match['match_id'])

        print("retrieving matches from " + str(last_retrieved_id))
        print("the next 100 matches: ")

        for match_id in match_ids:
            if match_id == to_match:
                return

            print("processing match " + str(match_id))
            while True:
                try:
                    match_details = api.get_match_details(match_id)
                except Exception:
                    print('exception occurred, retry get_match_details after 5 seconds...')
                    time.sleep(5)
                    continue
                break

            # do not record the game that is not finished normally
            players = match_details['players']
            finished = True
            for player in players:
                if player['leaver_status'] != 0:
                    finished = False
                    print("match " + str(match_id) + " is not finished normally")
                    break

            if finished:
                print(match_details)
                print('Storing match ' + str(match_id) + ' record to the database...')
                dbmapper.insert_match_into_database(match_details)

                file.write(str(match_id) + '\n')

        last_retrieved_id = match_ids[-1]

    end_time = time.time()
    time_elapsed = end_time - start_time
    print("time elapsed: " + str(time_elapsed))
    file.close()


def collect_matches(key):
    """collect matches details from the Valve server, it will collect the matches from the time it starts

    :param key: the API key
    :return: null
    """

    api = dota2api.Dota2api(key)
    initial_result = api.get_match_history(matches_requested=1, min_players=10, game_mode=1)
    initial_match = initial_result['matches'][0]
    most_recent_retrieved_id = initial_match['match_id']
    # Sleep for 5 minutes, just ugly setup the following while loop
    print('initial setup, waiting for 5 minutes...\n')
    time.sleep(300)
    while True:
        # request for the latest match recorded on the Valve server
        while True:
            try:
                latest_result = api.get_match_history(matches_requested=1, min_players=10, game_mode=1)
            except Exception:
                print('exception occurred, retry get_match_details after 5 seconds...')
                time.sleep(5)
                continue
            break
        latest_match = latest_result['matches'][0]
        latest_match_id = latest_match['match_id']
        print('latest match id: ' + str(latest_match_id))

        if most_recent_retrieved_id == latest_match_id:
            print('No new matches recorded on the Valve server, waiting for 5 minutes...')
            time.sleep(300)
        else:
            print('Retrieving match from ' + str(latest_match_id) + ' to ' + str(most_recent_retrieved_id) +
                  '(excluding), descending...')
        __retrieve_subroutine(latest_match_id, most_recent_retrieved_id)
        most_recent_retrieved_id = latest_match_id
