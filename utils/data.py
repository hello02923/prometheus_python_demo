# -*- coding: utf-8 -*-
"""
與資料庫做互動
"""
from pymongo import MongoClient
#%%
client = MongoClient(
    host='localhost:27017', username='帳號', password='密碼')
db = client['Web']
#%%
def getProduct():
    data = list(db.productList.find({},{'_id':0, 'created_at':0, 'modified_at':0}))
    return data
# %%
