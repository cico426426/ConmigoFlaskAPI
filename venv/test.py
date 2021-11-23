import pymongo

CONNECTION_STRING = "mongodb+srv://new-user:7XRipwIAtJMPxUOi@comingocluster.joldg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('Comigo_DB')

res = db.NorthTaiwan_Attractions.find({},{'景點':1, '圖片':1, 'view':1, '地址':1}).sort("view", 1).limit(3)
for doc in res:
    print(doc)