import kivymd_extensions.akivymd
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog
import pyrebase
from validate_email import validate_email
import time
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
import threading
from kivymd.toast import toast
from kivymd.uix.card import MDCard


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
import time
from kivy.clock import Clock
cred = credentials.Certificate("playChat.json")
firebase_admin.initialize_app(cred)
dbstore = firestore.client()
Builder.load_file("message.kv")
callback_done = threading.Event()
tn = dbstore.collection("User").document("message").get()
print(tn.to_dict())

bientam = ""
status = ""
name = ""

duli = dbstore.collection("User").document("datamessage").get()
duli = duli.to_dict()
duli = duli["dt"]
print(duli)
print("###################################")

Window.size = (320, 620)

config = {
    "apiKey": "AIzaSyActuACAwT6Z5h2ozQ3U2Mz8ipoX42sjYc",
    "authDomain": "playchat-386e6.firebaseapp.com",
    #"databaseURL":"http://playchat-386e6.firebaseapp.com",
    "databaseURL":"https://playchat-386e6-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "playchat-386e6",
    "storageBucket": "playchat-386e6.appspot.com",
    "messagingSenderId": "668971008979",
    "appId": "1:668971008979:web:aef3dbc43cfcd83300e526",
    "measurementId": "G-RV9QYHXX53"
  }


firebase = pyrebase.initialize_app(config)
auth= firebase.auth()
db = firebase.database()
Builder.load_file("social_media.kv")
sex_info=""
name_info=""
email_info=""
i= 0
class Login(Screen):
    def checkLogin(self):
        global sex_info,name_info,email_info,name
        email = self.ids["email_login"].text
        password = self.ids["password_login"].text

        try:
            user = auth.sign_in_with_email_and_password(email,password)
            info = db.child("Users").child("ID :"+ user["localId"]).get()
            info = info.val()
            sex_info = info["Sex"]
            email_info = info["email"]
            name_info = info["name"]
            name = info["name"]+" : "
            print(sex_info,name_info,name_info)
            Id = auth.get_account_info(user['idToken'])
            emailVerified = Id['users'][0]['emailVerified']
            print(emailVerified)
            if emailVerified:
                self.manager.current = "onb"
            else:
                self.ids["error"].text = "Tai khoan email chua duoc xac thuc!"

        except:
            self.ids["error"].text = "Email hoac mat khau chua dung!"
class Signup(Screen):
    def success(self):
        dialog = AKAlertDialog(
            header_icon="check-circle-outline", header_bg=[0, 0.7, 0, 1]
        )
        content = Factory.SuccessDialog()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()
    def checkSignup(self):
        email = self.ids["email_signup"].text
        password  = self.ids["password_signup"].text
        passwordR = self.ids["password_signupR"].text
        username = self.ids["username"].text 
        if self.ids["sexMan"].active == True:
            self.sex = "Man"
        else:
            self.sex = "Girl"

        if (validate_email(email)):
            if len(password)>7:

                if str(password)==str(passwordR):
                    try:
                        user = auth.create_user_with_email_and_password(email,passwordR)
                        db.child("Users").child("ID :"+ user["localId"]).set({"name":username,"Sex":self.sex,"email":email})
                        self.ids["error_signup"].text = "Tao tai khoan thanh cong! "
                        auth.send_email_verification(user['idToken'])
                        self.success()
                        time.sleep(1)
                        self.manager.current = "login"
                    except:
                        self.ids["error_signup"].text = "Tai khoan da co nguoi dung!"
                else:
                    self.ids["error_signup"].text = "Password chua khop!"
            else:
                self.ids["error_signup"].text = "Password khong it hon 8 ki tu!"
        else:
            self.ids["error_signup"].text = "Email khong hop le!"

class ForgetPassword(Screen):
    def checkForgetpass(self):
        email = self.ids["email_forget"].text
        try:
            auth.send_password_reset_email(email)
            self.ids["fg"].text = "Vui long check mail reset password"
            time.sleep(2)
            self.manager.current = "login"
        except:
            self.ids["fg"].text = "Vui long check lai mail"
class Onboarding(Screen):
    def finish_callback(self):
        self.manager.current ="main"


class Loadercard(MDCard):
    pass



