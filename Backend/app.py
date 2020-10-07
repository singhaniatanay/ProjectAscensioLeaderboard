from flask import Flask,jsonify,request
import sys,os,json
import pandas as pd

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



if __name__ == '__main__':
	app.run(port=105)



