from classes.handlers.account_handler import AccountHandler
from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables

import tkinter as tk
import sys
from typing import TYPE_CHECKING




class ChangePasswordPage(tk.Canvas):

    if TYPE_CHECKING:
        from main import SampleApp
        app = SampleApp()

    def __init__(self, app, *args, **kwargs):

        tk.Frame.__init__(self,app, *args, **kwargs)
        self.canvas = tk.Canvas(self , bg = 'red', width = 345,height = 518)
        self.canvas.pack(fill = "both", expand = True)
        app.title(StaticVariables.CHANGE_PASSWORD)
        app.iconbitmap(StaticVariables.COBRA_LOGO_PATH)
        acc_id = app.set_account_id()
        
        
        website_label = tk.Label(self, bg='red', text=StaticVariables.CHANGE_YOUR_PASSWORD, foreground='white')
        website_canvas = self.canvas.create_window( 110, 150, anchor = "nw",window = website_label)
        
        old_password_label = tk.Label(self, bg='red', text=StaticVariables.OLD_PASSWORD, foreground='white')
        old_password_canvas = self.canvas.create_window( 230, 190, anchor = "nw",window = old_password_label)
        
        new_password_label = tk.Label(self, bg='red', text=StaticVariables.NEW_PASSWORD, foreground='white')
        new_password_canvas = self.canvas.create_window( 230, 220, anchor = "nw",window = new_password_label)
        
        confirm_password_label = tk.Label(self, bg='red', text=StaticVariables.CONFIRM_PASSWORD, foreground='white')
        confirm_password_canvas = self.canvas.create_window( 230, 250, anchor = "nw",window = confirm_password_label)
        
        code_label = tk.Label(self, bg='red', text='Code', foreground='white')
        code_canvas = self.canvas.create_window( 230, 280, anchor = "nw",window = code_label)
        
        self.password_logo = tk.PhotoImage(file=StaticVariables.PASSWORD_LOGO_PATH)
        old_password_logo = self.canvas.create_image(90, 190, image = self.password_logo, anchor=NW)
        new_password_logo = self.canvas.create_image(90, 220, image = self.password_logo, anchor=NW)
        confirm_password_logo = self.canvas.create_image(90, 250, image = self.password_logo, anchor=NW)
        
        
        self.otp_logo = tk.PhotoImage(file=StaticVariables.OTP_LOGO_PATH)
        otp_image = self.canvas.create_image(90, 280, image = self.otp_logo, anchor=NW)
        
        
        self.back_logo = tk.PhotoImage(file=StaticVariables.BACK_LOGO_PATH)
        self.next_logo = tk.PhotoImage(file =StaticVariables.NEXT_LOGO_PATH)
        
        
        
        back_button = tk.Button( self, image=self.back_logo, borderwidth=0, bg='red', command=lambda: app.switch_Canvas(StaticVariables.ACCOUNT_PAGE))
        back_button_canvas = self.canvas.create_window( 10, 10, anchor = "nw",window = back_button)


        # Create Entry Box
        global entry_old_password
        global entry_new_password
        global entry_verify_password
        global entry_verify_otp
        entry_old_password = tk.Entry(self.canvas, show="*")
        entry_new_password = tk.Entry(self.canvas, show="*")
        entry_verify_password = tk.Entry (self.canvas, show="*")
        entry_verify_otp = tk.Entry(self.canvas)
        

        self.canvas.create_window(180, 200, window=entry_old_password)
        self.canvas.create_window(180, 230, window=entry_new_password)
        self.canvas.create_window(180, 260, window=entry_verify_password)
        self.canvas.create_window(180, 290, window=entry_verify_otp)
        
        
        def handle_change_password():
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')
            
            credentials = app.query_account(acc_id)

            acc_username = credentials[1]
            acc_email = credentials[2]
            acc_password = credentials[3]
            
            acc = AccountHandler(acc_username, acc_email, acc_password)
            
            old_passw = entry_old_password.get()
            new_pass = entry_new_password.get()
            verify_pass = entry_verify_password.get()
            verify_otp = entry_verify_otp.get()
            status =  acc.change_password(acc_id, old_passw,new_pass,verify_pass, verify_otp)
            
            if status == StaticVariables.PASSWORD_CHANGED:
                
                LogHandler.debug_log(self, function_name, 'Password is changed', '')

                app.switch_Canvas('AccountPage')
                
            elif status == StaticVariables.INCORRECT_OTP:
                
                LogHandler.debug_log(self, function_name, 'OTP is wrong', '')

            elif status == StaticVariables.PASSWRODS_DONT_MATCH:
                LogHandler.debug_log(self, function_name, 'Passwords dont match', '')
                
            else:
                LogHandler.debug_log(self, function_name, 'Old password is wrong', '')

                
        
        self.small_cobra_logo = tk.PhotoImage(file = StaticVariables.SMALL_COBRA_LOGO_PATH)
        small_logo_image = self.canvas.create_image(130, 450, image = self.small_cobra_logo, anchor=NW)
        
        change_password_button = tk.Button( self, image = self.next_logo, borderwidth=0, bg='red', command=handle_change_password)
        change_password_button_canvas = self.canvas.create_window( 160, 350, anchor = "nw",window = change_password_button)