class Main(Screen):


    def get_date(self):
        t = threading.Thread(target=self.send_request)
        t.start()

    def set_user1(self, *args):
        user1 = args[1]
        self.ids.user1.avatar = "https://cdn3.iconfinder.com/data/icons/generic-avatars/128/avatar_portrait_man_male_hipster_beard_2-512.png"
        self.ids.user1.name = user1["name"]
        self.ids.user1.email = user1["email"]
        self.ids.user1.website = user1["website"]

    def set_user2(self, *args):
        user2 = args[1]
        self.ids.user2.name = user2["name"]
        self.ids.user2.email = user2["email"]
        self.ids.user2.website = user2["website"]
        self.ids.user2.avatar = "https://cdn4.iconfinder.com/data/icons/avatars-21/512/avatar-circle-human-male-3-512.png"

    def set_user3(self, *args):
        user3 = args[1]
        self.ids.user3.name = user3["name"]
        self.ids.user3.email = user3["email"]
        self.ids.user3.website = user3["website"]
        self.ids.user3.avatar = "https://cdn2.iconfinder.com/data/icons/avatars-60/5985/17-Cashier-256.png"

    def set_user4(self, *args):
        user4 = args[1]
        self.ids.user4.name = user4["name"]
        self.ids.user4.email = user4["email"]
        self.ids.user4.website = user4["website"]
        self.ids.user4.avatar = "https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/man_adult_mustache_people_woman_father_avatar-256.png"

    def set_user5(self, *args):
        user5 = args[1]
        self.ids.user5.name = user5["name"]
        self.ids.user5.email = user5["email"]
        self.ids.user5.website = user5["website"]
        self.ids.user5.avatar = "https://cdn4.iconfinder.com/data/icons/avatars-xmas-giveaway/128/female_woman_avatar_portrait_1-256.png"

    def set_user6(self, *args):
        user6 = args[1]
        self.ids.user6.name = user6["name"]
        self.ids.user6.email = user6["email"]
        self.ids.user6.website = user6["website"]
        self.ids.user6.avatar = "https://cdn4.iconfinder.com/data/icons/avatars-xmas-giveaway/128/suicide_squad_woman_avatar_joker-256.png"



    def send_request(self):
        url = "https://jsonplaceholder.typicode.com/"

        UrlRequest(
            url + "users/1", self.set_user1, on_error=self.got_error, timeout=4
        )
        UrlRequest(
            url + "users/2", self.set_user2, on_error=self.got_error, timeout=4
        )
        UrlRequest(
            url + "users/3", self.set_user3, on_error=self.got_error, timeout=4
        )
        UrlRequest(
            url + "users/4", self.set_user4, on_error=self.got_error, timeout=4
        )
        UrlRequest(
            url + "users/5", self.set_user5, on_error=self.got_error, timeout=4
        )
        UrlRequest(
            url + "users/6", self.set_user6, on_error=self.got_error, timeout=4
        )
        UrlRequest(
            url + "users/7", self.set_user7, on_error=self.got_error, timeout=4
        )
        UrlRequest(
            url + "users/8", self.set_user8, on_error=self.got_error, timeout=4
        )
        return True

    def got_error(self, *args):
        error_msg = "Timeout.Check connection"
        return toast(error_msg)

    def clear_data(self):
        self.ids.user2.name = ""
        self.ids.user2.email = ""
        self.ids.user2.website = ""
        self.ids.user2.avatar = ""
        self.ids.user1.avatar = ""
        self.ids.user1.name = ""
        self.ids.user1.email = ""
        self.ids.user1.website = ""

    def warning(self):
        dialog = AKAlertDialog(
            header_icon="close-circle-outline", header_bg=[0.9, 0, 0, 1]
        )
        content = Factory.ErrorDialog()      
        content.ids.button1.bind(on_release=dialog.dismiss)
        content.ids.button2.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()
    def on_enter(self):
        global sex_info,name_info,email_info,name
        self.ids["mailinfo"].text = email_info
        self.ids["usernameprofile"].text = name_info
        self.ids["sexprofile"].text = sex_info
        

class Chatgui(Screen):

    def __init__(self, **kwargs):       
        global status ,bientam
        super().__init__(**kwargs)
        
        Clock.schedule_interval(self.update,2)  


    def thu(self):
        global status,bientam,name
        
        data = self.ids['textct'].text
        dbstore.collection("User").document("message").set({"name":name,"content":data,"time":time.strftime("%H:%M:%S")})
        self.ids['textct'].text = ""
        
        
    def on_snapshot(doc_snapshot, changes, read_time):
        global bientam,name
        for doc in doc_snapshot:
            print(f'Nội dung: {doc.to_dict()}')
            bientam =doc.to_dict()["name"] + doc.to_dict()["content"] +"      "+ doc.to_dict()["time"]

        callback_done.set() 
    doc_ref = dbstore.collection("User").document("message") 
    doc_watch = doc_ref.on_snapshot(on_snapshot)    

    def update(self,*args):
        global bientam,status
        print(bientam,status)
        print(str(i)+"############################################")

        if bientam != status :

            self.ids['content'].text = self.ids['content'].text + "\n" + str(bientam)
            bientam = status
            

    def on_enter(self):
        global duli
        duli = dbstore.collection("User").document("datamessage").get()
        duli = duli.to_dict()
        duli = duli["dt"]
        print(duli)
        print("###################################")
        self.ids['content'].text = duli        
    def savect(self):
        dbstore.collection("User").document("datamessage").set({"dt":self.ids['content'].text})
class Social_media1(MDApp):

    def build(self):


        sm = ScreenManager()
        sm.add_widget(Login(name = "login"))
        sm.add_widget(Signup(name = "signup"))
        sm.add_widget(ForgetPassword(name = "fgp"))
        sm.add_widget(Onboarding(name = "onb"))
        
        sm.add_widget(Main(name = "main"))
        sm.add_widget(Chatgui(name = "chatgui"))
        return sm
        
Social_media1().run()
