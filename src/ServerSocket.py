from beanie_batteries_queue.queue import asyncio
from MultilayerPerceptron import MultilayerPerceptron
import DatabaseModel
import socket, threading, os, json, platform, gc

gc.enable()

HOST = "0.0.0.0"
PORT = 7228

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

os_type = platform.system()

if   os_type == 'Windows': os.system('cls')
elif os_type == 'Linux'  : os.system('clear')

print(f"\n[-] Server started...")
print(f"[-] {os_type} - {HOST}:{PORT}")

clients, usernames = [], []
database, model = 0x00, 0x00

async def ModelRender():
    
    if (os.path.exists(f'./models/{os_type}/sequential.keras') == False):
         
        database = DatabaseModel
        await database.init()
        
        print('\n[-] Checking database...')
        
        for data_file in os.listdir('./database/data/definitive/'):
            
            json_datas = json.load(open(f'./database/data/definitive/{data_file}'))
             
            for data in json_datas:    
                
                if (data['text'] in f"{await database.findOne('text', data['text'])}"):
                    pass
                else:
                    await database.InsertData(data['id'], data['text'])
         
        print('[-] Check was been completed...\n')
        
        dataset = await database.findAll()
        multilayerPerceptron = MultilayerPerceptron(dataset)
        multilayerPerceptron.build_model(system = os_type, debug = False, log = False)
      
    return MultilayerPerceptron.load_model(f'./models/{os_type}/sequential.keras')

model = asyncio.run(ModelRender())
print("\n[-] Waiting for client request...")

def handleMessages(client, username):
    
    while True:

        try:
            message_status = False
            question_status = False
            seed_text = client.recv(1024).decode()
            size_predict = int(client.recv(1024).decode())

            if (seed_text.__eq__('exit') != True):
                
                with open('./database/data/black-list/list.txt') as black_list:
                    for word in black_list:
                        word = word.strip()
                        if (str(seed_text).find(str(word)) != -1):
                            client.send("Desculpe! Mas de acordo com minhas diretrizes, não posso realizar nenhuma tarefa deste tipo.".encode())
                            break
                        else:
                            message_status = True
                
                with open('./database/data/greetings/greetings.txt') as list:
                    for word in list:
                        word = word.strip()
                        if(str(seed_text).find(str(word)) != -1):
                            client.send("Olá, sou a Assistente Luna, é um prazer ter você aqui. Qual sua dúvida?".encode())
                            break
                        else:
                            message_status = True 
                 
                for file in os.listdir('./database/data/definitive/'):
                    if (question_status == True):
                        break
                    with open(f'./database/data/definitive/{file}') as questions:
                        for question in questions:
                            
                            question = question.strip()
                            question = question.lower()
                            seed_text = seed_text.lower()
                              
                            for word in seed_text.split():
                                if(question.find(word) != -1):
                                    question_status = True
                                    break
                                else:
                                    question_status = False
                
                if (question_status == False):
                    client.send("Infelizmente não posso processar mensagens deste tipo. Que tal tentar novamente?".encode())
                elif (message_status == True and question_status == True):
                    print(f'\n[-] {username}: seed text ({seed_text}), size of predict ({size_predict})')                
                    predict = MultilayerPerceptron.predict_text(seed_text, int(20), model)
                    print(f'[-] predict: {predict}')
                    client.send(f'{predict}'.encode()) 
            
            else:
                client.close()
                usernames.remove(username)

                print(f'\n\n[-] User {username} left the server...\n')
                break
        
        except Exception as exception:

            client.close()
            usernames.remove(username)
            
            print(exception)
            print(f'\n\n[-] User {username} left the server...\n')
            break
   
def initialConnection():

    while True:
        
        client, address = server.accept()

        print(f'\n[-] New Connection: {str(address)}')
        clients.append(client)
        
        username = f"C{address[1]}"
        usernames.append(username)
        client.send("Handshake".encode())

        user_thread = threading.Thread(target=handleMessages, args=(client, username))
        user_thread.start()
   
initialConnection()
