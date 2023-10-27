import pymongo

client = pymongo.MongoClient()

db = client['test']
collection = db['test_collection']

data_to_insert = [
    {"id": 1, "text": "test"}
]

result  = collection.insert_many(data_to_insert)
print(result.inserted_ids)

for data in collection.find():
    print(data)

