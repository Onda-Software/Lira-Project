import gc, sys, unittest

gc.enable()
sys.path.append('./src/')
from DatabaseModel import init
from DatabaseModel import InsertData
from DatabaseModel import findAll
from DatabaseModel import findOne

class DatabaseModelTest(unittest.IsolatedAsyncioTestCase):

    async def test_init(self):
        self.assertEqual(True, await init())
    
    async def test_InsertData(self):
        await init()
        self.assertEqual(True, await InsertData('1', 'test')) 

    async def test_findAll(self):
        await init()
        self.assertNotEqual([], await findAll())
       
    async def test_findOne(self):
        await init()
        self.assertNotEqual([], await findOne('1', 'test'))
    
if __name__ == '__main__':
    unittest.main()
