from kivy.uix.boxlayout import BoxLayout
from kivymd.app import Builder, MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton

seed_text = '''

MDTextField:
    hint_text: "Seed Text "
    helper_text: "Enter with a pre text for predict"
    helper_text_mode: "on_focus"
    icon_right: "message"
    icon_right_color: app.theme_cls.primary_color
    pos_hint:{'center_x': 0.5, 'center_y': 0.5}
    size_hint_x:None
    width:300

'''

class MainApp(MDApp):

    def build(self):

        screen = Screen()
         
        self.input = Builder.load_string(seed_text)
        button = MDRectangleFlatButton(text=">", pos_hint={"center_x": 0.5,"center_y": 0.4}, on_release=self.print_text)
        
        screen.add_widget(self.input)
        screen.add_widget(button)

        return screen

    def print_text(self, none):
        print(self.input.text)

MainApp().run()
