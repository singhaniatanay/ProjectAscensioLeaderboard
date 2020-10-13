from flask import Flask, jsonify
from flask_pymongo import pymongo
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),'..','Config'))
from atlassconfig import url
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__),'..','..','GetDataPython'))
import leetcode_scrape



CONNECTION_STRING = url
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('database')
user_collection = pymongo.collection.Collection(db, 'User')
team_collection = pymongo.collection.Collection(db, 'Team')





def midnightUpdateDAO():
	for currUserData in user_collection.find():
		lc_handle = currUserData['lc_handle']
		lc_curr_data = leetcode_scrape.getData(lc_handle)
		today = str(datetime.today().day) + '-' + str(datetime.today().month) + '-' +str(datetime.today().year)
		currUserData['lc_data'].append([today,lc_curr_data['Solved Questions'],lc_curr_data['Acceptance Rate']])
		currUserData['last_lc_Data'] = lc_curr_data['Solved Questions']
		try :
			user_collection.update_one({'_id':currUserData['_id']}, {'$set':currUserData})
		except :
			print('Ahh! Shit Here We Go Again..',' UserID : ',currUserData['_id'])



def getUserDAO(googleID):
	userData = user_collection.find_one({'_id':googleID})
	return userData

def getTeamDAO(teamCode):
	teamData = team_collection.find_one({'_id':teamCode})
	return teamData

def getTeamDataDAO(teamCode):
	team = team_collection.find_one({'_id':teamCode})
	teamData = {}
	for member in team['members']:
		memberData = user_collection.find_one({'_id':member})
		lc_curr_data = leetcode_scrape.getData(memberData['lc_handle'])
		dat = {}
		dat['lc_data'] = memberData['lc_data']
		dat['lc_curr_data'] = lc_curr_data
		teamData[member] = dat
		
		


	return teamData


def createTeamDAO(googleID,teamCode,timestamp,team_name):
	data = {
			'_id' : teamCode,
			'members' : [googleID],
			'time' : timestamp,
			'teamName' : team_name
			}
	try :
		dat = team_collection.insert_one(data)
		data['success'] = True
		userData = getUserDAO(googleID)
		userData['teams'].append(teamCode)
		user_collection.update_one({'_id':googleID}, {'$set' : userData})
	except :
		data = {'success' : False, 'message' : 'Team Creation Failed'}

	return data

def joinTeamDAO(googleID,teamCode):
	try :
		prev_data = team_collection.find_one({'_id':teamCode})
		if googleID in prev_data['members']:
			return {'success' : False, 'message' : 'User Already present in the team!'}

		userData = getUserDAO(googleID)
		userData['teams'].append(teamCode)
		prev_data['members'].append(googleID)
		try :
			team_collection.update_one({'_id': teamCode}, {'$set' : prev_data})
			user_collection.update_one({'_id':googleID}, {'$set' : userData})
			prev_data['success'] = True
		except :
			prev_data = {'success' : False, 'message' : 'Team Update Failed!'}

	except:
		prev_data = {'success' : False, 'message' : 'Team Does not exist!'}

	return prev_data


def createUserDAO(googleID,emailID,cf_handle,lc_handle):
	lc_curr_data = leetcode_scrape.getData(lc_handle)
	userData = {
				'_id' : googleID,
				'emailID' : emailID,
				'cf_handle' : cf_handle,
				'lc_handle' : lc_handle,
				'teams' : [],
				'lc_data' : [],
				'last_lc_Data' : lc_curr_data['Solved Questions']
				}
	
	try :
		dat =  user_collection.insert_one(userData)
		userData['success'] = True

	except :
		userData = {'success' : False,'message' : 'User Could not be created'}

	return userData





