import pyautogui, socket, threading
from time import sleep
from kivy.utils import platform
from kivymd.theming import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

SERVER_IP = "0.0.0.0"
PORT = 7229

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Gerenciador(ScreenManager): 
    pass

class TelaInicio(Screen): 
    pass

class TelaChat(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def sendMessage(self):
        
        input = self.ids.texto.text
        
        client.send(f'{input}'.encode())
        sleep(0.5)
        client.send(f'{int(18)}'.encode())

        predict = client.recv(1024).decode()

        self.ids.caixa_texto.add_widget(CaixaComentario(text=predict))
        self.ids.texto.text = ''
    
class CaixaComentario(BoxLayout):
    def __init__(self, text = '', **kwarg):
        super(CaixaComentario, self).__init__(**kwarg)
        self.ids.resposta_dinamica.text = text
    
class TelaInfo(Screen):
    pass

class Principal(App):

    def build(self):

        if(platform == 'android' or platform == 'ios'):
            Window.maximize()
        else:
            
            screen_width, screen_height = pyautogui.size()

            Window.size = (600, 800)
            Window.left = int((screen_width - Window.width) / 2)
            Window.top = int((screen_height - Window.height) / 2)
        
        self.connect()
        return Gerenciador()
    
    def connect(self): 
        client.connect((SERVER_IP, PORT))
        client.recv(1024).decode()
    
def startThreads(): threading.Thread(target=Principal().run()).start()
