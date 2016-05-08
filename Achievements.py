import time
import json
from pymongo import *
from pprint import pprint

import requests

from decimal import *


steam_key = 'C100AD140B625C873DAB3CB5A5B076A8'
client = MongoClient("localhost", 27017)
coll_players = client.steam.players

# Selects player with open profiles, with at least one game
player_sample = coll_players.find({'visibility': 3,
                                   'achievements': {'$exists': False},
                                   'games': {'$gt': {}}})


# Goes through the profiles and look for achievements to upload
def upload_achievements(players, db, steamkey):
    # Errors, always errors that is due to connection issues or whatnot. While True allows for 60 seconds before retry
    while True:
        try:
            i = 1
            for p in players:
                # So that the variables can be used in further functions (if statements etc)
                global player_id
                player_id = p['_id']
                global player_achievements # ^^
                player_achievements = []
                j = 1
                print str(len(p['games'])) + ' games owned'
                played_games = []
                # Excluding games with 0 play time - almost every player has games he hasn't played
                for q in p['games']:
                    if q['playtime_forever'] > 0:
                        played_games.append(q)
                print str(played_games.__len__()) + ' games played'
                print player_id
                # And now to download achievements
                for games in played_games:
                    achievements = requests.get("http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=" + str(games["appid"]) + "&key="+ steam_key +"&steamid=" + str(player_id)).json()
                    if 'achievements' in achievements['playerstats']:
                        player_achievements.append([str(games["appid"]), achievements['playerstats']['achievements']])

                        db.update({'_id': player_id},
                                  {'achievements': player_achievements}, upsert=True)

            i = + 1
            if i % 10 == 0:
                print str(Decimal(i) / Decimal(player_sample.count())) * 100 + '%'

        except ValueError:
            print 'error, waiting 60 seconds'
            time.sleep(60)
    pass

upload_achievements(player_sample, coll_players, steam_key)