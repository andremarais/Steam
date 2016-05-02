import urllib2
import json
from pymongo import *
from pprint import pprint
import urllib, urllib2
import requests

steam_key = 'C100AD140B625C873DAB3CB5A5B076A8'

client = MongoClient("localhost", 27017)
coll_players = client.steam.players

players = coll_players.find().limit(1)
#
# for p in players:
#     player_id = p['_id']
#     for games in p['games']:
#         print games['appid']
#         print player_id
#         achievements = urllib2.urlopen("http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=" + str(games["appid"]) + "&key="+ steam_key +"&steamid=" + str(player_id)).read()
#         # print achievements
#         pass
#     # print "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=" + games["appid"] + "&key="+ steam_key +"&steamid=" + player_id
#
#
# print "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=" + str(320) + "&key="+ steam_key +"&steamid=" + str(76561197998281789)

a = requests.get("http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=" + str(220) + "&key="+ steam_key +"&steamid=" + str(76561197998281789))


# response = urllib2.urlopen(a)
#
# results = requests.get("http://www.bing.com/search",
#               params={'q': query, 'first': page},
#               headers={'User-Agent': user_agent})

# b = requests.get("http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=" + str(320) + "&key="+ steam_key +"&steamid=" + str(76561197998281789))
print a.json()

