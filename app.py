from flask import Flask
from flask import request
import pymongo

import json
import random
from flask import jsonify
from random import sample
import requests
from googleplaces import GooglePlaces, types, lang


from DBHandler import ConnectDB, UserDBOperation
from FiliterHandler import ViewTypeFiliter, ViewListFiliter
from PassDataHandler import GetSearchViewList, GetRecomandViewList
from WrapDataHandler import WrapResult

db = ConnectDB.DBConnction()


app = Flask(__name__)
# 處理json亂碼問題
app.config['JSON_AS_ASCII'] = False


@app.route("/test")
def test():
    res = db.OffshoreTaiwan_Attractions.find_one({"景點": "七美嶼"})
    jso = jsonify(str(res))
    return jso


# app.config['MONGO_URI'] = "mongodb://localhost:27017/New_ComingoDB"
# mongo = PyMongo(app)


@app.route('/')
def index():
    attraction = db.OffshoreTaiwan_Attractions.find_one({"景點": "七美嶼"})
    if attraction:
        return attraction['景點']
    else:
        return "Fail"


# ##########################################
# /addUserInfo : ["POST"]
# 新增user的資料
# ##########################################
@app.route('/addUserInfo', methods=["POST"])
def addUserInfo():
    COL = "User"
    userinfo = str(request.get_data(), "utf-8")
    userinfo_dict = json.loads(userinfo)
    db[COL].insert_one(userinfo_dict)
    return "get data"


# ##########################################
# /getUserInfo : ["POST"]
# 問題 : 如何知道是哪個使用者進行登入，並回傳那些data
# ##########################################
@app.route('/getUserInfo', methods=["POST"])
def getUserInfo():
    COL_NAME = "User"
    email = (request.form['email'])
    query = {'e-mail': email}
    print(email)
    if db[COL_NAME].count_documents(query):
        print("true")
        name = db[COL_NAME].find_one(query, {'userName': 1})
        return str(name['userName'])
    else:
        print("false")
        return "false"


# ##########################################
# /updateUserInfo : ["POST"]
# ##########################################
@app.route('/updateUserInfo', methods=["POST"])
def updateUserInfo():
    email = (request.form['email'])
    userName = (request.form['userName'])
    print(userName + " " + email)
    query = {'e-mail': email}
    newName = {"$set": {'userName': userName}}
    db["User"].update_one(query, newName)
    return "update success"


# ##########################################
# /testResult : ["POST"]
# res : 將測驗內容存進MongoDB
# ##########################################
@app.route('/testResult', methods=["POST"])
def testResult():
    COL_NAME = 'TestResult'
    result = str(request.get_data(), "utf-8");
    result_dict = json.loads(result)
    print(type(result_dict))
    email = result_dict['e-mail']
    print(email)
    db[COL_NAME].insert_one(result_dict)
    return "get data"


# ##########################################
# /deleteTestResult : ["POST"]
# res : 更新測驗內容存進MongoDB
# ##########################################
@app.route('/deleteTestResult', methods=["POST"])
def deleteTestResult():
    COL_NAME = 'TestResult'
    email = (request.form['email'])
    query = {'e-mail': email}
    db[COL_NAME].delete_one(query)
    return "delete success"


# ##########################################
# /getTestResult : ["POST"]
# res : 回傳測驗內容
# ##########################################
@app.route('/getTestResult', methods=["POST"])
def getTestResult():
    COL_NAME = 'TestResult'
    email = (request.form['email'])
    query = {'e-mail': email}
    print(email)
    res = db[COL_NAME].find_one(query, {'attractionTypeList': 1, 'transportType': 1})
    jso = jsonify(str(res))
    print(str(res))
    if res:
        return jso
    else:
        return "Fail"


