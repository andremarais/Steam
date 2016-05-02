import urllib2
import json
from pymongo import *
from pprint import pprint
from itertools import chain

steam_ids = ['76561198021980285', '76561197998281789', '76561198015864105', '76561198018309333', '76561198006229085']
steam_key = 'C100AD140B625C873DAB3CB5A5B076A8'
# Louis: 76561198021980285
# Myne: 76561197998281789
# Kazi: 76561198015864105
# Bibo (blessed is he): 76561198018309333
# Riaan: 76561198006229085

client = MongoClient("localhost", 27017)
coll_players = client.steam.players


def get_steam_data(steam_id, steamkey):
    steam_profile = {}

    player_summary = json.loads(urllib2.urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamkey + "&steamids=" + steam_id).read())
    # pprint(player_summary)
    ownedgames = json.loads(urllib2.urlopen("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + steamkey + "&steamid=" + steam_id + "&format=json").read())

    if len(ownedgames['response']) < 2:
        # Private or no owned games (ignores free games)
        steam_profile['visibility'] = 2
        steam_profile['games'] = {}
        steam_profile['friends'] = {}



    else:
        steam_profile['games'] = ownedgames['response']['games']
        # In the event that the player's profile is public, get friends list and set visibility to 3 (as in API)
        if player_summary['response']['players'][0]['communityvisibilitystate'] == 3:
            friend_list = urllib2.urlopen("http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=" + steamkey + "&steamid=" + steam_id + "&relationship=friend").read()

            friend_list = json.loads(friend_list)
            friends = []

            for f in friend_list['friendslist']['friends']:
                friends.append(f['steamid'])

            steam_profile['visibility'] = 3
            steam_profile['friends'] = friends

            pass

        # And then when it's private, empty friends list and visibility set to 1 (as in API)
        else:
            steam_profile['visibility'] = 1
            steam_profile['friends'] = {}
            steam_profile['games'] = ownedgames['response']['games']
            pass

    steam_profile['steam_id'] = steam_id


    return steam_profile


def update_steam_player(steam_profile, db):
    db.update({"_id" : steam_profile["steam_id"]},
                {"$set" : {"friends": steam_profile['friends'],
                 'games': steam_profile['games'],
                           'visibility': steam_profile['visibility']}}, upsert=True)


def list_of_steam_ids(db):
    results = db.find({'visibility': {'$in': [1, 3]}})
    loaded_ids = []
    friends_list = []

    for r in results:
        friends_list.append(r['friends'])
        loaded_ids.append(r['_id'])

    # converts to single array and removes duplicates
    friends_list = sorted(set(list(chain.from_iterable(friends_list))))
    for f in friends_list:
        if f in loaded_ids:
            friends_list.remove(f)

    return friends_list


def find_them_all(seed, jumps, db):
    # downloads seed profile and uploads to MongoDB
    update_steam_player(get_steam_data(seed, steam_key), db)
    print 'uploaded seed profile'
    i = 1

    while i <= jumps:
        new_ids = list_of_steam_ids(db)
        print len(new_ids)

        for l in new_ids:
            print l
            update_steam_player(get_steam_data(l, steam_key), db)
            print 'uploaded', l
        i += 1

find_them_all('76561197960989628', 1, coll_players)

# print get_steam_data('76561197999098582', steam_key)