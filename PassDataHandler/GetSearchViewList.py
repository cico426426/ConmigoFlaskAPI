from DBHandler import ConnectDB

db = ConnectDB.DBConnction()

# 在attraction中搜尋-------------------------------------------------------------------------------------------
def searchInAttraction(Key):

    query = {"$or" : [{"地址": {"$regex":Key}},{ "景點":Key}]}
    print(query)
    res = db.NorthTaiwan_Attractions.find(query, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1})
    print(res)
    if (not res):
        res = db.CentralTaiwan_Attractions.find(query, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1})
    if (not res):
        res = db.SouthernTaiwan_Attractions.find(query, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1})
    if (not res):
        res = db.EasternTaiwan_Attractions.find(query, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1})
    if (not res):
        res = db.OffshoreTaiwan_Attractions.find(query, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1})
    # print(res)
    # return [item for item in res]
    list = ""
    # return [item for item in res]
    count = 0
    for item in res:
        list += "{'type':'attraction'," + str(item)[1:] + ","
        count += 1
    if count==0:
        return ""
    return list[:-1] +","
# 在blog restaurant中搜尋-------------------------------------------------------------------------------------
def searchInBlogRestaurant(Key):
    query = {"$or" : [{"name":{"$regex":Key}},{"地址":Key}]}
    res = db["TaiwanBlogRestaurant"].find(query, {'name': 1, 'img': 1, '地址': 1})
    list = ""
    # return [item for item in res]
    count = 0
    for item in res:
        list += "{'type':'blogRestaurant'," + str(item)[1:] + ","
        count += 1
    if count==0:
        return ""
    return list[:-1]+","
# 在resturant中搜尋-------------------------------------------------------------------------------------------
def searchInRestaurant(Key):
    query  = {"$or" : [{"name":{"$regex":Key}},{"地址":Key}]}
    res = db["Restaurant"].find(query, {'name': 1, 'img': {"$slice": ["$img", 1]}, 'rating': 1, '地址': 1})

    list = ""
    count = 0
    for item in res:
        list += "{'type':'restaurant'," + str(item)[1:] + ","
        count += 1
    if count==0:
        return ""
    return list[:-1]+","
    # return [item for item in res]

# 在Hotel中搜尋-------------------------------------------------------------------------------------------
def searchInHotel(Key):
    query  = {"$or" : [{"名稱":{"$regex":Key}},{"地址":Key}]}
    res = db["Hotel"].find(query, {'名稱': 1, '圖一': 1, '星級': 1, '地址': 1})
    # return [item for item in res]
    list = ""
    count = 0
    for item in res:
        list += "{'type':'hotel'," + str(item)[1:] + ","
        count += 1
    if count==0:
        return ""
    return list[:-1]+","

# 在Bike中搜尋-------------------------------------------------------------------------------------------
def searchInBike(Key):
    query  = {"$or" : [{"名稱":{"$regex":Key}},{"地址":Key}]}
    res = db["BikeStation"].find(query, {'名稱': 1, '地址': 1, "容量":1})
    # return [item for item in res]
    list = ""
    count = 0
    for item in res:
        list += "{'type':'bike'," + str(item)[1:] + ","
        count += 1
    if count==0:
        return ""
    return list[:-1]+","
