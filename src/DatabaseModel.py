from beanie import Document, init_beanie
from beanie_batteries_queue import Task
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import pymongo
from typing import Optional

class Category(BaseModel):
    name: str
    description: Optional[str] = None

class DataDocument(Document):
    key: str
    text: str
    category: Optional[Category] = None
    
    class Settings:
        
        name = "dataset"
        
        use_cache = True
        use_revision = True
        use_state_management = True
        state_management_previus = True
        validate_on_save = True

        indexes = [
            [
                ("key", pymongo.TEXT),
                ("text", pymongo.TEXT),
            ],
        ]

async def init():

    global client 
    client = AsyncIOMotorClient(
        "mongodb://localhost:27017"
    )
    
    await init_beanie(
        database = client.test,
        document_models = [
            DataDocument,
        ],
    )
    
async def InsertData(key, text):
     
    if(key == '' or text == ''):
        raise ValueError 

    data = DataDocument(key = key, text = text)

    await DataDocument.insert_one(data)
 
async def findAll():
    
    datas = []

    async for data in DataDocument.find():

        datas.append(data)
    
    return datas

async def findOne(field, index):
    return await DataDocument.find({field: index}).to_list()
    
class runner(Task):

    async def init_call(self, task):

        await task.push()

        async for task in task.queue():
            await task.finish()
            break
