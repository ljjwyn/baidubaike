#!/usr/bin/python3
import pandas as pd
import pymongo
from sqlalchemy import create_engine


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def get_keywords():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['BaiduXueshuMedical']
    mycol = mydb["relatePaper"]
    keyWordsList = []
    for i in mycol.find():
        keyWordsList.extend(i['keyWords'])
    data = pd.Series(keyWordsList)
    data = pd.Series(data.value_counts())
    keys = pd.DataFrame(data.index, columns=['keys'])
    data = data.reset_index(drop=True)
    keys.insert(loc=1, column='count', value=data)
    cols = [i for i, x in enumerate(keys['keys']) if len(x) >= 15 or not check_contain_chinese(x)]
    finalKeys = keys.drop(cols, axis=0)
    finalKeys = finalKeys.reset_index(drop=True)
    res=finalKeys['keys'].values.tolist()
    #print(res[20000])
    #return res[0:5]
    return res

