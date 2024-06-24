import os

text = "o tigrinho ta pagando sql?"
count = 0

for file in os.listdir('./database/data/definitive/'):
    with open(f'./database/data/definitive/{file}') as questions:
        for question in questions:

            question = question.strip()
            question = question.lower()
            text = text.lower()
            
            if (count != 3):
                for word in text.split():
                    
                    if(question.find(word) != -1):
                        count += 1
                        print("ok")
            else:
                break

if (count == 3):
    print("bingo")
