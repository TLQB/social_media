import kivymd_extensions.akivymd
from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog

Builder.load_string(
    """
<SuccessDialog@BoxLayout>:
    orientation: "vertical"
    padding: dp(40)

    MDLabel:
        text: "Successful!"
        size_hint_y: None
        height: self.texture_size[1]
        halign: "center"
        valign: "center"
        bold: True
        theme_text_color: "Custom"
        text_color: 0, .7, 0, 1

    MDLabel:
        text: "These are some custom contents!"
        halign: "center"
        valign: "top"
        theme_text_color: "Custom"
        text_color: 0, .7, 0, 1
        font_style: "Caption"

    MDFillRoundFlatButton:
        id: button
        text: "Confirm"
        md_bg_color: 0, .7, 0, 1
        pos_hint: {"center_x": .5}


<ErrorDialog@BoxLayout>:
    orientation: "vertical"
    spacing: dp(10)
    padding: dp(20)

    MDLabel:
        text: "Connection Failed"
        halign: "center"
        theme_text_color: "Custom"
        text_color: .9, 0, 0, 1

    MDLabel:
        text: "Connection Failed. Make sure you are connected to the internet and then try again!"
        halign: "center"
        theme_text_color: "Custom"
        text_color: .9, 0, 0, 1
        font_style: "Caption"

    MDFillRoundFlatButton:
        id: button
        text: "Dismiss"
        md_bg_color: .9, 0, 0, 1
        pos_hint: {"center_x": .5}


<WarningDialog>
    BoxLayout:
        orientation: "vertical"
        padding: dp(20) 

        MDLabel:
            text: "Password Required"
            halign: "center"
            valign: "center"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color 

        MDLabel:
            text: "Please enter password before continue"
            theme_text_color: "Secondary"
            font_style: "Caption"   

        MDTextField:
            hint_text: "Password"   

        MDFillRoundFlatButton:
            id: submit
            text: "Submit"
            pos_hint: {"center_x": .5}
            md_bg_color: 1, .75, 0, 1





<Dialogs>

    MDBoxLayout:
        orientation: "vertical"



        StackLayout:
            orientation: "lr-tb"
            padding: dp(20)
            spacing: dp(20)

            MDRaisedButton:
                text: "Success"
                on_release: root.success()

            MDRaisedButton:
                text: "Error"
                on_release: root.error()

            MDRaisedButton:
                text: "Warning"
                on_release: root.warning()

            MDRaisedButton:
                text: "Bottom_Right"
                on_release: root.bottom_right()

            MDRaisedButton:
                text: "Top_Center"
                on_release: root.top_center()
"""
)


class Dialogs(Screen):
    def success(self):
        dialog = AKAlertDialog(
            header_icon="check-circle-outline", header_bg=[0, 0.7, 0, 1]
        )
        content = Factory.SuccessDialog()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

    def error(self):
        dialog = AKAlertDialog(
            header_icon="close-circle-outline", header_bg=[0.9, 0, 0, 1]
        )
        content = Factory.ErrorDialog()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

    def warning(self):
        dialog = AKAlertDialog(
            header_icon="exclamation",
            header_bg=[1, 0.75, 0, 1],
            progress_interval=3,
        )
        dialog.bind(on_progress_finish=dialog.dismiss)
        content = Factory.WarningDialog()
        content.ids.submit.bind(on_release=dialog.dismiss)
        content.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

class Social_media2(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Dialogs(name = "login"))
        
        return sm
        
Social_media2().run()