# ##########################################
# /getAttractionInfo : ["GET"]
# args : type, name
# res : 以json格式，回傳單一景點資訊
# 活動須重新設計!!! name, region,city, month, 回傳的值不唯一
# ##########################################
@app.route('/getAttractionInfo', methods=["GET"])
def getAttractionInfo():
    attractionType = request.args.get("type")
    attractionName = request.args.get("name")

    res = ViewTypeFiliter.attractoionType_filiter(attractionType, attractionName)
    jso = jsonify(str(res))
    print(str(res))
    if res:
        return jso
    else:
        return "Fail"


# ##########################################
# /getSearchBarResultList : ["GET"]
# args : type, region, city
# res : 以json格式，回傳多筆景點
# !!須從新設計 新增景點總類 android 也須從新設計
# ##########################################
@app.route('/getSearchBarResult', methods=["GET"])
def getSearchBarResult():
    key = request.args.get("key")
    attraction_res = GetSearchViewList.searchInAttraction(key)
    blogRestaurant_res = GetSearchViewList.searchInBlogRestaurant(key)
    restaurant_res = GetSearchViewList.searchInRestaurant(key)
    bike_res = GetSearchViewList.searchInBike(key)

    # res = blogRestaurant_res
    res = attraction_res + blogRestaurant_res + restaurant_res + bike_res

    return "{{'data':[" + res[:-1] + "]}}"

# ##########################################
# /getAttractionsList : ["GET"]
# args : type, region, city
# res : 以json格式，回傳多筆景點

# ##########################################
@app.route('/getAttractionsList', methods=["GET"])
def getAttractionsList():
    attractionType = request.args.get("type")
    region = request.args.get("region")
    city = request.args.get("city")
    res = ViewListFiliter.attractionListFilter(attractionType, region, city)
    print(res)
    # col = "NorthTaiwan_Attractions"
    # res = db[col].find({},{'景點':1, '圖片':1, 'view':1, '地址':1}).sort("view", 1)
    # res = db.NorthTaiwan_Attractions.find({},{'景點':1, '圖片':1, 'view':1, '地址':1}).sort("view", 1)
    jso = jsonify(res)

    return jso

# ##########################################
# /getFestivalList : ["GET"]
# args : month, city
# res : 以json格式，回傳多筆Festival
# ##########################################
@app.route('/getFestivalList', methods=["GET"])
def getFestivalList():
    month = request.args.get("month")
    city = request.args.get("city")
    res = db["Taiwan_Festival"].find({'month': month, 'city': city}, {'name': 1, 'image': 1, '地址': 1})

    if str(res.count()) == '0':
        return 'none'
    else:
        jso = jsonify(WrapResult.wrapResult(res))
        return jso

# ##########################################
# /getRecomandList : ["GET"]
# args : 尚未決定
# res : 以json格式，回傳多筆attraction
# ##########################################
@app.route('/getRecomandList', methods=["POST"])
def getRecomandList():
    # COL_NAME = "User"
    types = (request.form['types'])
    # types = request.args.get("types")
    types = types[:-1]
    typelist = types.split(",")
    recommand_res = []
    for type in typelist:
        recommand_res += GetRecomandViewList.getFavorTypeAttractionLists(type)
    new_res = []
    print(len(recommand_res))
    for item in recommand_res:
        if item not in new_res:
            new_res.append(item)
    recommand_res = new_res
    print(len(recommand_res))
    recommand_res = sorted(recommand_res, key=lambda k: int(k['view']), reverse=True)

    res_str = str(recommand_res)
    print(len(recommand_res))

    return  "{'data':[" + res_str[1:len(res_str) - 1] + "]}"

