from flask import Flask,jsonify,request, make_response
import sys,os,json
import pandas as pd

from DAO.database import getUserDAO, createUserDAO


app  = Flask(__name__)
sys.path.append(os.path.join(os.path.dirname(__file__),'..','GetDataPython'))
from scrape import scrapeLeetcode, scrapeCodeforces

    


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
	emailID = request.headers.get('emailID')
	googleID = request.headers.get('googleID')
	return jsonify(getUserDAO(emailID,googleID))


@app.route('/createUser', methods=['POST'])
def createUser():
	googleID = request.headers.get('googleID')
	emailID = request.headers.get('emailID')
	cf_handle = request.args.get('cfHandle')
	lc_handle = request.args.get('lcHandle')
	data = createUserDAO(googleID,emailID,cf_handle,lc_handle)
	return make_response(jsonify(data), 201)


if __name__ == '__main__':
	app.run(port=3000)



