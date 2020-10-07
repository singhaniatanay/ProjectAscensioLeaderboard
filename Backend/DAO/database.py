from flask import Flask, jsonify
from flask_pymongo import pymongo
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),'..','Config'))
from atlassconfig import url


CONNECTION_STRING = url
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('database')
user_collection = pymongo.collection.Collection(db, 'User')
team_collection = pymongo.collection.Collection(db, 'Team')


for x in team_collection.find():
	print(x)