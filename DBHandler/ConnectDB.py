import pymongo

def DBConnction():
    CONNECTION_STRING = "---------------------------------"
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.get_database('Comigo_DB')
    return db
