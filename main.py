from src.database import MongoDatabase
from src.model import TextCompletionModel
from json import load
import sys
import os

if __name__ == "__main__":

    client = MongoDatabase('test_database', 'test_collection')
    client.connect()

    json_datas = load(open('./database/data/data.json'))
    #client.insert(json_datas)

    dataset = MongoDatabase.get_datas(client)
    textCompletionModel = TextCompletionModel(dataset)

    arg = sys.argv[1:]
    model = 0x00
    
    if(arg[0] == "windows"):

        if(os.path.exists('./models/windows/sequential.keras') == False):
    
            textCompletionModel.build_model(debug=False, log=False)
        
        model = textCompletionModel.load_model('./models/windows/sequential.keras')
    
    elif(arg[0] == "unix"):
        
        if(os.path.exists('./models/unix/sequential.keras') == False):

            textCompletionModel.build_model(debug=False, log=False)
        
        model = textCompletionModel.load_model('./models/unix/sequential.keras')

 
    while True:
        
        print("\n=================================================================")

        text_predict = str(input("Please enter a pre text for predict: "))
        
        if(text_predict == "exit()"):
            break
        
        size_predict = int(input("Plese enter with a size for predict: "))
        generated_text = textCompletionModel.predict_text(text_predict, size_predict, model)
        print(f"\nPredicted text is: {generated_text}")

        print("=================================================================\n")

