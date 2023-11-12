from database import MongoDatabase
from model import TextCompletionModel
from json import load
import os

if __name__ == "__main__":

    client = MongoDatabase('test_database', 'test_collection')
    client.connect()

    json_datas = load(open('../database/data/data.json'))
    client.insert(json_datas)

    dataset = MongoDatabase.get_datas(client)
    textCompletionModel = TextCompletionModel(dataset)

    while True:

        if(os.path.exists('./models/sequential.keras') == False):
        
            textCompletionModel.build_model(debug=False, log=False)
        
        else:
            
            model = textCompletionModel.load_model('./models/sequential.keras')
     
            while True:
                
                print("\n=================================================================")

                text_predict = str(input("Please enter a pre text for predict: "))
                size_predict = int(input("Plese enter with a size for predict: "))
                generated_text = textCompletionModel.predict_text(text_predict, size_predict, model)
                print(f"\nPredicted text is: {generated_text}")

                print("=================================================================\n")
