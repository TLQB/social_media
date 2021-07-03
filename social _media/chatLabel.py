
from kivymd.app import MDApp
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton, MDRoundFlatIconButton, MDRaisedButton, MDTextButton, MDIconButton
from kivy.core.window import Window
from kivy.clock import Clock

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
import time
from kivy.clock import Clock
cred = credentials.Certificate("kivydatabase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

callback_done = threading.Event()


Window.size = (300, 600)

Builder.load_file("chatLabel.kv")

bientam = ""
status = ""
name = ""

class Chat(Screen):

    chat_layout = ObjectProperty(None)

    def __init__(self, **kwargs):       
        global status ,bientam
        super().__init__(**kwargs)   
        Clock.schedule_interval(self.send_message,2)  

 

    def recv_message(self):
        global status,bientam,name
        if self.ids.message.text:
            name = self.ids.message.text
            max_width = (self.chat_layout.width - self.chat_layout.spacing - self.chat_layout.padding[0] - \
                        self.chat_layout.padding[2]) * 0.75
            db.collection("User").document("message").set({"message":self.ids.message.text})
            self.chat_layout.add_widget(
                SmoothLabel.create_sized_label(text=self.ids.message.text, max_width=max_width, font_name='Roboto',
                                               font_size=15, pos_hint={'right':1}))
            self.ids.message.text = ""
            self.ids.scroll.scroll_y = 0 
       
    def on_snapshot(col_snapshot, changes, read_time):
        global status,bientam,name
        for doc in col_snapshot:
           print(f'Nội dung: {doc.to_dict()["message"]}')
           bientam = doc.to_dict()["message"]
        callback_done.set() 
    col_query = db.collection("User").document("message")
    query_watch = col_query.on_snapshot(on_snapshot)


    def send_message(self,*args):
        global status,bientam,name
        print()
        if bientam != status and name != bientam :
            print("okkkkkk")
            max_width = (self.chat_layout.width - self.chat_layout.spacing - self.chat_layout.padding[0] - \
                        self.chat_layout.padding[2]) * 0.75
            self.chat_layout.add_widget(
                SmoothLabel.create_sized_label(text=bientam, max_width=max_width, font_name='Roboto',
                                               font_size=15, pos_hint={'left':0}))
            #self.ids.message.text = ""
            self.ids.scroll.scroll_y = 0 
            bientam = status
        else:
            print("koooooooo")

class SmoothLabel(Label):
    def create_sized_label(**kwargs):
        max_width = kwargs.pop('max_width', 0)
        if max_width <= 0:
            return SmoothLabel(**kwargs)
        core_label = CoreLabel(padding=[10,10], **kwargs) 
        core_label.refresh()
        if core_label.width > max_width:

            return SmoothLabel(text_size=(max_width,None), **kwargs)
        else:
            return SmoothLabel(**kwargs)
class MyApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(Chat(name="chat"))
        return self.sm
MyApp().run()