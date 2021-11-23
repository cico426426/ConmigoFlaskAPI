import pymongo

def DBConnction():
    CONNECTION_STRING = "mongodb+srv://new-user:7XRipwIAtJMPxUOi@comingocluster.joldg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.get_database('Comigo_DB')
    return db