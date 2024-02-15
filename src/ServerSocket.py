import socket, threading, os, json, platform
from MongoDatabaseConnection import MongoDatabaseConnection
from TextCompletionModel import TextCompletionModel

HOST = "127.0.0.1"
PORT = 7123

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

os_type = platform.system()

if (os_type == 'Windows'):
    os.system('clear-host')
elif (os_type == 'Linux'):
    os.system('clear')

print(f"\nServer started...")
print(f"{os_type} - {HOST}:{PORT}")
print("\nWaiting for client request...")

clients, usernames = [], []
database, model = 0x00, 0x00

if (os_type == "Windows"):

    if (os.path.exists('./models/windows/sequential.keras') == False):
        
        database = MongoDatabaseConnection('test_database', 'test_collection')
        database.connect()
        
        json_datas = json.load(open('./database/data/data.json'))
        database.insert(json_datas)
        
        dataset = database.get_datas()
        textCompletionModel = TextCompletionModel(dataset)
        textCompletionModel.build_model(system="windows", debug = False, log = False)
    
    model = TextCompletionModel.load_model('./models/windows/sequential.keras')
    
elif (os_type == "Linux"):
    
    if (os.path.exists('./models/unix/sequential.keras') == False):
        
        database = MongoDatabaseConnection('test_database', 'test_collection')
        database.connect()

        json_datas = json.load(open('./database/data/data.json'))
        database.insert(json_datas)
        
        dataset = database.get_datas()
        textCompletionModel = TextCompletionModel(dataset)
        textCompletionModel.build_model(system = "unix", debug = False, log = True)
    
    model = TextCompletionModel.load_model('./models/unix/sequential.keras')

def handleMessages(client, username):
    
    while True:
        try:
            
            print('Waiting for a message...')
            seed_text = client.recv(1024).decode()
            size_predict = client.recv(1024).decode()
            
            if (seed_text.__eq__('exit') != True and seed_text.__eq__('') != True):
                
                print(f'\n{username}: seed text ({seed_text}), size of predict ({size_predict})')                
                predict = TextCompletionModel.predict_text(seed_text, int(size_predict), model)
                print()
                client.send(f'{predict}'.encode())
                
            else:
                client.close()
                usernames.remove(username)

                print(f'\nUser {username} left the server...\n')
                break
            
        except Exception as exception:

            client.close()
            usernames.remove(username)
            
            print(exception)
            print(f'\nUser {username} left the server...\n')
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
