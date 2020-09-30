from bs4 import BeautifulSoup
import requests,os

def getData(userID):
    url = 'https://leetcode.com/{}/'.format(userID)
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc)

    rows = soup.find_all('span','badge')
    ans = []
    c1 = eval(rows[0].text.strip())
    if c1==0:
        ans = rows[1:4]
    else:
        ans = rows[3:6]

    ans = [x.text.strip() for x in ans]

    dic = {'User' : userID,
        'Solved Questions' : int(ans[0][:ans[0].find('/')].strip()),
           'Total Questions' : int(ans[0][ans[0].find('/')+1:].strip()),
          'Accepted Submissions' : int(ans[1][:ans[1].find('/')].strip()),
           'Total Submissions' : int(ans[1][ans[1].find('/')+1:].strip()),
          'Acceptance Rate' : eval(ans[2][:ans[2].find('%')].strip())}
    
    return dic