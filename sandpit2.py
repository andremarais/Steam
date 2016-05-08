import urllib2
import json
from pymongo import *
from pprint import pprint
import urllib, urllib2
import requests


client = MongoClient("localhost", 27017)
coll_players = client.steam.players


print coll_players.find({'_id': '76561197960859083'})[0]

