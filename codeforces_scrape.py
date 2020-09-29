userData = []
userDB = pd.read_csv('./userDatabase.csv')
for x in userDB['Codeforces_User']:    
    url = 'https://codeforces.com/api/user.rating?handle={}'.format(x)
    r = requests.get(url)
    json = r.json()
    userData += json['result']

df = pd.DataFrame(userData)
df = df.set_index(['handle'])
df.to_csv('codeforces_DB.csv')