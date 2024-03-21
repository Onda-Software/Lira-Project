from beanie_batteries_queue.queue import asyncio
from MultilayerPerceptron import MultilayerPerceptron
import DatabaseModel
import socket, threading, os, json, platform, gc

gc.enable()

HOST = "127.0.0.1"
PORT = 7222

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

os_type = platform.system()

if   os_type == 'Windows': os.system('clear-host')
elif os_type == 'Linux'  : os.system('clear')

print(f"\nServer started...")
print(f"{os_type} - {HOST}:{PORT}")

clients, usernames = [], []
database, model = 0x00, 0x00

async def ModelRender():
    
    if (os.path.exists(f'./models/{os_type}/sequential.keras') == False):
         
        database = DatabaseModel
        await database.init()
        
        print('\nChecking database...')
        
        for data_file in os.listdir('./database/data/'):
            
            json_datas = json.load(open(f'./database/data/{data_file}'))
             
            for data in json_datas:    
                
                if (data['text'] in f"{await database.findOne('text', data['text'])}"):
                    pass
                else:
                    await database.InsertData(data['id'], data['text'])
        
        print('Insertion was been completed...\n')
        
        dataset = await database.findAll()
        multilayerPerceptron = MultilayerPerceptron(dataset)
        multilayerPerceptron.build_model(system = os_type, debug = False, log = False)
      
    return MultilayerPerceptron.load_model(f'./models/{os_type}/sequential.keras')

model = asyncio.run(ModelRender())
print("\nWaiting for client request...")

def handleMessages(client, username):
    
    while True:

        try:
            
            seed_text = client.recv(1024).decode()
            size_predict = int(client.recv(1024).decode())

            if (seed_text.__eq__('exit') != True and seed_text.__eq__('') != True):
                
                print(f'\n{username}: seed text ({seed_text}), size of predict ({size_predict})')                
                predict = MultilayerPerceptron.predict_text(seed_text, int(size_predict), model)
                client.send(f'{predict}'.encode())
             
            else:
                client.close()
                usernames.remove(username)

                print(f'\n\nUser {username} left the server...\n')
                break
        
        except Exception as exception:

            client.close()
            usernames.remove(username)
            
            print(exception)
            print(f'\n\nUser {username} left the server...\n')
            break
   
def initialConnection():

    while True:
        
        client, address = server.accept()

        print(f'\nNew Connection: {str(address)}')
        clients.append(client)
        
        username = f"C{address[1]}"
        usernames.append(username)
        client.send("Welcome!".encode())

        user_thread = threading.Thread(target=handleMessages, args=(client, username))
        user_thread.start()
   
initialConnection()
