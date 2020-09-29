import pandas as pd
from leetcode_scrape import getData

def saveData(csvFileName):
    df = pd.read_csv('./{}').format(csvFileName)
    userLeetcode_Datas = []
    for i in df['LeetCode_User']:
        userLeetcode_Datas.append(getData(i))

    df_leetcode = pd.DataFrame(userLeetcode_Datas)
    df_leetcode.to_csv('leetcode_usr_data.csv',index=False)