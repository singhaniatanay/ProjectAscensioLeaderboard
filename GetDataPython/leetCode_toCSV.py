import pandas as pd
from leetcode_scrape import getData
import sys,os


def leetcode_scrape(team):
	df = pd.read_csv('../Database/{}/UserDatabase.csv'.format(team))
	userLeetcode_Datas = []
	for i in df['LeetCode_User']:
	    userLeetcode_Datas.append(getData(i))
	df_leetcode = pd.DataFrame(userLeetcode_Datas)
	df_leetcode.to_csv('../Database/{}/leetcode_user_data.csv'.format(team),index=False)