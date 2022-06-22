from classes.handlers.account_handler import AccountHandler
from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables

import tkinter as tk
from typing import TYPE_CHECKING







class LoginPage(tk.Canvas):

    if TYPE_CHECKING:
        from main import SampleApp
        app = SampleApp()

    def __init__(self, app, *args, **kwargs):

        tk.Frame.__init__(self,app, *args, **kwargs)
        self.canvas = tk.Canvas(self , bg = 'red', width = 345,height = 518)
        self.canvas.pack(fill = "both", expand = True)
        app.title(StaticVariables.COBRA_PASSW_MANAGER)
        app.iconbitmap(StaticVariables.COBRA_LOGO_PATH)
        

        self.logo = tk.PhotoImage(file =StaticVariables.COBRA_LOGO_PATH)
        self.login_logo = tk.PhotoImage(file =StaticVariables.LOGIN_LOGO_PATH)
        self.register_logo = tk.PhotoImage(file =StaticVariables.REGISTER_LOGO_PATH )
        error_logo = tk.PhotoImage(file=StaticVariables.ERROR_LOGO_PATH)
        self.username_logo = tk.PhotoImage(file=StaticVariables.USERNAME_LOGO_PATH)
        self.password_logo = tk.PhotoImage(file=StaticVariables.PASSWORD_LOGO_PATH)
        username_image = self.canvas.create_image(80, 190, image = self.username_logo, anchor=NW)
        password_image = self.canvas.create_image(80, 220, image = self.password_logo, anchor=NW)
        logo_image = self.canvas.create_image(100, 50, image = self.logo, anchor=NW)
        

       # Create Entry Box
        global entry_username_login
        global entry_password_login
        entry_username_login = tk.Entry(self.canvas) 
        entry_password_login = tk.Entry (self.canvas, show="*") 

        self.canvas.create_window(180, 200, window=entry_username_login)
        self.canvas.create_window(180, 230, window=entry_password_login)
       
        def handle_wrong_username():
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')
            
            global wrong_username_window
            wrong_username_window = tk.Toplevel(self.canvas)
            wrong_username_window.title(StaticVariables.COBRA_PASSW_MANAGER)
            wrong_username_window.geometry('250x150')
            wrong_username_window.iconbitmap(StaticVariables.COBRA_LOGO_PATH)
            wrong_username_canvas = tk.Canvas(wrong_username_window , width = 250,height = 150, bg='red')
            wrong_username_canvas.pack(fill = "both", expand = True)
            wrong_username_canvas.create_image( 115, 20, image = error_logo, anchor = "nw")
            wrong_username_label = tk.Label(wrong_username_window, text=StaticVariables.USERNAME_NOT_FOUND, foreground='white', bg='red')
            wrong_username_canvas = wrong_username_canvas.create_window( 10, 50, anchor = "nw",window = wrong_username_label)




        def handle_wrong_password():
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')
            
            global wrong_password_window
            wrong_password_window = tk.Toplevel(self.canvas)
            wrong_password_window.title(StaticVariables.COBRA_PASSW_MANAGER)
            wrong_password_window.geometry('250x150')
            wrong_password_window.iconbitmap(StaticVariables.COBRA_LOGO_PATH)
            wrong_password_canvas = tk.Canvas(wrong_password_window , width = 250,height = 150, bg='red')
            wrong_password_canvas.pack(fill = "both", expand = True)
            wrong_password_canvas.create_image( 115, 20, image = error_logo, anchor = "nw")
            wrong_password_label = tk.Label(wrong_password_window, text=StaticVariables.WRONG_PASSW, foreground='white', bg='red')
            wrong_password_canvas = wrong_password_canvas.create_window( 40, 50, anchor = "nw",window = wrong_password_label)

        
        def handle_register():
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')
            
            app.switch_Canvas(StaticVariables.REGISTER_PAGE)
        
           
        def handle_login_button():
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')
            
            # Create Variables from user input
            login_username = entry_username_login.get()
            login_password = entry_password_login.get()
            acc = AccountHandler(login_username, '', login_password)
            status = acc.check_account_status()
            credencials = acc.query_login_cred(login_username)
            
            if credencials is not None:
                
                if login_username == credencials[StaticVariables.L_USERNAME_STRING]:
                    
                    if login_password == credencials[StaticVariables.L_PASSW_STRING]:

                        app.get_account_id(credencials['id'])

                        if status == StaticVariables.VERIFIED_STRING:
                            app.switch_Canvas(StaticVariables.LANDING_PAGE)
                        else:
                            app.switch_Canvas(StaticVariables.VERIFY_MAIL_PAGE)
                        
                    else:
                        handle_wrong_password()
                        
                else:
                    handle_wrong_username()
            else:
                handle_wrong_username()
                
        def handle_forgot_password(self):
            app.switch_Canvas(StaticVariables.RECOVER_PASSW_PAGE)
                
        forgot_password_label = tk.Label(self, text=StaticVariables.FORGOT_PASSW_BUTTON, fg="white", bg='red', cursor="hand2")
        forgot_password_label.bind("<Button-1>",handle_forgot_password)
        forgot_password_label_canvas = self.canvas.create_window(120, 260, anchor='nw', window=forgot_password_label)
        
        register_label = tk.Label(self, text=StaticVariables.SING_UP_BUTTON, fg='white', bg='red' )
        register_label_canvas = self.canvas.create_window(90, 400, anchor='nw', window=register_label)
        
        login_button = tk.Button( self, image = self.login_logo, borderwidth=0, command=handle_login_button, bg='red')
        login_button_canvas = self.canvas.create_window( 155, 300, anchor = "nw",window = login_button)
        
        register_button = tk.Button( self, image = self.register_logo, borderwidth=0, command=handle_register, bg='red')
        register_button_canvas = self.canvas.create_window( 155, 450, anchor = "nw",window = register_button)