import urllib2
import json
from pymongo import *
from pprint import pprint

def test_shit(steam_id, steamkey):
    player_summary = urllib2.urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamkey + "&steamids=" + steam_id).read()
    ownedgames = urllib2.urlopen("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + steamkey + "&steamid=" + steam_id + "&format=json").read()
    return json.loads(player_summary), json.loads(ownedgames)

super_private = '76561197964624206'
louis = '76561198021980285'
myne = '76561197998281789'

#
# print 'super private'
# # pprint(test_shit(super_private, 'C100AD140B625C873DAB3CB5A5B076A8')['response']['players'][0])
# print '-----'
# print 'Louis'
# # pprint(test_shit(louis, 'C100AD140B625C873DAB3CB5A5B076A8')['response']['players'][0])
# print '-----'
# print 'Mine'
# pprint(test_shit(myne, 'C100AD140B625C873DAB3CB5A5B076A8')['response']['players'][0])

# pprint(test_shit(super_private, 'C100AD140B625C873DAB3CB5A5B076A8')[1]['response'])

print test_shit('76561197960989628', 'C100AD140B625C873DAB3CB5A5B076A8')[1]['response']