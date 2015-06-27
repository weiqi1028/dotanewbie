__author__ = 'wzhang'

from dota2api.src import weburl
from urllib.parse import urlencode
from urllib.request import urlopen
import json


class Dota2api:
    """the Dota2 web API wrapper class

    api_key:
        the API key issued from steam

    """

    def __init__(self, key):
        self.api_key = key

    def get_match_history_by_account_id(self, account_id, **kwargs):
        """get match history giving the player's account id

        :param account_id: the player's steam id
        :param kwargs: additional API parameters
        :return: the match history
        """

        if 'account_id' not in kwargs:
            kwargs['account_id'] = account_id
        url = self.__build_url(weburl.GET_MATCH_HISTORY, **kwargs)
        print("requesting for: " + url)
        try:
            response = urlopen(url)
            json_result = json.loads(response.read().decode('utf-8'))
            result = json_result['result']
            return result
        except Exception:
            raise Exception

    def get_match_history(self, **kwargs):
        """get match history giving API parameters

        :param kwargs: additional API parameters
        :return: the match history
        """

        url = self.__build_url(weburl.GET_MATCH_HISTORY, **kwargs)
        print("requesting for: " + url)
        try:
            response = urlopen(url)
            json_result = json.loads(response.read().decode('utf-8'))
            result = json_result['result']
            return result
        except Exception:
            raise Exception

    def get_all_match_history(self, account_id):
        """get all the match history giving a player's account id, 500 results maximum

        :param account_id: the player's steam id
        :return: all the match history of the player, 500 maximum
        """

        stats = []
        result = self.get_match_history(account_id=account_id)
        num_results = result['num_results']
        results_remaining = result['results_remaining']

        while num_results > 0:
            matches = result['matches']
            for match in matches:
                stats.append(match)
            if results_remaining == 0:
                break
            last_record = matches[-1]
            last_match_id = last_record['match_id'] - 1
            result = self.get_match_history(account_id=account_id, start_at_match_id=last_match_id)
            num_results = result['num_results']
            results_remaining = result['results_remaining']
        return stats

    def get_match_history_by_sequence_num(self, **kwargs):
        """get match history by sequence number

        :param kwargs: additional API parameters
        :return: the match history
        """

        url = self.__build_url(weburl.GET_MATCH_HISTORY_BY_SEQUENCE_NUM, **kwargs)
        print("requesting for: " + url)
        try:
            response = urlopen(url)
            json_result = json.loads(response.read().decode('utf-8'))
            result = json_result['result']['matches']
            return result
        except Exception:
            raise Exception

    def get_match_details(self, match_id, **kwargs):
        """get match details by match id

        :param match_id: the match id
        :param kwargs: additional API parameters
        :return: the match details
        """

        if 'match_id' not in kwargs:
            kwargs['match_id'] = match_id
        url = self.__build_url(weburl.GET_MATCH_DETAILS, **kwargs)
        print("requesting for: " + url)
        try:
            response = urlopen(url)
            json_result = json.loads(response.read().decode('utf-8'))
            result = json_result['result']
            return result
        except Exception:
            raise Exception

    def get_game_items(self):
        """get items from the Valve server

        :return: the items dictionary
        """

        url = self.__build_url(weburl.GET_GAME_ITEMS)
        print("requesting for: " + url)
        response = urlopen(url)
        json_result = json.loads(response.read().decode('utf-8'))
        items = json_result['result']['items']
        return items

    def get_heroes(self):
        """get heroes from the Valve server

        :return: the heroes dictionary
        """

        url = self.__build_url(weburl.GET_HEROES)
        print("requesting for: " + url)
        response = urlopen(url)
        json_result = json.loads(response.read().decode('utf-8'))
        heroes = json_result['result']['heroes']
        return heroes

    def get_player_statistics(self, account_id):
        """get the players statistics by steam id

        :param account_id: the steam id
        :return: the players statistics
        """

        stats = {}
        total_match = {}
        won_match = {}
        win_rate = {}
        kills = {}
        deaths = {}
        assists = {}
        kda = {}
        # hero is is from 1 to 112
        for i in range(112):
            total_match[i + 1] = 0
            won_match[i + 1] = 0
            win_rate[i + 1] = 0
            kills[i + 1] = 0
            deaths[i + 1] = 0
            assists[i + 1] = 0
            kda[i + 1] = 0
        matches = self.get_all_match_history(account_id)
        print('matches played ' + str(len(matches)))
        for match in matches:
            players = match['players']
            for player in players:
                if player['account_id'] == account_id:
                    hero_id = player['hero_id']
                    total_match[hero_id] += 1
                    match_id = match['match_id']
                    match_details = self.get_match_details(match_id)
                    radiant_win = match_details['radiant_win']
                    player_details = match_details['players']
                    for player_detail in player_details:
                        if player_detail['account_id'] == account_id:
                            player_slot = player_detail['player_slot']
                            radiant = False
                            if player_slot & 128 == 0:
                                radiant = True
                            if (radiant and radiant_win) or (not radiant and not radiant_win):
                                won_match[hero_id] += 1
                            kills[hero_id] += player_detail['kills']
                            deaths[hero_id] += player_detail['deaths']
                            assists[hero_id] += player_detail['assists']
                            break
                    break
        for i in range(112):
            if total_match[i + 1] != 0:
                win_rate[i + 1] = won_match[i + 1] / total_match[i + 1]
        for i in range(112):
            if total_match[i + 1] != 0:
                if deaths[i + 1] == 0:
                    kda[i + 1] = kills[i + 1] + assists[i + 1]
                else:
                    kda[i + 1] = (kills[i + 1] + assists[i + 1]) / deaths[i + 1]
        stats['matches_played'] = total_match
        stats['matches_won'] = won_match
        stats['win_rate'] = win_rate
        stats['kda'] = kda
        return stats

    def __build_url(self, api_call, **kwargs):
        """build the url that the http GET request will send to

        :param api_call: the API url
        :param kwargs: additional API parameters
        :return:
        """

        kwargs['key'] = self.api_key
        query = urlencode(kwargs)
        query = '{0}?{1}'.format(api_call, query)
        return query
