from flask import request

import json
from DBHandler import ConnectDB
db = ConnectDB.DBConnction
COL = "User"

def addUserInfo(userInfo):    
    userinfo_dict = json.loads(userInfo)
    db[COL].insert_one(userinfo_dict)
    return "get data"

def getUserInfo(email):
    query = {'e-mail': email}
    print(email)
    if db[COL].count_documents(query):
        print("true")
        name = db[COL].find_one(query, {'userName': 1})
        return str(name['userName'])
    else:
        print("false")
        return "false"

def updateUserInfo(userName, email):
    print(userName + " " + email)
    query = {'e-mail': email}
    newName = {"$set": {'userName': userName}}
    db[COL].update_one(query, newName)
    return "update success"