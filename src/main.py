from database import MongoDatabase
from model import TextCompletionModel
from json import load
import os

if __name__ == "__main__":

    client = MongoDatabase('test_database', 'test_database')
    client.connect()

    json_datas = load(open('../database/data/data.json'))
    #client.insert(json_datas)

    dataset = MongoDatabase.get_datas(client)
    textCompletionModel = TextCompletionModel(dataset)

    while True:

        if(os.path.exists('./models/sequential.keras') == False):
        
            textCompletionModel.build_model()
        
        else:
            
            while True:
   
                model = textCompletionModel.load_model('./models/sequential.keras')
     
                text_predict = str(input("\nPlease enter a pre text for predict: "))
                size_predict = int(input("Plese enter with a size for predict: "))
                generated_text = textCompletionModel.predict_text(text_predict, size_predict, model)
                print(f"\nPredicted text is: {generated_text}\n")

