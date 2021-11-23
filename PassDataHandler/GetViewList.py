from flask import request
import random
from flask import jsonify
from random import sample
import requests

from DBHandler import ConnectDB
from WrapDataHandler import WrapResult

db = ConnectDB.DBConnction()

# Bike--------------------------------------------------------------------------------
def get_bike(region, city):
    COLNAME = "BikeStation"
    city = city.replace("台", "臺")
    if city != "全區":
        res = db[COLNAME].find({"縣市": city}, {'名稱':1, "地址" : 1, "容量":1})
        return WrapResult.wrapResult(res)
    else:
        if region == "北部":
            res_str = str(get_northBikeInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "中部":
            res_str = str(get_centralBikeInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "南部":
            res_str = str(get_southBikeInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "東部":
            res_str = str(get_eastBikeInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "離島":
            res_str = str(get_offshoreBikeInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "全台":
            res = get_northHotelInRandom(COLNAME) + get_centralHotelInRandom(
                COLNAME) + get_southHotelInRandom(COLNAME) \
                  + get_offshoreHotelInRandom(COLNAME)
            res_str = str(res)
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"

def get_northBikeInRandom(COLNAME):
    # Keelung_res = [item for item in random_bike(COLNAME, "基隆市").limit(10)]
    Taipei_res = [item for item in random_bike(COLNAME, "臺北市")]
    NewTaipei_res = [item for item in random_bike(COLNAME, "新北市")]
    # Yilan_res = [item for item in random_bike(COLNAME, "宜蘭縣").limit(10)]
    Taoyuan = [item for item in random_bike(COLNAME, "桃園市")]
    HsinchuCountry = [item for item in random_bike(COLNAME, "新竹市")]
    # HisnchuCity = [item for item in random_bike(COLNAME, "新竹縣").limit(10)]

    res = Taipei_res + NewTaipei_res + Taoyuan + HsinchuCountry
    # print(res[0]['rating'])
    # res = sorted(res, key=lambda k: k['rating'], reverse=True)

    # print(len(res))
    return res

def get_centralBikeInRandom(COLNAME):
    Miaoli = [item for item in random_bike(COLNAME, "苗栗縣")]
    Taichung = [item for item in random_bike(COLNAME, "臺中市")]
    # Changhua = [item for item in random_hotel(COLNAME, "彰化縣").limit(10)]
    # Nantou = [item for item in random_hotel(COLNAME, "南投縣").limit(10)]
    # Yunlin = [item for item in random_hotel(COLNAME, "雲林縣").limit(10)]

    res = Miaoli + Taichung
    return res

def get_southBikeInRandom(COLNAME):
    # ChiayiCountry = [item for item in random_hotel(COLNAME, "嘉義縣").limit(10)]
    ChiayiCity = [item for item in random_hotel(COLNAME, "嘉義市").limit(10)]
    Tainan = [item for item in random_hotel(COLNAME, "臺南市").limit(10)]
    Kaohsiung = [item for item in random_hotel(COLNAME, "高雄市").limit(10)]
    Pingtung = [item for item in random_hotel(COLNAME, "屏東縣").limit(10)]

    res =  ChiayiCity + Tainan + Kaohsiung + Pingtung
    return res

def get_eastBikeInRandom(COLNAME):
    Hualien = [item for item in random_hotel(COLNAME, "花蓮縣")]
    Taitung = [item for item in random_hotel(COLNAME, "臺東縣")]

    res = Hualien + Taitung
    return res

def get_offshoreBikeInRandom(COLNAME):
    # Penghu = [item for item in random_hotel(COLNAME, "澎湖縣")]
    Kinmen = [item for item in random_hotel(COLNAME, "金門縣")]
    # Matusu = [item for item in random_hotel(COLNAME, "連江縣")]

    res =  Kinmen
    return res

def random_bike(COLNAME, city):
    count = db[COLNAME].find({"縣市": city}).count()
    if count != 0:
        start = random.randrange(count)
        res = db[COLNAME].find({"縣市": city}, {'名稱': 1, '地址': 1, "容量":1})[
              start:start + 10]
        return res

    res = db[COLNAME].find({"縣市": city}, {'名稱': 1, '地址': 1}).limit(10)

    return res
# Hotel--------------------------------------------------------------------------------
def get_hotel(region, city):
    COLNAME = "Hotel"
    print(city)
    city = city.replace("台", "臺")
    if city != "全區":
        res = db[COLNAME].find({"縣市": city}, {'名稱': 1, '圖一':  1, '星級': 1, '地址': 1}).sort(
            "星級", 1).limit(100)
        print(res)
        return WrapResult.wrapResult(res)
    else:
        if region == "北部":
            res_str = str(get_northHotelInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "中部":
            res_str = str(get_centralHotelInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "南部":
            res_str = str(get_southHotelInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "東部":
            res_str = str(get_eastHotelInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "離島":
            res_str = str(get_offshoreHotelInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "全台":
            res = get_northHotelInRandom(COLNAME) + get_centralHotelInRandom(
                COLNAME) + get_southHotelInRandom(COLNAME) \
                  + get_eastHotelInRandom(COLNAME) + get_offshoreHotelInRandom(COLNAME)
            res_str = str(res)
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"

def get_northHotelInRandom(COLNAME):
    Keelung_res = [item for item in random_hotel(COLNAME, "基隆市").limit(10)]
    Taipei_res = [item for item in random_hotel(COLNAME, "臺北市").limit(10)]
    NewTaipei_res = [item for item in random_hotel(COLNAME, "新北市").limit(10)]
    Yilan_res = [item for item in random_hotel(COLNAME, "宜蘭縣").limit(10)]
    Taoyuan = [item for item in random_hotel(COLNAME, "桃園市").limit(10)]
    HsinchuCountry = [item for item in random_hotel(COLNAME, "新竹市").limit(10)]
    HisnchuCity = [item for item in random_hotel(COLNAME, "新竹縣").limit(10)]
    res = Keelung_res + Taipei_res + NewTaipei_res + Yilan_res + Taoyuan + HsinchuCountry + HisnchuCity
    # print(res[0]['rating'])
    # res = sorted(res, key=lambda k: k['rating'], reverse=True)

    # print(len(res))
    return res

def get_centralHotelInRandom(COLNAME):
    Miaoli = [item for item in random_hotel(COLNAME, "苗栗縣").limit(10)]
    Taichung = [item for item in random_hotel(COLNAME, "臺中市").limit(10)]
    Changhua = [item for item in random_hotel(COLNAME, "彰化縣").limit(10)]
    Nantou = [item for item in random_hotel(COLNAME, "南投縣").limit(10)]
    Yunlin = [item for item in random_hotel(COLNAME, "雲林縣").limit(10)]

    res = Miaoli + Taichung + Changhua + Nantou + Yunlin
    return res

def get_southHotelInRandom(COLNAME):
    ChiayiCountry = [item for item in random_hotel(COLNAME, "嘉義縣").limit(10)]
    ChiayiCity = [item for item in random_hotel(COLNAME, "嘉義市").limit(10)]
    Tainan = [item for item in random_hotel(COLNAME, "臺南市").limit(10)]
    Kaohsiung = [item for item in random_hotel(COLNAME, "高雄市").limit(10)]
    Pingtung = [item for item in random_hotel(COLNAME, "屏東縣").limit(10)]

    res = ChiayiCountry + ChiayiCity + Tainan + Kaohsiung + Pingtung
    return res

def get_eastHotelInRandom(COLNAME):
    Hualien = [item for item in random_hotel(COLNAME, "花蓮縣")]
    Taitung = [item for item in random_hotel(COLNAME, "臺東縣")]

    res = Hualien + Taitung
    return res

def get_offshoreHotelInRandom(COLNAME):
    Penghu = [item for item in random_hotel(COLNAME, "澎湖縣")]
    Kinmen = [item for item in random_hotel(COLNAME, "金門縣")]
    Matusu = [item for item in random_hotel(COLNAME, "連江縣")]

    res = Penghu + Kinmen + Matusu
    return res

def random_hotel(COLNAME, city):
    count = db[COLNAME].find({"縣市": city}).count()
    if count != 0:
        start = random.randrange(count)
        res = db[COLNAME].find({"縣市": city}, {'名稱': 1, '圖一': 1, '地址': 1, '星級': 1})[
              start:start + 10]
        return res

    res = db[COLNAME].find({"縣市": city}, {'名稱': 1, '圖一': 1, '地址': 1, '星級': 1}).limit(10)

    return res

# Restaurant--------------------------------------------------------------------------------
def get_restaurant(region, city):
    COLNAME = "Restaurant"
    city = city.replace("台", "臺")
    print("get restaurant")
    if city != "全區":
        res = db[COLNAME].find({"city": city}, {'name': 1, 'img': {"$slice": ["$img", 1]}, 'rating': 1, '地址': 1}).sort(
            "rating", 1).limit(150)
        print(res)
        return WrapResult.wrapResult(res)
    else:
        if region == "北部":
            res_str = str(get_northRestaturantInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "中部":
            res_str = str(get_centralRestaturantInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "南部":
            res_str = str(get_southRestaurantInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "東部":
            res_str = str(get_eastRestaurantInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "離島":
            res_str = str(get_offshoreRestaurantInRandom(COLNAME))
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
        elif region == "全台":
            res = get_northRestaturantInRandom(COLNAME) + get_centralRestaturantInRandom(
                COLNAME) + get_southRestaurantInRandom(COLNAME) \
                  + get_eastRestaurantInRandom(COLNAME) + get_offshoreRestaurantInRandom(COLNAME)
            res_str = str(res)
            return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"


def get_northRestaturantInRandom(COLNAME):
    # n = random_data(COLNAME, "臺北市")
    Keelung_res = [item for item in random_data(COLNAME, "基隆市")]
    Taipei_res = [item for item in random_data(COLNAME, "臺北市")]
    NewTaipei_res = [item for item in random_data(COLNAME, "新北市")]
    Yilan_res = [item for item in random_data(COLNAME, "宜蘭縣")]
    Taoyuan = [item for item in random_data(COLNAME, "桃園市")]
    HsinchuCountry = [item for item in random_data(COLNAME, "新竹市")]
    HisnchuCity = [item for item in random_data(COLNAME, "新竹縣")]
    res = Keelung_res + Taipei_res + NewTaipei_res + Yilan_res + Taoyuan + HsinchuCountry + HisnchuCity
    # print(res[0]['rating'])
    # res = sorted(res, key=lambda k: k['rating'], reverse=True)

    # print(len(res))
    return res

def get_centralRestaturantInRandom(COLNAME):
    Miaoli = [item for item in random_data(COLNAME, "苗栗縣")]
    Taichung = [item for item in random_data(COLNAME, "臺中市")]
    Changhua = [item for item in random_data(COLNAME, "彰化縣")]
    Nantou = [item for item in random_data(COLNAME, "南投縣")]
    Yunlin = [item for item in random_data(COLNAME, "雲林縣")]

    res = Miaoli + Taichung + Changhua + Nantou + Yunlin
    return res


def get_southRestaurantInRandom(COLNAME):
    ChiayiCountry = [item for item in random_data(COLNAME, "嘉義縣")]
    ChiayiCity = [item for item in random_data(COLNAME, "嘉義市")]
    Tainan = [item for item in random_data(COLNAME, "臺南市")]
    Kaohsiung = [item for item in random_data(COLNAME, "高雄市")]
    Pingtung = [item for item in random_data(COLNAME, "屏東縣")]

    res = ChiayiCountry + ChiayiCity + Tainan + Kaohsiung + Pingtung
    return res


def get_eastRestaurantInRandom(COLNAME):
    Hualien = [item for item in random_data(COLNAME, "花蓮縣")]
    Taitung = [item for item in random_data(COLNAME, "臺東縣")]

    res = Hualien + Taitung
    return res


def get_offshoreRestaurantInRandom(COLNAME):
    Penghu = [item for item in random_data(COLNAME, "澎湖縣")]
    Kinmen = [item for item in random_data(COLNAME, "金門縣")]
    Matusu = [item for item in random_data(COLNAME, "連江縣")]

    res = Penghu + Kinmen + Matusu
    return res


def random_data(COLNAME, city):
    count = db[COLNAME].find({"city": city}).count()
    if count != 0:
        start = random.randrange(count)
        res = db[COLNAME].find({"city": city}, {'name': 1, 'img': {"$slice": ["$img", 1]}, '地址': 1, 'rating': 1})[
              start:start + 10]
        return res
    res = db[COLNAME].find({"city": city}, {'name': 1, 'img': {"$slice": ["$img", 1]}, '地址': 1, 'rating': 1}).limit(10)

    return res

# Attraction--------------------------------------------------------------------------------
def get_attractionList(region, city):
    COLNAME = ""

    if region == "北部":
        COLNAME = "NorthTaiwan_Attractions"
    elif region == "中部":
        COLNAME = "CentralTaiwan_Attractions"
    elif region == "南部":
        COLNAME = "SouthernTaiwan_Attractions"
    elif region == "東部":
        COLNAME = "EasternTaiwan_Attractions"
    elif region == "離島":
        COLNAME = "OffshoreTaiwan_Attractions"
    elif region == "全台":

        north_res = [item for item in db["NorthTaiwan_Attractions"].find({}, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1})]
        central_res = [item for item in db["CentralTaiwan_Attractions"].find({}, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1})]
        southern_res = [item for item in  db["SouthernTaiwan_Attractions"].find({}, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1})]
        east_res = [item for item in db["EasternTaiwan_Attractions"].find({}, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1})]
        offshore_res = [item for item in  db["OffshoreTaiwan_Attractions"].find({}, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1})]

        res = []
        res += north_res + central_res + southern_res + east_res + offshore_res

        res = sorted(res, key=lambda k: int(k['view']), reverse=True)
        res_str = str(res)

        print(len(res))
        print(north_res)
        return "{'data':[" + res_str[1:len(res_str) - 1] + "]}"
    print(COLNAME)
    res = ""
    if city == "全區":
        res = db[COLNAME].find({}, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1}).sort("view", 1)
        print(res)
    else:
        city = city.replace("台", "臺")
        res = db[COLNAME].find({'城市': city}, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1}).sort("view", 1)
    return WrapResult.wrapResult(res)

# BlogRestaurant--------------------------------------------------------------------------------
def get_blogRestaurantList(region, city):
    NORTH_CITIES = ["基隆市", "新北市", "台北市", "宜蘭縣", "新竹縣", "新竹市", "桃園市"]
    CENTRAL_CITIES = ["南投縣", "台中市", "彰化縣", "苗栗縣", "雲林縣"]
    SOUTH_CITIES = ["台南市", "嘉義市", "嘉義縣", "屏東縣", "高雄市"]
    EAST_CITIES = ["台東縣", "花蓮縣"]
    COL = "TaiwanBlogRestaurant"
    CITIES = []
    if region == "北部":
        CITIES = NORTH_CITIES
    elif region == "中部":
        CITIES = CENTRAL_CITIES
    elif region == "南部":
        CITIES = SOUTH_CITIES
    elif region == "東部":
        CITIES = EAST_CITIES
    elif region == "全台":
        # res = db[COL].aggregate([{'$sample':{'size', 100}}])
        # res = db[COL].find({}, {'name': 1, 'img': 1, '地址': 1}).limit(10)
        count = db[COL].estimated_document_count()
        start = random.randrange(count)
        res = db[COL].find({}, {'name': 1, 'img': 1, '地址': 1})[start:start + 75]
        return WrapResult.wrapResult(res)
    if city == "全區":

        res = db[COL].find({'city': {'$in': CITIES}}, {'name': 1, 'img': 1, '地址': 1}).limit(75)
    else:
        # city = city.replace("台", "臺")
        print(city)
        res = db[COL].find({'city': city}, {'name': 1, 'img': 1, '地址': 1}).limit(75)
    return WrapResult.wrapResult(res)