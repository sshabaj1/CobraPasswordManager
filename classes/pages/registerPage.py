from classes.handlers.account_handler import AccountHandler
from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables


import tkinter as tk
from tkinter import StringVar
import threading
import sys
from typing import TYPE_CHECKING




class RegisterPage(tk.Canvas):

    if TYPE_CHECKING:
        from main import SampleApp
        app = SampleApp()

    def __init__(self, app, *args, **kwargs):

        tk.Frame.__init__(self,app, *args, **kwargs)
        self.canvas = tk.Canvas(self , bg = 'red', width = 345,height = 518)
        self.canvas.pack(fill = "both", expand = True)
        app.title(StaticVariables.REGISTER)
        app.iconbitmap(StaticVariables.COBRA_ICON_PATH)
        
        # Load images
        self.username_logo = tk.PhotoImage(file=StaticVariables.USERNAME_LOGO_PATH)
        self.email_logo = tk.PhotoImage(file=StaticVariables.EMAIL_LOGO_PATH)
        self.password_logo = tk.PhotoImage(file=StaticVariables.PASSWORD_LOGO_PATH)
        self.back_logo = tk.PhotoImage(file=StaticVariables.BACK_LOGO_PATH)
        self.next_logo = tk.PhotoImage(file =StaticVariables.NEXT_LOGO_PATH)
        
        response_text = StringVar()
        
        username_image = self.canvas.create_image(80, 187, image = self.username_logo, anchor=tk.NW)
        email_image = self.canvas.create_image(80, 217, image = self.email_logo, anchor=tk.NW)
        password_image = self.canvas.create_image(80, 247, image = self.password_logo, anchor=tk.NW)

        back_button = tk.Button( self, image = self.back_logo, borderwidth=0, background='red', command=lambda: app.switch_Canvas('LoginPage'))
        back_button_canvas = self.canvas.create_window( 10, 10, anchor = "nw",window = back_button)
        
        
        wellcome_label = tk.Label(self, text=StaticVariables.WELLCOME_MESSAGE, fg='white', bg='red' )
        wellcome_label_canvas = self.canvas.create_window(50, 100, anchor='nw', window=wellcome_label)
        
        tips_label = tk.Label(self, text=StaticVariables.ENTER_CREDENCIALS, fg='white', bg='red' )
        tips_label_canvas = self.canvas.create_window(10, 130, anchor='nw', window=tips_label)
        
        response_label = tk.Label(self, textvariable=response_text, fg='white', bg='red' )
        response_label_canvas = self.canvas.create_window(80, 350, anchor='nw', window=response_label)
        
        
        # Create Entry Box
        global entry_username_register
        global entry_email_register
        global entry_password_register
        entry_username_register = tk.Entry(self.canvas)
        entry_email_register = tk.Entry(self.canvas)
        entry_password_register = tk.Entry (self.canvas, show="*")
        
        

        self.canvas.create_window(180, 200, window=entry_username_register)
        self.canvas.create_window(180, 230, window=entry_email_register)
        self.canvas.create_window(180, 260, window=entry_password_register)
        
        
        def send_register_otp(usr, eml, passw):
            function_name = sys._getframe().f_code.co_name
            LogHandler.debug_log(self, function_name, '', '')
            
            acc = AccountHandler(usr, eml, passw)
            acc.set_otp()
            acc.send_otp_verify_acc()
        
        
        def handle_register():
            function_name = sys._getframe().f_code.co_name
            print('function_name: ', function_name)
            LogHandler.debug_log(self, function_name, '', '')
            
            register_username = entry_username_register.get()
            register_email = entry_email_register.get()
            register_password = entry_password_register.get()
            creds = [register_username, register_email, register_password]

            if len(register_username) > 6:
                if len(register_email) > 10:
                    if len(register_password) > 8:
                        acc = AccountHandler(register_username, register_email, register_password)
                        account_created = acc.create_account()
                        print('account_created: ', account_created)
                        if account_created['status'] == True:
                            res = StaticVariables.PLEASE_WAIT
                            response_text.set(res)
                            app.get_account_id(account_created['acc_id'])

                            send_mail = threading.Thread(target=send_register_otp, args=(register_username, register_email, register_password))
                            send_mail.start()
                            app.switch_Canvas(StaticVariables.VERIFY_MAIL_PAGE)   
                    else:
                        res = StaticVariables.PASSWORD_SHORT_ERROR
                        response_text.set(res)
                else:
                    res = StaticVariables.EMAIL_SHORT_ERROR
                    response_text.set(res)
            else:
                
                res = StaticVariables.USERNAME_SHORT_ERROR
                response_text.set(res)
            
            
        
        self.small_cobra_logo = tk.PhotoImage(file =StaticVariables.SMALL_COBRA_LOGO_PATH)
        small_logo_image = self.canvas.create_image(130, 450, image = self.small_cobra_logo, anchor=tk.NW)
        
        
        register_button = tk.Button( self, image = self.next_logo, borderwidth=0, bg='red', command= handle_register)
        register_button_canvas = self.canvas.create_window( 160, 300, anchor = "nw",window = register_button)