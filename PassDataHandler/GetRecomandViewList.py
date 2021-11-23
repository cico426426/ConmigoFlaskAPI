from random import sample
from DBHandler import ConnectDB

db = ConnectDB.DBConnction()

def getFavorTypeAttractionLists(type):

    list = []
    cultureList = ["#文青必訪", "#古蹟巡禮", "#打卡熱點", "#寺廟祈福", "#戰地文化", "#漫遊客庄", "#燈塔"]
    viewList = ["#水上活動", "#打卡熱點", "#生態體驗", "#地質奇觀", "#泡溫泉", "#迎曙光", "#登山步道"]
    artList = ["#台灣燈會", "#看展覽", "#藝術"]
    shoppingList = ["#主題樂園", "#必買", "#泡溫泉", "#逛老街", "#逛夜市"]
    foodList = ["#吃海鮮", "#非吃不可", "#逛老街", "#逛夜市"]

    if type == "文化古蹟":
        list = cultureList
    elif type == "風景":
        list = viewList
    elif type == "藝文展覽":
        list = artList
    elif type == "購物中心":
        list = shoppingList
    elif type == "美食":
        list = foodList

    colList = ["NorthTaiwan_Attractions","CentralTaiwan_Attractions"
    ,"SouthernTaiwan_Attractions","EasternTaiwan_Attractions","OffshoreTaiwan_Attractions"]
    res = []
    for col in colList :
        res += searchInRegion(list, col)
    # print(len(res))
    # res = list(dict.fromkeys(res))
    # print(len(res))

    if type in ["風景", "文化古蹟"]:
        res = sample(res, 30)
    else:
        res = sample(res, 35)

    return res

def searchInRegion(list, COL):

    res = db[COL].find({"hashtag" : {"$in" : list}}, {'景點': 1, '圖片': 1, 'view': 1, '地址': 1})
    res_list = [item for item in res]

    return res_list