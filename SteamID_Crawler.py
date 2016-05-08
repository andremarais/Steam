import json
from pymongo import *
from pprint import pprint
from itertools import chain
import requests
import time

steam_key = 'C100AD140B625C873DAB3CB5A5B076A8'
client = MongoClient("localhost", 27017)
coll_players = client.steam.players


# Function to gather steam data.
def get_steam_data(steam_id, steamkey):
    steam_profile = {}
    global player_summary
    player_summary = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamkey + "&steamids=" + steam_id)
    # if empty result set, wait 60 seconds then try again. Seems like this happens very infrequently, but still...
    if len(player_summary.json()['response']['players']) == 0 or player_summary.status_code == 500:
        print 'error in getting profile, waiting 60 seconds then trying again'
        time.sleep(30)
        print '30 seconds'
        time.sleep(15)
        print '15 seconds'
        time.sleep(15)
        print 'trying again'
        player_summary = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamkey + "&steamids=" + steam_id)
        print player_summary

    player_summary = player_summary.json()

    # Check if profile is private or public. 1 indicates having a private account
    if player_summary['response']['players'][0]['communityvisibilitystate'] == 1:
        steam_profile['visibility'] = 1
        steam_profile['games'] = {}
        steam_profile['friends'] = {}
    else:
        # In the event that the profile is public, get owned games and friends list
        ownedgames = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + steamkey + "&steamid=" + steam_id + "&format=json").json()
        friend_list = requests.get("http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=" + steamkey + "&steamid=" + steam_id + "&relationship=friend").json()

        friends = []
        for f in friend_list['friendslist']['friends']:
            friends.append(f['steamid'])

        steam_profile['visibility'] = 3
        steam_profile['friends'] = friends
        # some players have 0 games....why do you have a steam account then, huh?
        if ownedgames['response']['game_count'] == 0:
            steam_profile['games'] = {}
        else:
            steam_profile['games'] = ownedgames['response']['games']

        pass
    steam_profile['steam_id'] = steam_id

    return steam_profile


# Function to upload the data to MongoDB
def update_steam_player(steam_profile, db):
    db.update({"_id": steam_profile["steam_id"]},
                {"$set": {"friends": steam_profile['friends'],
                 'games': steam_profile['games'], 'visibility': steam_profile['visibility']}}, upsert=True)


# Function to see who is already on the DB
def list_of_steam_ids(db):
    results = db.find({'visibility': {'$in': [1, 3]}})
    loaded_ids = []
    friends_list = []

    for r in results:
        friends_list.append(r['friends'])
        loaded_ids.append(r['_id'])
    # Unlists the arrays into a single array
    friends_list = sorted(set(list(chain.from_iterable(friends_list))))

    return friends_list, loaded_ids


# Finally, the function to download all the API data and upload it to MongoDB
def find_them_all(seed, jumps, db):
    update_steam_player(get_steam_data(seed, steam_key), db)
    # Errors, always errors that is due to connection issues or whatnot. While True allows for 60 seconds before retry
    while True:
        try:
            i = 1

            while i <= jumps:
                new_ids, existing_ids = list_of_steam_ids(db)
                print len(new_ids)
                k = 1
                for l in new_ids:
                    if l not in existing_ids:
                        print l
                        update_steam_player(get_steam_data(l, steam_key), db)
                        k += 1
                i += 1

        except ValueError:
            print 'error, waiting 60 seconds'
            time.sleep(60)

find_them_all('76561197960877310', 4, coll_players)
