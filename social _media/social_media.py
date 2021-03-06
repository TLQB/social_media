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
Window.size = (320, 620)

config = {
    "apiKey": "AIzaSyActuACAwT6Z5h2ozQ3U2Mz8ipoX42sjYc",
    "authDomain": "playchat-386e6.firebaseapp.com",
    "databaseURL":"http://playchat-386e6.firebaseapp.com",
    #"databaseURL":"https://playchat-386e6-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "playchat-386e6",
    "storageBucket": "playchat-386e6.appspot.com",
    "messagingSenderId": "668971008979",
    "appId": "1:668971008979:web:aef3dbc43cfcd83300e526",
    "measurementId": "G-RV9QYHXX53"
  }


firebase = pyrebase.initialize_app(config)
auth= firebase.auth()

Builder.load_file("social_media.kv")

class Login(Screen):
    def checkLogin(self):
        email = self.ids["email_login"].text
        password = self.ids["password_login"].text

        try:
            user = auth.sign_in_with_email_and_password(email,password)
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

        if (validate_email(email)):
            if len(password)>7:

                if str(password)==str(passwordR):
                    try:
                        user = auth.create_user_with_email_and_password(email,passwordR)
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
        self.ids.user1.avatar = "https://cdn4.iconfinder.com/data/icons/avatars-21/512/avatar-circle-human-male-3-512.png"
        self.ids.user1.name = user1["name"]
        self.ids.user1.email = user1["email"]
        self.ids.user1.website = user1["website"]

    def set_user2(self, *args):
        user2 = args[1]
        self.ids.user2.name = user2["name"]
        self.ids.user2.email = user2["email"]
        self.ids.user2.website = user2["website"]
        self.ids.user2.avatar = "https://cdn4.iconfinder.com/data/icons/avatars-21/512/avatar-circle-human-male-3-512.png"

    def send_request(self):
        url = "https://jsonplaceholder.typicode.com/"

        UrlRequest(
            url + "users/1", self.set_user1, on_error=self.got_error, timeout=4
        )
        UrlRequest(
            url + "users/2", self.set_user2, on_error=self.got_error, timeout=4
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
class Chatgui(Screen):
    def msg(self, *args):
        self.content = self.ids["content"].text 
        #self.ids["ct"].text = self.ids["ct"].text +"\n"+self.content
        if self.content != "":
            self.ids['ct'].text = self.ids['ct'].text + '\n' + self.content
            self.ids["content"].text  = ""
        else:
            print("ok")
        
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
