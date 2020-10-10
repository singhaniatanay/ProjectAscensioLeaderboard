from flask import Flask,jsonify,request, make_response
import sys,os,json
import pandas as pd
import time
from baseconv import base62 
from flask_apscheduler import APScheduler
from ValidationLayer.validationLayer import isRequestValid, isCFValid, isLCValid
from DAO.database import getUserDAO, createUserDAO, createTeamDAO, joinTeamDAO, midnightUpdateDAO

app  = Flask(__name__)
sys.path.append(os.path.join(os.path.dirname(__file__),'..','GetDataPython'))
from scrape import scrapeLeetcode, scrapeCodeforces

scheduler = APScheduler()  


@app.route('/leaderboard/leetcode')
def leaderboardLeetcode():
	team_name = request.args.get('team')
	scrapeLeetcode(team_name)
	leetcode_user_df = pd.read_csv('../Database/{}/leetcode_user_data.csv'.format(team_name))
	output_json = leetcode_user_df.to_json(orient="records")
	parsed_output = json.loads(output_json)
	return jsonify(parsed_output)


@app.route('/leaderboard/codeforces')
def leaderboardCodeforces():
	team_name = request.args.get('team')
	scrapeCodeforces(team_name)
	codeforces_user_df = pd.read_csv('../Database/{}/codeforces_user_data.csv'.format(team_name))
	output_json = codeforces_user_df.to_json(orient="records")
	parsed_output = json.loads(output_json)
	return jsonify(parsed_output)

@app.route('/getUserData')
def getUserData():
	googleID = request.headers.get('googleID')
	return jsonify(getUserDAO(googleID))


@app.route('/createUser', methods=['POST'])
def createUser():
	googleID = request.headers.get('googleID')
	emailID = request.headers.get('emailID')
	cf_handle = request.args.get('cfHandle')
	lc_handle = request.args.get('lcHandle')
	if not isCFValid(cf_handle):
		return make_response(jsonify({'success':False,'message':'Invalid CodeForces Handle'}))
	if not isLCValid(lc_handle):
		return make_response(jsonify({'success':False,'message':'Invalid LeetCode Handle'}))

	data = createUserDAO(googleID,emailID,cf_handle,lc_handle)
	return make_response(jsonify(data), 201)

@app.route('/createTeam', methods=['POST'])
def createTeam():
	if not isRequestValid(request.headers.get('googleID')):
		return make_response(jsonify({'status':'User Does Not Exist!'}),401)

	timestamp = int(round(time.time() * 1000))
	code = base62.encode(timestamp)
	team_name = request.args.get('teamName')
	googleID = request.headers.get('googleID')
	data = createTeamDAO(googleID,code,timestamp,team_name)
	return make_response(jsonify(data),201)

@app.route('/joinTeam', methods=['POST'])
def joinTeam():
	if not isRequestValid(request.headers.get('googleID')):
		return make_response(jsonify({'status':'User Does Not Exist!'}),401)

	teamCode = request.args.get('teamCode')
	googleID = request.headers.get('googleID')
	data = joinTeamDAO(googleID,teamCode)
	return make_response(jsonify(data),201)

def midnightDataFetch():
	print('===== Im Working =====')
	midnightUpdateDAO()

if __name__ == '__main__':
	# scheduler.add_job(id = 'cronJobWorker',func = midnightDataFetch,trigger = 'cron',hour = 19, minute = 41)
	scheduler.add_job(id = 'cronJobWorker',func = midnightDataFetch,trigger = 'interval', seconds = 5)
	scheduler.start()
	app.run(port=3000)





