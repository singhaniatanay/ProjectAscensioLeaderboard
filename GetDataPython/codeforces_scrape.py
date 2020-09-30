import pandas as pd
import requests
import sys


def codeforces_scrape(team):
	userData = []
	userDB = pd.read_csv('../Database/{}/userDatabase.csv'.format(team))
	for x in userDB['Codeforces_User']:    
	    url = 'https://codeforces.com/api/user.rating?handle={}'.format(x)
	    r = requests.get(url)
	    json = r.json()
	    userData += json['result']

	df = pd.DataFrame(userData)
	df = df.set_index(['handle'])
	df.to_csv('../Database/{}/codeforces_user_data.csv'.format(team))