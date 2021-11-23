from PassDataHandler import GetViewInfo, GetSearchViewList, GetViewList, GetRecomandViewList

def attractoionType_filiter(type, attractionName):
    searchRes = ""
    print(type, attractionName)
    if (type == "attraction"):
        searchRes = GetViewInfo.search_attraction(attractionName)
    elif (type == "blogRestaurant"):
        searchRes =  GetViewInfo.search_blogRestaurant(attractionName)
    elif type == "restaurant":
        searchRes =  GetViewInfo.search_restaurant(attractionName)
    elif type == "hotel":
        searchRes =  GetViewInfo.search_Hotel(attractionName)
    elif type == "bike":
        searchRes =  GetViewInfo.search_Bike(attractionName)
    elif (type == "festival"):
        searchRes =  GetViewInfo.search_festival(attractionName)

    return searchRes