import pymongo

class MongoDatabaseConnection:
    
    def __init__(self, db_name: str, collection_name: str) -> None:
        self.db_name = db_name
        self.collection_name = collection_name
    
    def connect(self):
        
        global client
        client = pymongo.MongoClient()

        if(client):
            global connect_state
            connect_state = True
        else:
            raise ConnectionError
        
        global database
        database = client[self.db_name]

        global collection
        collection = database[self.collection_name]

        return database, collection

    def insert(self, data):
        
        if(connect_state != True):
            raise ConnectionError
        
        if(data == "" or data == None):
            raise ValueError
        
        return collection.insert_many(data)

    def get_datas(self):
        
        datas = []

        for data in collection.find():
            datas.append(data)
         
        return datas
