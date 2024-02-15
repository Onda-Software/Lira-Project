from kivy.utils import platform
import socket, threading
from kivymd.app import Builder, MDApp
from kivymd.theming import Window
from kivymd.uix.button.button import MDLabel, MDRectangleFlatButton
from kivymd.uix.screen import Screen

SERVER_IP = "127.0.0.1"
PORT = 7123

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class OutlinedLabel(MDLabel): pass

class MainApp(MDApp):
    
    def build(self):

        if(platform == 'android' or platform == 'ios'):
            Window.maximize()
        else:
            Window.size = (600, 800)
        
        screen = Screen()

        self.label  = Builder.load_file('./src/style/Label.kv')
        self.input  = Builder.load_file('./src/style/TextField.kv')
        self.button = MDRectangleFlatButton(
            text = ">",
            text_color = (0, 0, 0, 1),
            line_color = (0, 0, 0, 1), 
            line_width = 1.12,
            md_bg_color= (0.5, 0.5, 1, 1),
            pos_hint = {"center_x": 0.9,"center_y": 0.1},
            on_release = self.sendMessage
        )
        
        screen.add_widget(self.label)
        screen.add_widget(self.input)
        screen.add_widget(self.button)
        
        self.connect(None)
        return screen

    def connect(self, none=None): 
        client.connect((SERVER_IP, PORT))
        self.label.text = "Connected to Server"
        client.recv(1024).decode()
    
    def sendMessage(self, none=None):
     
        seed_text = self.input.text
        
        client.send(f'{seed_text}'.encode()) 
        size_predict = int(3)
        client.send(f'{size_predict}'.encode())

        self.label.text = client.recv(1024).decode()
    
def startThreads(): threading.Thread(target=MainApp().run()).start()
