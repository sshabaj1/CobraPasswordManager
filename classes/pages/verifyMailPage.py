from classes.handlers.account_handler import AccountHandler
from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables

import sys
import tkinter as tk
from tkinter import StringVar
from typing import TYPE_CHECKING




class VerifyMailPage(tk.Canvas):

    if TYPE_CHECKING:
        from main import SampleApp
        app = SampleApp()

    def __init__(self, app, *args, **kwargs):

        tk.Frame.__init__(self,app, *args, **kwargs)
        self.canvas = tk.Canvas(self , bg = 'red', width = 345,height = 518)
        self.canvas.pack(fill = "both", expand = True)
        app.title(StaticVariables.VERIFY_YOUR_EML)
        app.iconbitmap(StaticVariables.COBRA_ICON_PATH)
        
        response_text = tk.StringVar()
        
        otp_label = tk.Label(self, text=StaticVariables.INSERT_CODE_VERIFY_MAIL, fg='white', bg='red' )
        otp_label_canvas = self.canvas.create_window(20, 100, anchor='nw', window=otp_label)
        
        response_label = tk.Label(self, textvariable=response_text, fg='white', bg='red' )
        response_label_canvas = self.canvas.create_window(80, 350, anchor='nw', window=response_label)
        
        
        self.back_logo = tk.PhotoImage(file=StaticVariables.BACK_LOGO_PATH)
        self.next_logo = tk.PhotoImage(file =StaticVariables.NEXT_LOGO_PATH)
        
        
        back_button = tk.Button( self, image = self.back_logo, borderwidth=0, bg='red', command=lambda: app.switch_Canvas(StaticVariables.LOGIN_PAGE))
        back_button_canvas = self.canvas.create_window( 10, 10, anchor = "nw",window = back_button)
        
        self.otp_logo = tk.PhotoImage(file=StaticVariables.OTP_LOGO_PATH)
        otp_image = self.canvas.create_image(90, 187, image = self.otp_logo, anchor=tk.NW)
        
        
        acc_id = app.set_account_id()
        
        global entry_otp_veriify
        entry_otp_veriify = tk.Entry(self.canvas)
        self.canvas.create_window(180, 200, window=entry_otp_veriify)
        
        
        def handle_verify_email():
            function_name = sys._getframe().f_code.co_name
            LogHandler.debug_log(self, function_name, '', '')
            
            otp_enterd = entry_otp_veriify.get()
            credentials = app.query_account(acc_id)

            accid = credentials[0]
            acc_username = credentials[1]
            acc_email = credentials[2]
            acc_password = credentials[3]
            acc = AccountHandler(acc_username, acc_email, acc_password)
            otp = acc.get_otp()
            
            if otp == otp_enterd:
                
                acc.confirm_account()
                app.switch_Canvas(StaticVariables.ACCOUNT_VERIFIED_PAGE)
                
            else:
                
                res = StaticVariables.WRONG_CODE_ERROR
                response_text.set(res)
                
        
        
        self.small_cobra_logo = tk.PhotoImage(file =StaticVariables.SMALL_COBRA_LOGO_PATH)
        small_logo_image = self.canvas.create_image(130, 450, image = self.small_cobra_logo, anchor=tk.NW)
        
        verify_button = tk.Button( self, image=self.next_logo, borderwidth=0,bg='red', command=handle_verify_email)
        verify_button_canvas = self.canvas.create_window( 160, 300, anchor = "nw",window = verify_button)