import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),'..','DAO'))
from DAO.database import getUserDAO
import requests,os


def isRequestValid(googleID):
	return getUserDAO(googleID)!=None

def isCFValid(cf_handle):
	url = 'https://codeforces.com/api/user.info?handles={}'.format(cf_handle)
	r = requests.get(url)
	return 'failed' in r.text.lower()

def isLCValid(lc_handle):
	url = 'https://leetcode.com/{}/'.format(lc_handle)
	r = requests.get(url)
	html_doc = r.text
	return 'Page Not Found' in html_doc and '404' in html_doc
