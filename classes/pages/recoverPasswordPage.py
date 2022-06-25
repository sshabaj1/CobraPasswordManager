from classes.handlers.account_handler import AccountHandler
from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables

import tkinter as tk
import threading
from typing import TYPE_CHECKING
import sys
from tkinter import StringVar



class RecoverPasswordPage(tk.Canvas):

    if TYPE_CHECKING:
        from main import SampleApp
        app = SampleApp()

    def __init__(self, app, *args, **kwargs):

        tk.Frame.__init__(self,app, *args, **kwargs)
        self.canvas = tk.Canvas(self , bg = 'red', width = 345,height = 518)
        self.canvas.pack(fill = "both", expand = True)
        app.title(StaticVariables.RECOVER_PASSWORD)
        app.iconbitmap(StaticVariables.COBRA_ICON_PATH)

        
        self.username_logo = tk.PhotoImage(file=StaticVariables.USERNAME_LOGO_PATH)
        self.email_logo = tk.PhotoImage(file=StaticVariables.EMAIL_LOGO_PATH)
        self.password_logo = tk.PhotoImage(file=StaticVariables.PASSWORD_LOGO_PATH)
        self.back_logo = tk.PhotoImage(file=StaticVariables.BACK_LOGO_PATH)
        self.next_logo = tk.PhotoImage(file = StaticVariables.NEXT_LOGO_PATH)
        
        
        self.small_cobra_logo = tk.PhotoImage(file =StaticVariables.SMALL_COBRA_LOGO_PATH)
        small_logo_image = self.canvas.create_image(130, 450, image = self.small_cobra_logo, anchor=tk.NW)
        
        username_image = self.canvas.create_image(85, 190, image = self.username_logo, anchor=tk.NW)
        email_image = self.canvas.create_image(85, 220, image = self.email_logo, anchor=tk.NW)
        
        
        website_label = tk.Label(self, bg='red', text=StaticVariables.ENTER_USR_EML_TO_RECOVER_PASSW, foreground='white')
        website_canvas = self.canvas.create_window( 5, 150, anchor = "nw",window = website_label)
        
        return_var = StringVar()
        
        return_label = tk.Label(self, bg='red', textvariable= return_var, foreground='white')
        return_canvas = self.canvas.create_window( 120, 400, anchor = "nw",window = return_label)
        
        back_button = tk.Button( self, image = self.back_logo, borderwidth=0, bg='red', command=lambda: app.switch_Canvas(StaticVariables.LOGIN_PAGE))
        back_button_canvas = self.canvas.create_window( 10, 10, anchor = "nw",window = back_button)
        
        # Create Entry Box
        global entry_username
        global entry_email

        entry_username = tk.Entry(self.canvas)
        entry_email = tk.Entry(self.canvas)

        self.canvas.create_window(180, 200, window=entry_username)
        self.canvas.create_window(180, 230, window=entry_email)
        
        
        def thread_send_otp_recover_password(ret_eml):
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')
            return_email = ret_eml
            app.send_otp_recover_password(return_email)
        
        
        def handle_recover_password():
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')

            q_username = entry_username.get()
            q_email = entry_email.get()
            credencials = app.query_account_by_username(q_username)

            if len(credencials) > 0:
                return_username = credencials[1]
                return_email = credencials[2]

                if return_username == q_username:
                    app.get_account_username(return_username)

                    if return_email == q_email:
                        send_mail = threading.Thread(target=thread_send_otp_recover_password, args=(return_email,))
                        send_mail.start()

                        app.switch_Canvas(StaticVariables.SET_NEW_PASSW_PAGE)
                        
                    else:
                        return_var.set(StaticVariables.WRONG_EML_STRING)

                        LogHandler.debug_log(self, function_name, 'Wrong Email: ', return_email)
                        
                else:
                    return_var.set(StaticVariables.WRONG_USR_STRING)
                    
                    LogHandler.debug_log(self, function_name, 'Wrong Username: ', return_username)
            
            
            
        next_button = tk.Button( self, image = self.next_logo, borderwidth=0, bg='red', command= handle_recover_password)    
        next_button_canvas = self.canvas.create_window( 155, 300, anchor = "nw",window = next_button)