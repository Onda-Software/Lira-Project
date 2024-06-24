import os

text = "teste de letras"

for file in os.listdir('./database/data/definitive/'):
    with open(f'./database/data/definitive/{file}') as questions:
        for question in questions:

            question = question.strip()
            question = question.lower()
            text = text.lower()

            for word in text.split():
                print(question.find(word))
                if(question.find(word) != -1):
                    print("ok")
