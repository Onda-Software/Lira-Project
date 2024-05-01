import socket, threading
from time import sleep
from kivy.utils import platform
from kivymd.theming import Window
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

SERVER_IP = "127.0.0.1"
PORT = 7229

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Gerenciador(ScreenManager): 
    pass

class TelaInicio(Screen): 
    pass

class TelaInfo(Screen):
    pass

class TelaChat(Screen):
 
    def addComent(self):
        
        input = self.ids.texto.text
        caixa_comentario = CaixaComentario(text=input)

        client.send(f'{input}'.encode())
        sleep(0.5)
        client.send(f'{int(18)}'.encode())

        predict = client.recv(1024).decode()

        self.ids.caixa_texto.add_widget(Widget(size_hint_y=None, height=10))
        self.ids.caixa_texto.add_widget(caixa_comentario)
        self.ids.caixa_texto.add_widget(Widget(size_hint_y=None, height=15))
        self.ids.caixa_texto.add_widget(CaixaComentarioLuna(predict))

        caixa_comentario.altera_tamanho_caixa()
        self.ids.texto.text = ''
    
class CaixaComentario(BoxLayout):
    
    def __init__(self, text = '', **kwargs):
        super(CaixaComentario, self).__init__(**kwargs)
        self.ids.resposta_dinamica.text = text
        self.padding = [30, 10]
        self.ids.resposta_dinamica.bind(texture_size=self._update_height)
    
    def altera_tamanho_caixa(self):
        label = self.ids.resposta_dinamica
        label.text_size = (label.width - 2 * label.padding[0], None)
    
    def _update_height(self, instance, size):
        min_height = 50 
        self.height = size[1] + self.padding[1] * 2
    
class CaixaComentarioLuna(BoxLayout):

    def __init__(self, text):
        super(CaixaComentarioLuna, self).__init__()
        self.ids.resposta_dinamica.text = text
        self.padding = [30, 10]
        self.ids.resposta_dinamica.bind(texture_size=self._update_height)
    
    def altera_tamanho_caixa(self):
        label = self.ids.resposta_dinamica
        label.text_size = (label.width - 2 * label.padding[0], None)        
    
    def _update_height(self, instance, size):
        min_height = 50
        self.height = size[1] + self.padding[1] * 2
    
class Principal(App):

    def build(self):

        if(platform == 'android' or platform == 'ios'):
            Window.maximize()
         
        Window.clearcolor = 169/255, 169/255, 169/255, 0/255    
        self.connect()
        return Gerenciador()
    
    def connect(self): 
        client.connect((SERVER_IP, PORT))
        client.recv(1024).decode()
    
def startThreads(): threading.Thread(target=Principal().run()).start()
