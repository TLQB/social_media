from kivy.app import App 
from kivy.lang import Builder 
import requests
from kivy.uix.screenmanager import Screen,ScreenManager
import time
import pyrebase 
from kivy.clock import Clock

config = {
    "apiKey": "AIzaSyActuACAwT6Z5h2ozQ3U2Mz8ipoX42sjYc",
    "authDomain": "playchat-386e6.firebaseapp.com",
    #"databaseURL":"http://playchat-386e6.firebaseapp.com/",
    "databaseURL":"https://playchat-386e6-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "playchat-386e6",
    "storageBucket": "playchat-386e6.appspot.com",
    "messagingSenderId": "668971008979",
    "appId": "1:668971008979:web:aef3dbc43cfcd83300e526",
    "measurementId": "G-RV9QYHXX53"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

name = "Quy Bao : "
Builder.load_file("message.kv")
#requests.delete("https://playchat-386e6-default-rtdb.asia-southeast1.firebasedatabase.app/.json")
db.child("biendem").set({"stt":0})
bientam = ""
status =""

class Mess1(Screen):

	firebase = pyrebase.initialize_app(config)
	db = firebase.database()
	def q(self):
		
		print("ppppp")
		self.my_stream.close()
	def stream_handler(message):	
		global bientam,status
		print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}	
		bientam = message["data"]

	
	my_stream = db.child("message").child("message").stream(stream_handler)


	def thu(self):
		global name
		#print(self.ids['textct'].text)
		data = self.ids['textct'].text
		db.child("message").set({"message":str(name)+str(data)})


		
		if data != "":
		
			#self.ids['content'].text = self.ids['content'].text + "\n" + self.ids['textct'].text 
			self.ids['textct'].text = ""
	def update(self,*args):
		global bientam,status
		if bientam != status   :
			datamessage = self.ids['content'].text + "\n"  + str(bientam)
			self.ids['content'].text =  datamessage
			

			bientam = status
		else:
			print("no")


	def __init__(self, **kwargs):       
		global status 
		super().__init__(**kwargs)
		
		Clock.schedule_interval(self.update,2)
		

class Mess2(Screen):
	pass

class testMessage(App):

	def build(self):
		sm = ScreenManager()
		sm.add_widget(Mess1(name = "mess1"))
		sm.add_widget(Mess2(name = "mess2"))


		return sm 
	def on_request_close(self, *args):
		
		return True


testMessage().run()