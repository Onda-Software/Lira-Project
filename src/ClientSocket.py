import socket, threading
from time import sleep
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

SERVER_IP = "0.0.0.0" 
#"18.228.155.29"
PORT = 7228

class RoundedTextInput(TextInput):
    pass

class Gerenciador(ScreenManager): 
    pass

class TelaInicio(Screen): 
    pass

class TelaChat(Screen):
     
    def __init__(self, **kwargs):
        super(TelaChat, self).__init__(**kwargs)
     
    def addComent(self, *args):
        
        connection_status = False
        session = None
        prdict = ''
        input = self.ids.texto.text
        caixa_comentario = CaixaComentario(text=input)
        
        try:
            session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            session.connect((SERVER_IP, PORT))
            session.recv(1024).decode()  

            self.ids.caixa_texto.add_widget(Widget(size_hint_y=None, height=10))
            self.ids.caixa_texto.add_widget(caixa_comentario)
            #self.ids.caixa_texto.add_widget(CaixaComentarioLuna("Carregando resposta..."))
            session.send(f'{input}'.encode())
            sleep(0.5)
            session.send(f'{int(12)}'.encode())
            predict = session.recv(1024).decode()
              
            self.ids.caixa_texto.add_widget(Widget(size_hint_y=None, height=15))
            caixa_comentario_luna = CaixaComentarioLuna(predict)
            self.ids.caixa_texto.add_widget(caixa_comentario_luna)
            caixa_comentario.altera_tamanho_caixa()
            self.ids.texto.text = ''
             
            session.close()
        except Exception as _:
            try:
                raise ConnectionRefusedError
            except ConnectionRefusedError as _:
                access_message = CaixaComentarioLuna("Não posso responder no momento. Verifique sua conexão com a internet e tente novamente...")
                self.ids.caixa_texto.add_widget(Widget(size_hint_y=None, height=10))
                self.ids.caixa_texto.add_widget(access_message)
                access_message.altera_tamanho_caixa()
                self.ids.texto.text = ''
    
    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)
        return super(TelaChat, self).on_pre_enter(*args)
    
    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'telainicio'
            return True    

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

    def __init__(self, text = ''):
        super(CaixaComentarioLuna, self).__init__()
        self.ids.resposta_dinamica.text = ''
        self.padding = [30, 10]
        self.ids.resposta_dinamica.bind(texture_size=self._update_height)

        self.full_text = text
        self.current_index = 0
        Clock.schedule_interval(self.type_text, 0.02)
    
    def type_text(self, dt):
        if self.current_index < len(self.full_text):
            self.ids.resposta_dinamica.text += self.full_text[self.current_index]
            self.current_index += 1
            self.altera_tamanho_caixa()
        else:
            return False
    
    def altera_tamanho_caixa(self):
        label = self.ids.resposta_dinamica
        label.text_size = (label.width - 2 * label.padding[0], None)        
    
    def _update_height(self, instance, size):
        min_height = 50
        self.height = size[1] + self.padding[1] * 2
    
class TelaInfo(Screen):

    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)
        return super(TelaInfo, self).on_pre_enter(*args)
    
    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'telainicio'
            return True
    
class Principal(App):

    def build(self):
    	
        Window.clearcolor = 220/255, 220/255, 220/255
        return Gerenciador()
    
    def on_focus(self, instance, value):
        if value:  # Quando o TextInput recebe foco (teclado aparece)
            Window.bind(on_keyboard=self.adjust_layout)
        else:  # Quando o TextInput perde foco (teclado desaparece)
            Window.unbind(on_keyboard=self.adjust_layout)
            self.reset_layout()
    
    def adjust_layout(self, window, key, *args):
        if key == 27:  # Tecla "ESC" ou "Back" no Android
            self.reset_layout()
        else:
            # Ajuste o layout para evitar que o teclado tampe o TextInput
            self.root.y = -self.root.ids.texto.height
    
    def reset_layout(self):
        self.root.y = 0
    
def startThreads(): threading.Thread(target=Principal().run()).start()
