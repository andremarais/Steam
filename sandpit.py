import requests
from pprint import pprint
from lxml.html import fromstring
from pymongo import *
import json
import array

steamkey = 'C100AD140B625C873DAB3CB5A5B076A8'
def fok(steamkey, steam_id):
    player_summary = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamkey + "&steamids=" + steam_id).json()
    ownedgames = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + steamkey + "&steamid=" + steam_id + "&format=json").json()
    print "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamkey + "&steamids=" + steam_id
    return player_summary, ownedgames


# pprint(fok(steamkey, '76561198015864105')[1]['response'])
# print fok(steamkey, '76561197960557003')[1]
client = MongoClient("localhost", 27017)
#
coll = client.steam.players
# d = dict((k, v) for k, v in d.items() if v >= 10)

all_games = coll.count()
print all_games


"""
>>> d = dict(a=1, b=10, c=30, d=2)
>>> d
{'a': 1, 'c': 30, 'b': 10, 'd': 2}
>>> d = dict((k, v) for k, v in d.items() if v >= 10)
>>> d
{'c': 30, 'b': 10}
"""

