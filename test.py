__author__ = 'wzhang'


from dota2api import gatherdata
from dota2api import dbmapper
import dota2api

key = "057E177A0B56008B34AD00A9361AE46F"
account_id = 209231489
# gatherdata.collect_matches(key)
# stats = dbmapper.get_heroes_statistics()
# print(stats)
api = dota2api.Dota2api(key)
stats = api.get_player_statistics(account_id)
print(stats)

# gatherdata.collect_matches(key)