import json, asyncio
import DatabaseModel

datas = json.load(open('./database/data/minimalist.json'))

async def main(): 
    
    database = DatabaseModel
    await database.init()
    
    for data in datas:
        await database.InsertData(data['key'], data['text'])
    
async def run():
    
    database = DatabaseModel
    await database.init()
    
    dataset = await database.findAll()
    for data in dataset:
        print(data.text)
    
asyncio.run(run())
