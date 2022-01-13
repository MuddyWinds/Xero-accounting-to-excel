import os
import sys
from xero_api import xero_auth_url, xero_first_auth, xero_refresh_token, xero_request
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.popup import Popup



class display_options(GridLayout):
    def close_all(self):
        Window.close()


    def createPopUp(self,title,msg):
        box = BoxLayout(orientation = 'vertical', padding = (10))
        box.add_widget(Label(text = msg))
        btn1 = Button(text = "OK")
    
        box.add_widget(btn1)
        popup = Popup(title=title, title_size= (30),title_align = 'center', content = box, size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    
        btn1.bind(on_press = self.close_all)
        popup.open()


    def on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 36:    # 40 - Entry key pressed
            self.connectBtn(instance)


    def get_response_url(self, instance):
        self.remove_widget(self.box1)

        old_tokens = xero_auth_url(self.ressult_url.text)
        xero_refresh_token(old_tokens[1])
        xero_request()

        self.createPopUp("Request Succeeded.", "Please check the excel file")


    def get_all_report_types(self, instance):
        # First time running the script
        xero_first_auth()
         
        self.box1.remove_widget(self.confirm_btn)
        self.confirm_btn = Button(text='Download Excel', on_press=self.get_all_report_types, size_hint=(0.3,1))
        self.ressult_url = TextInput(hint_text='Paste your response URL ', multiline=False, write_tab=False, size_hint=(0.4, 1))
        self.box1.add_widget(self.ressult_url)

        self.confirm_btn = Button(text='Confirm', on_press=self.get_response_url, size_hint=(0.3,1))
        self.box1.add_widget(self.confirm_btn)


    def open_file_explorer(self, instance):
        xero_request()
        self.createPopUp("Request Succeeded.", "Please check the excel file")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        Window.size = (500, 200)
        
        # Choose Report Type   ** Replace by drop down menu
        self.box1 = BoxLayout(orientation='horizontal', spacing=10)
        self.box1.add_widget(Label(text="Initial Connection", size_hint=(0.3, 1)))
        self.confirm_btn = Button(text='Connect', on_press=self.get_all_report_types, size_hint=(0.3,1))
        self.box1.add_widget(self.confirm_btn)
        self.add_widget(self.box1)

        # Specify the excel sheet name to be specified  ** Allow user to select 
        self.box3 = BoxLayout(orientation='horizontal', spacing=10)
        self.box3.add_widget(Label(text="Reconnection ", size_hint=(0.3, 1)))
        # self.excel_sheet_name = TextInput(hint_text='Paste your path here',multiline=False, size_hint=(0.4, 1))
        self.choose_btn = Button(text='Re-connect', on_press=self.open_file_explorer, size_hint=(.3,1))
        # self.box3.add_widget(self.excel_sheet_name)
        self.box3.add_widget(self.choose_btn)
        self.add_widget(self.box3)

        Window.bind(on_key_down=self.on_keyboard_down)


class xero_integration(App):
    def build(self):
        self.title = "Xero-Pytho Integration"

        # Display full argument list
        print('Number of arguments: ', len(sys.argv), 'arguments.')
        print('Argument List', str(sys.argv))

        return display_options()
