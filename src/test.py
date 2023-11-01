from database import MongoDatabase

if __name__ == "__main__":

    client = MongoDatabase('test_database', 'test_collection')
    database, collection = client.connect()

    print(f"\nDatabase: {database}")
    print(f"\nCollection: {collection}\n")

    data = [{'id': 1, 'text': 'test'}, {'id': 2, 'text': 'test'}]
 
    MongoDatabase.insert(data)

    datas = MongoDatabase.get_datas()
    for data in datas:
        print(data['text'])

