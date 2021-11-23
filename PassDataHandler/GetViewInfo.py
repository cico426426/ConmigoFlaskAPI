from DBHandler import ConnectDB

db = ConnectDB.DBConnction()

# Bike--------------------------------------------------------------------------------
def search_Bike(attractionName):
    query = {"名稱" : attractionName}
    res = db["BikeStation"].find_one(query)
    return res

# Hotel--------------------------------------------------------------------------------
def search_Hotel(attractionName):
    query = {"名稱" : attractionName}
    res = db["Hotel"].find_one(query)
    return res

# Restaurant--------------------------------------------------------------------------------
def search_restaurant(attractionName):
    query = {'name': attractionName}
    count = db['Restaurant'].find(query).count()
    print(count)
    busRes = db["Restaurant"].find_one(query, {'bus':1})

    # if(busRes['bus']==[]):
    #     # res = db["Restaurant"].find_one(query, {'name': 1, 'city': 1, '地址': 1, 'X': 1, 'Y': 1,
    #     #                                         'phone': 1, 'openingHourList': 1, 'rating': 1, 'url': 1,
    #     #                                         'website': 1,  'bus': 1, 'parking': 1,
    #     #                                         'img': {"$slice": ["$img", 1]}})
    #     res = db["Restaurant"].find_one(query, {'reviews':1})
    # else:
    res = db["Restaurant"].find_one(query)
    return res

# Attraction--------------------------------------------------------------------------------
def search_attraction(attractionName):
    query = {"景點": attractionName}
    print(attractionName)
    res = db.NorthTaiwan_Attractions.find_one(query)
    if (not res):
        res = db.CentralTaiwan_Attractions.find_one(query)
    if (not res):
        res = db.SouthernTaiwan_Attractions.find_one(query)
    if (not res):
        res = db.EasternTaiwan_Attractions.find_one(query)
    if (not res):
        res = db.OffshoreTaiwan_Attractions.find_one(query)
    return res

# Blog Restaurant--------------------------------------------------------------------------------
def search_blogRestaurant(attactionName):
    query = {"name": attactionName}
    res = db.TaiwanBlogRestaurant.find_one(query)
    return res

# Festuval 不在此功能上 應分開--------------------------------------------------------------------------------
def search_festival(attractionName):
    query = {"name": attractionName}
    res = db.Taiwan_Festival.find_one(query)
    return res