import socket, threading, os, time

SERVER_IP = "0.0.0.0"
PORT = 3001

os.system('clear')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = ""

try:
    client.connect((SERVER_IP, PORT))
    print("\nConnected to server!")
except:
    print(f'ERROR: Please review your input: {SERVER_IP}:{PORT}')

def recvMessage():

    while True:
        generated_text = client.recv(1024).decode()
        print(f'\n> {generated_text}\n')

def sendMessage():

    while True:
        
        time.sleep(1)

        print("=================================================================")
        
        text_predict = str(input("Please enter a pre text for predict: "))
        
        if(text_predict == "exit"):
            client.send("exit".encode())
            time.sleep(0.5)
            client.send(f'{0}'.encode())
            client.close()
            os._exit(0)
        else:
            client.send(f'{text_predict}'.encode())
        
        size_predict = int(input("Plese enter with a size for predict: "))
        client.send(f'{size_predict}'.encode())

recvThread = threading.Thread(target=recvMessage, args=())
sendThread = threading.Thread(target=sendMessage, args=())

def startThreads():
    recvThread.start()
    sendThread.start()
