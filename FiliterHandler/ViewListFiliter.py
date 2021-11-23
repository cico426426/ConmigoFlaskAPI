from PassDataHandler import GetViewList

def attractionListFilter(type, region, city):
    searchRes = ""
    if (type == "attraction"):
        searchRes = GetViewList.get_attractionList(region, city)
    elif (type == "blogRestaurant"):
        searchRes = GetViewList.get_blogRestaurantList(region, city)
    elif (type == 'restaurant'):
        searchRes = GetViewList.get_restaurant(region, city)
    elif (type == 'hotel'):
        searchRes = GetViewList.get_hotel(region, city)
    elif type=="bike":
        searchRes = GetViewList.get_bike(region, city)

    # print(searchRes)
    return searchRes