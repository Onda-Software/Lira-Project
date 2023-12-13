import socket, threading, os, sys, json
from MongoDatabaseConnection import MongoDatabaseConnection
from TextCompletionModel import TextCompletionModel

LOCALHOST = "0.0.0.0"
PORT = 3001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCALHOST, PORT))
server.listen()

os.system('clear')
print("\nServer started")
print("Waiting for client request...")

arg = sys.argv[1:]
model = 0x00
database = 0x00

if(arg[0] == "windows"):

    if(os.path.exists('./models/windows/sequential.keras') == False):
        
        database = MongoDatabaseConnection('test_database', 'test_collection')
        database.connect()
        
        json_datas = json.load(open('./database/data/data.json'))
        #client.insert(json_datas)
        
        dataset = database.get_datas()
        textCompletionModel = TextCompletionModel(dataset)
        textCompletionModel.build_model(system="windows" ,debug=False, log=False)

    model = TextCompletionModel.load_model('./models/windows/sequential.keras')

elif(arg[0] == "unix"):
    
    if(os.path.exists('./models/unix/sequential.keras') == False):
        
        client = MongoDatabaseConnection('test_database', 'test_collection')
        client.connect()

        json_datas = json.load(open('./database/data/data.json'))
        #client.insert(json_datas)
        
        dataset = client.get_datas()
        textCompletionModel = TextCompletionModel(dataset)
        textCompletionModel.build_model(system="unix" ,debug=False, log=True)

    model = TextCompletionModel.load_model('./models/unix/sequential.keras')

clients = []
usernames = []

def handleMessages(client, username):
    
    while True:
        try:

            seed_text = client.recv(1024).decode()
            size_predict = client.recv(1024).decode()
            
            print(f'\n{usernames[usernames.index(username)]}: seed text ({seed_text}), size of predict ({size_predict})')

            predict = TextCompletionModel.predict_text(seed_text, int(size_predict), model)

            client.send(f'{predict}'.encode())

        except Exception as e:
            print(e)
            clientLeaved = clients.index(client)
            client.close()

            clients.remove(clients[clientLeaved])
            clientsLeavedUsername = usernames[clientLeaved]

            print(f'\nUser {clientsLeavedUsername} left the server...\n')
            usernames.remove(clientsLeavedUsername)

def initialConnection():

    while True:
        try:
            
            client, address = server.accept()

            print(f'\nNew Connection: {str(address)}')
            clients.append(client)

            username = f"C{address[1]}"
            usernames.append(username)
            client.send("Welcome!".encode())

            user_thread = threading.Thread(target=handleMessages, args=(client, username))
            user_thread.start()

        except:
            pass

initialConnection()
