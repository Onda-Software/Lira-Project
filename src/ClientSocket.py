import socket, threading, os, time
from kivymd.app import Builder, MDApp
from kivymd.uix.button.button import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton

SERVER_IP = "0.0.0.0"
PORT = 3000

#os.system('clear')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class OutlinedLabel(MDLabel):
    pass

class MainApp(MDApp):

    def build(self):
        
        screen = Screen()

        self.label = Builder.load_file('./src/style/Label.kv')
        self.input = Builder.load_file('./src/style/TextField.kv')
        button = MDRectangleFlatButton(
            text=">",
            pos_hint={"center_x": 0.5,"center_y": 0.4},
            on_release=self.sendMessage
        )
        
        screen.add_widget(self.label)
        screen.add_widget(self.input)
        screen.add_widget(button)

        self.connect(None)
        return screen

    def connect(self, none=None):
        
        try:
            client.connect((SERVER_IP, PORT))
            self.label.text = "Connected to Server"
            client.recv(1024).decode()
        except Exception as exception:
            print(f'ERROR: Please review your input: {SERVER_IP}:{PORT}')
            print(exception)

    def sendMessage(self, none=None):
    
        seed_text = self.input.text
        
        if(seed_text == "exit"):
            client.send("exit".encode())
            time.sleep(0.5)
            client.send(f'{0}'.encode())
            client.close()
            os.system('clear')
            os._exit(0)
        else:
            client.send(f'{seed_text}'.encode()) 
            size_predict = int(3)
            time.sleep(0.5)
            client.send(f'{size_predict}'.encode())

        time.sleep(1)
        self.label.text = client.recv(1024).decode()

def startThreads():
    threading.Thread(target=MainApp().run()).start()
