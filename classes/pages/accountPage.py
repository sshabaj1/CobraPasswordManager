from classes.handlers.account_handler import AccountHandler
from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables

import tkinter as tk
import threading
import sys



from typing import TYPE_CHECKING




class AccountPage(tk.Frame):
    
    if TYPE_CHECKING:
        from main import SampleApp
        app = SampleApp()
    
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self,master, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg = 'red' ,width = 345,height = 518)
        self.canvas.pack(fill = "both", expand = True)
        master.title(StaticVariables.ACCOUNT)
        acc_id = master.set_account_id()

        
        
        self.back_logo = tk.PhotoImage(file = StaticVariables.BACK_LOGO_PATH)
        self.email_logo = tk.PhotoImage(file = StaticVariables.EMAIL_LOGO_PATH)
        self.password_logo = tk.PhotoImage(file = StaticVariables.PASSWORD_LOGO_PATH)
        
        back_button = tk.Button( self, image = self.back_logo, borderwidth=0, bg='red', command=lambda: master.switch_Canvas(StaticVariables.LANDING_PAGE))
        back_button_canvas = self.canvas.create_window( 10, 10, anchor = "nw",window = back_button)
        
        
        
        def send_change_password_otp():
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')
            
            credentials = master.query_account(acc_id)
            acc_username = credentials[1]
            acc_email = credentials[2]
            acc_password = credentials[3]
            acc = AccountHandler(acc_username, acc_email, acc_password)
            acc.set_otp()
            acc.send_otp_change_pass()
        
        
        def handle_change_password():
            function_name = sys._getframe().f_code.co_name
            LogHandler.debug_log(self, function_name, '', '')
            
            credentials = master.query_account(acc_id)
            accid = credentials[0]
            acc_username = credentials[1]
            acc_email = credentials[2]
            acc_password = credentials[3]
            acc = AccountHandler(acc_username, acc_email, acc_password)
            send_mail = threading.Thread(target=send_change_password_otp)
            send_mail.start()
            master.switch_Canvas(StaticVariables.CHANGE_PASSWORD_PAGE)
            
        
        def send_change_mail_otp():
            function_name = sys._getframe().f_code.co_name
            LogHandler.debug_log(self, function_name, '', '')
            
            credentials = master.query_account(acc_id)
            accid = credentials[0]
            acc_username = credentials[1]
            acc_email = credentials[2]
            acc_password = credentials[3]
            acc = AccountHandler(acc_username, acc_email, acc_password)
            acc.set_otp()
            acc.send_otp_change_email()
            
            
        
        
        def handle_change_email():
            function_name = sys._getframe().f_code.co_name
            LogHandler.debug_log(self, function_name, '', '')
            
            credentials = master.query_account(acc_id)
            accid = credentials[0]
            acc_username = credentials[1]
            acc_email = credentials[2]
            acc_password = credentials[3]
            acc = AccountHandler(acc_username, acc_email, acc_password)
            send_mail = threading.Thread(target=send_change_mail_otp)
            send_mail.start()
            master.switch_Canvas(StaticVariables.CHANGE_EMAIL_PAGE)
        
        self.small_cobra_logo = tk.PhotoImage(file = StaticVariables.SMALL_COBRA_LOGO)
        small_logo_image = self.canvas.create_image(130, 400, image = self.small_cobra_logo, anchor=tk.NW)
        
        change_password_button = tk.Button( self, image = self.password_logo, borderwidth=0, bg='red', command=handle_change_password)
        change_password_button_canvas = self.canvas.create_window( 200, 250, anchor = "nw",window = change_password_button)
        
        change_email_button = tk.Button( self, image = self.email_logo, borderwidth=0, bg='red', command=handle_change_email)
        change_email_button_canvas = self.canvas.create_window( 110, 250, anchor = "nw",window = change_email_button)