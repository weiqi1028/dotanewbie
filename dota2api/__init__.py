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

        stats = {'matches': []}
        result = self.get_match_history(account_id)
        results_remaining = result['results_remaining']
        num_matches = 0

        while results_remaining > 0:
            matches = result['matches']
            for match in matches:
                stats['matches'].append(match)
            num_matches += result['num_results']
            last_record = matches[-1]
            last_match_id = last_record['match_id']
            result = self.get_match_history(account_id, start_at_match_id=last_match_id)
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