# ##########################################
# /addFavorAttraction : ["POST"]
# res : 將景點類型、名稱與e-mail載入資料庫中，若以存在，部會重複存
# ##########################################
@app.route('/addFavorAttraction', methods=["POST"])
def addFavorAttraction():
    COL = "FavorAttraction"
    favorAttractionInfo = str(request.get_data(), "utf-8");
    favorAttractionInfo = json.loads(favorAttractionInfo)

    userAccount = favorAttractionInfo['userAccount']
    type = favorAttractionInfo['type']
    name = favorAttractionInfo['name']
    query = {'$and' : [{'userAccount':userAccount,'type':type,'name':name}]}
    count = db[COL].count_documents(query)
    print(count)
    if count > 0:
        return "exisit"
    else:
        db[COL].insert_one(favorAttractionInfo)
    return "get data"

# ##########################################
# /removeFavorAttraction : ["POST"]
# res : 回傳測驗內容
# ##########################################
@app.route('/removeFavorAttraction', methods=["Post"])
def removeFavorAttraction():
    COL = "FavorAttraction"
    favorAttractionInfo = str(request.get_data(), "utf-8");
    favorAttractionInfo = json.loads(favorAttractionInfo)
    # userAccount = request.args.get("userAccount")
    # name = request.args.get("name")
    # type = request.args.get("type")

    # print(userAccount)
    userAccount = favorAttractionInfo['userAccount']
    name = favorAttractionInfo['name']
    type = favorAttractionInfo['type']
    print(userAccount + " " + name + " " + type)
    query = {'$and' : [{'userAccount':userAccount},{'type':type},{'name':name}]}
    #
    print(query)
    res = db[COL].delete_one(query)

    count = db[COL].count_documents(query)
    print(count)
    if count==0 :
        return "Delete Success"
    else:
        return "Fail Delete"

# ##########################################
# /getFavorAttractionList : ["POST"]
# res : 回傳測驗內容
# ##########################################
@app.route('/getFavorAttractionList', methods=["Post"])
def getFavorAttractionList():
    COL = "FavorAttraction"
    favorAttractionInfo = str(request.get_data(), "utf-8")
    favorAttractionInfo = json.loads(favorAttractionInfo)
    # userAccount = request.args.get("userAccount")

    userAccount = favorAttractionInfo['userAccount']
    print(userAccount)
    # query = {'userAccount':userAccount}
    #
    res = db[COL].find({'userAccount':userAccount})

    list = ""
    for item in res:
        attractionType = item["type"]
        attractionName = item["name"]
        searchRes = ViewTypeFiliter.attractoionType_filiter(attractionType, attractionName)
        list += "{'type':"+attractionType+","+str(searchRes)[1:]+","

    list =  "{'data':[" + list[:-1] + "]}"
    # return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
    return list


# ##########################################
# 爬取評論資訊
# /getAttractionReviews : ["GET"]
# args : attractionName
# ##########################################
@app.route('/getAttractionReviews', methods=["GET"])
def getAttractionReviews():
    name = request.args.get("name")
    API = "AIzaSyDPhivwAfyfrDBUWFIT2wt47-QA431Xj_Q"
    google_places = GooglePlaces(API)

    query_result = google_places.text_search(query=name, language=lang.CHINESE_TRADITIONAL)

    if query_result.has_attributions:
        print(query_result.has_attributions)

    place = query_result.places[0]
    print(place.name)
    place_id = place.place_id

    url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=" + API + "&language=zh-Hant"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    dict_state = json.loads(response.text)
    result = str(dict_state['result'])
    result = result.replace("\n", "")
    result = result.strip()
    print(result)
    return result

# ##########################################
# 搜尋景點資訊
# /getFestivalByMonth : ["GET"]
# args : currentFestival
# ##########################################
@app.route('/getFestivalByMonth', methods=["GET"])
def getFestivalByMonth():
    month = request.args.get("month")
    res = db["Taiwan_Festival"].find({'month': month}, {'name': 1, '活動時間': 1, '地址': 1})

    if str(res.count()) == '0':
        return 'none'
    else:
        jso = jsonify(WrapResult.wrapResult(res))
        return jso

# ##########################################
# __main__
# ##########################################
if __name__ == "__main__":
    app.run(host='0.0.0.0')
