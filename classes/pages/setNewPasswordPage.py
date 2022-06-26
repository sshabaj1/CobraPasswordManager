from classes.handlers.account_handler import AccountHandler
from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables


import tkinter as tk
import sys
from typing import TYPE_CHECKING




class SetNewPasswordPage(tk.Canvas):

    if TYPE_CHECKING:
        from main import SampleApp
        app = SampleApp()

    def __init__(self, app, *args, **kwargs):

        tk.Frame.__init__(self,app, *args, **kwargs)
        self.canvas = tk.Canvas(self , bg = 'red', width = 345,height = 518)
        self.canvas.pack(fill = "both", expand = True)
        app.title(StaticVariables.SET_PASSWORD)
        app.iconbitmap(StaticVariables.COBRA_ICON_PATH)
        print()

        
        self.otp_logo = tk.PhotoImage(file=StaticVariables.OTP_LOGO_PATH)
        self.password_logo = tk.PhotoImage(file=StaticVariables.PASSWORD_LOGO_PATH)
        self.back_logo = tk.PhotoImage(file=StaticVariables.BACK_LOGO_PATH)
        self.next_logo = tk.PhotoImage(file =StaticVariables.NEXT_LOGO_PATH)
        error_logo = tk.PhotoImage(file=StaticVariables.ERROR_LOGO_PATH)
        
        self.small_cobra_logo = tk.PhotoImage(file =StaticVariables.SMALL_COBRA_LOGO_PATH)
        small_logo_image = self.canvas.create_image(130, 450, image = self.small_cobra_logo, anchor=tk.NW)
        
        website_label = tk.Label(self, bg='red', text=StaticVariables.ENTER_NEW_PASSW, foreground='white')
        website_canvas = self.canvas.create_window( 100, 150, anchor = "nw",window = website_label)
        
        
        username_image = self.canvas.create_image(90, 190, image = self.otp_logo, anchor=tk.NW)
        password1_image = self.canvas.create_image(90, 220, image = self.password_logo, anchor=tk.NW)
        password2_image = self.canvas.create_image(90, 250, image = self.password_logo, anchor=tk.NW)
        
        code_label = tk.Label(self, bg='red', text=StaticVariables.CONFIRM_CODE, foreground='white')
        code_canvas = self.canvas.create_window( 240, 190, anchor = "nw",window = code_label)
        
        new_password_label = tk.Label(self, bg='red', text=StaticVariables.NEW_PASSWORD, foreground='white')
        new_password_canvas = self.canvas.create_window( 240, 220, anchor = "nw",window = new_password_label)
        
        confirm_password_label = tk.Label(self, bg='red', text=StaticVariables.CONFIRM_PASSWORD, foreground='white')
        confirm_password_canvas = self.canvas.create_window( 240, 250, anchor = "nw",window = confirm_password_label)
        
        global entry_otp
        global entry_password1
        global entry_password2

        entry_otp = tk.Entry(self.canvas)
        entry_password1 = tk.Entry(self.canvas, show='*')
        entry_password2 = tk.Entry(self.canvas, show='*')

        self.canvas.create_window(180, 200, window=entry_otp)
        self.canvas.create_window(180, 230, window=entry_password1)
        self.canvas.create_window(180, 260, window=entry_password2)
        
        
        back_button = tk.Button( self, image = self.back_logo, borderwidth=0, bg='red', command=lambda: app.switch_Canvas(StaticVariables.LOGIN_PAGE))
        back_button_canvas = self.canvas.create_window( 10, 10, anchor = "nw",window = back_button)
        
        
        def handle_wrong_otp():
            function_name = sys._getframe().f_code.co_name
            LogHandler.debug_log(self, function_name, '', '')
            
            global wrong_otp_window
            wrong_otp_window = tk.Toplevel(self.canvas)
            wrong_otp_window.title(StaticVariables.COBRA_PASSW_MANAGER)
            wrong_otp_window.geometry('250x150')
            wrong_otp_window.iconbitmap(StaticVariables.COBRA_LOGO_PATH)
            wrong_otp_canvas = tk.Canvas(wrong_otp_window , width = 250,height = 150, bg='red')
            wrong_otp_canvas.pack(fill = "both", expand = True)
            wrong_otp_canvas.create_image( 115, 20, image = error_logo, anchor = "nw")
            wrong_otp_label = tk.Label(wrong_otp_window, text=StaticVariables.WRONG_CODE_ERROR, foreground='white', bg='red')
            wrong_otp_window = wrong_otp_canvas.create_window( 40, 50, anchor = "nw",window = wrong_otp_label)
        
        def handle_password_not_match():
            function_name = sys._getframe().f_code.co_name
            LogHandler.debug_log(self, function_name, '', '')
            
            global wrong_password_window
            wrong_password_window = tk.Toplevel(self.canvas)
            wrong_password_window.title(StaticVariables.COBRA_PASSW_MANAGER)
            wrong_password_window.geometry('250x150')
            wrong_password_window.iconbitmap(StaticVariables.COBRA_LOGO_PATH)
            wrong_password_canvas = tk.Canvas(wrong_otp_window , width = 250,height = 150, bg='red')
            wrong_password_canvas.pack(fill = "both", expand = True)
            wrong_password_canvas.create_image( 115, 20, image = error_logo, anchor = "nw")
            wrong_password_label = tk.Label(wrong_otp_window, text=StaticVariables.WRONG_PASSWORD_ERROR, foreground='white', bg='red')
            wrong_password_window = wrong_password_canvas.create_window( 40, 50, anchor = "nw",window = wrong_password_label)
        
        
        def handle_set_password():
            function_name = sys._getframe().f_code.co_name
            LogHandler.debug_log(self, function_name, '', '')
            
            otp = app.set_otp()
            enterd_otp = entry_otp.get()
            pass1 = entry_password1.get()
            pass2 = entry_password2.get()
            if otp == enterd_otp:
                if pass1 == pass2:
                    account_username = app.set_account_username()
                    account_credencials = app.query_account_by_username(account_username)
                    q_account_id = account_credencials[0]
                    q_account_email = account_credencials[2]
                    q_account_password = pass1
                    acc = AccountHandler(account_username, q_account_email, q_account_password)
                    acc.set_new_password(q_account_id, q_account_password)
                    app.switch_Canvas(StaticVariables.PASSW_RECOVERED_PAGE)
                else:
                    handle_password_not_match
            else:
                handle_wrong_otp()
        
        
        next_button = tk.Button( self, image = self.next_logo, borderwidth=0, bg='red', command= handle_set_password)    
        next_button_canvas = self.canvas.create_window( 155, 300, anchor = "nw",window = next_button)