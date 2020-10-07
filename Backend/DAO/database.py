import pyrebase
import json
from firebase_admin import credentials, auth





cred = credentials.Certificate("../Config/firebaseAdminConfig.json")
fb = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('../Config/firebaseConfig.json')))


print("Hello World")
print(fb)
print(cred)
print(pb)
