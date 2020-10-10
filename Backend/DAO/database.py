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


def getUserDAO(emailID,googleID):

	userData = user_collection.find_one({'_id':googleID})
	return userData

def createTeamDAO(googleID,teamCode):
	


def createUserDAO(googleID,emailID,cf_handle,lc_handle):
	userData = {
				'_id' : googleID,
				'emailID' : emailID,
				'cf_handle' : cf_handle,
				'lc_handle' : lc_handle,
				'teams' : []
				}
	
	try :
		dat =  user_collection.insert_one(userData)
		userData['success'] = True

	except :
		userData = {'success' : False}

	return userData

