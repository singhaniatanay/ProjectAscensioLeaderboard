import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),'..','DAO'))
from DAO.database import getUserDAO

def isRequestValid(req):
	return getUserDAO(req.headers.get('googleID'))!=None
