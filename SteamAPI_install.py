import urllib2
# import pprint
# import xml.parsers
import json

steamID = '76561197998281789'
steamKey = 'C100AD140B625C873DAB3CB5A5B076A8'
AppID = "218620"


# PlayerSummary = urllib2.urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamKey + "&steamids=" + steamID).read()
# OwnedGames = urllib2.urlopen("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + steamKey + "&steamid=" + steamID + "&format=json").read()
# GamesScheme = urllib2.urlopen("http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key=" + steamKey + "&appid=" + AppID).read()
# GameAchievements = urllib2.urlopen("http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid=" + AppID + "&format=json").read()
# GameStats = urllib2.urlopen("http://api.steampowered.com/ISteamUserStats/GetGlobalStatsForGame/v0001/?format=json&appid=" + AppID + "&count=1&name").read()
FriendsList = urllib2.urlopen("http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=" + steamKey + "&steamid=" + steamID + "&relationship=friend").read()
# PlayerAchievements = urllib2.urlopen("http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=440&key=" + steamKey + "&steamid=" + steamID).read()
# PlayerStats = urllib2.urlopen("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=440&key=" + steamKey + "&steamid="+ steamID).read()



# print 'PlayerSummary'
# print PlayerSummary
# print ("---------------")
# print 'OwnedGames'
# print OwnedGames
# print ("---------------")
# print 'GamesScheme'
# print GamesScheme
# print ("---------------")
# print 'GameAchievements'
# print GameAchievements
print ("---------------")
print 'FriendsList'
print FriendsList
# print ("---------------")
# print 'PlayerAchievements'
# print OwnedGames
# print ("---------------")
# print 'PlayerStats'
# print PlayerStats
# print ("---------------")