from classes.handlers.record_handler import RecordHandler
from classes.handlers.account_handler import AccountHandler
from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables


import tkinter as tk
import secrets
import string
from tkinter import StringVar

import sys


from typing import TYPE_CHECKING



class AddRecordPage(tk.Frame): # Sub-lcassing tk.Frame
    
    if TYPE_CHECKING:
        from main import SampleApp
        app = SampleApp()
    
    def __init__(self, master, *args, **kwargs):

        tk.Frame.__init__(self,master, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg = 'red' ,width = 500,height = 300, relief="sunken")
        self.canvas.pack(fill = "both", expand = True)
        master.title(StaticVariables.ADD_RECORD)
        acc_id = master.set_account_id()

        
        acc_data = master.query_account(acc_id)
        ac_usr = acc_data[1]
        ac_mail = acc_data[2]
        ac_passw = acc_data[3]
        acc = AccountHandler(ac_usr, ac_mail, ac_passw)
        records = acc.query_records_by_account_id(acc_id)
        generated_password = StringVar()
        
        
        self.username_logo = tk.PhotoImage(file=StaticVariables.USERNAME_LOGO_PATH)
        self.email_logo = tk.PhotoImage(file=StaticVariables.EMAIL_LOGO_PATH)
        self.password_logo = tk.PhotoImage(file=StaticVariables.PASSWORD_LOGO_PATH)
        self.website_logo = tk.PhotoImage(file = StaticVariables.WEBSITE_LOGO_PATH)
        self.back_logo = tk.PhotoImage(file=StaticVariables.BACK_LOGO_PATH)
        self.next_logo = tk.PhotoImage(file = StaticVariables.NEXT_LOGO_PATH)
        self.save_logo = tk.PhotoImage(file = StaticVariables.SAVE_LOGO_PATH)
        self.length_logo = tk.PhotoImage(file = StaticVariables.LENGTH_LOGO_PATH)
        self.generate_password_logo = tk.PhotoImage(file = StaticVariables.GENERATE_PASSWORD_LOGO_PATH)
        
        
        
        back_button = tk.Button( self, image = self.back_logo, borderwidth=0, bg='red', command=lambda: master.switch_Canvas('RecordListPage'))
        back_button_canvas = self.canvas.create_window( 10, 250, anchor = "nw",window = back_button)




            
        entry_website_login = tk.Entry(self.canvas)
        entry_username_login = tk.Entry(self.canvas)
        entry_email_login = tk.Entry(self.canvas) 
        entry_password_login = tk.Entry (self.canvas, show="*", textvariable=generated_password)
        
        self.canvas.create_window(130, 40, window=entry_website_login)
        self.canvas.create_window(130, 70, window=entry_username_login)
        self.canvas.create_window(130, 100, window=entry_email_login)
        self.canvas.create_window(130, 130, window=entry_password_login)
        
        website_label = tk.Label(self, bg='red', image= self.website_logo)
        website_canvas = self.canvas.create_window( 2, 30, anchor = "nw",window = website_label)
        username_label = tk.Label(self, bg='red', image= self.username_logo)
        username_canvas = self.canvas.create_window( 2, 60, anchor = "nw",window = username_label)
        email_label = tk.Label(self, bg='red', image= self.email_logo)
        email_canvas = self.canvas.create_window( 2, 90, anchor = "nw",window = email_label)
        password_label = tk.Label(self, bg='red', image= self.password_logo)
        password_canvas = self.canvas.create_window( 2, 120, anchor = "nw",window = password_label)
        
        def handle_create_record():
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')
            
            new_website = entry_website_login.get()
            new_username = entry_username_login.get()
            new_email = entry_email_login.get()
            new_password = entry_password_login.get()
            
            record = RecordHandler(account_id=acc_id, website=new_website, username=new_username, email=new_email, password=new_password)
            record.insert_record()

            master.switch_Canvas(StaticVariables.RECORD_LIST_PAGE)
            
        
        def handle_generate_password():
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')
            
            acc_id = master.set_account_id()
            
            global generate_password_window
            generate_password_window = tk.Toplevel(self.canvas)
            generate_password_window.title(StaticVariables.GENERATE_PASSWORD)
            generate_password_window.geometry('500x300')
            generate_password_window.iconbitmap(StaticVariables.COBRA_LOGO_PATH)
            generate_password_canvas = tk.Canvas(generate_password_window ,bg = 'red', width = 250,height = 150)
            generate_password_canvas.pack(fill = "both", expand = True)
            
            template_password_label = tk.Label(generate_password_window, bg='red', image = self.password_logo)
            template_password_canvas = generate_password_canvas.create_window( 2, 27, anchor = "nw",window = template_password_label)
            
            password_length_label = tk.Label(generate_password_window, bg='red', image = self.length_logo)
            password_length_canvas = generate_password_canvas.create_window( 400, 20, anchor = "nw",window = password_length_label)
            
            entry_template_password_login = tk.Entry(generate_password_window)
            generate_password_canvas.create_window(100, 40, window=entry_template_password_login)
            

            
            spinbox_var = StringVar()
            
            # Creating Spinbox
            password_length_spinbox = tk.Spinbox(generate_password_window, from_ = 8, to = 20, width=3, textvariable=spinbox_var)
            generate_password_canvas.create_window(450, 40, window=password_length_spinbox)
            
            
            
            
            def generate_new_password():
                function_name = sys._getframe().f_code.co_name
                LogHandler.info_log(self, function_name, '', '')
                
                pass_length = spinbox_var.get()
                entry_template_password_login.delete(0, 'end')
                password_length = int(pass_length)
                alphabet = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(alphabet) for i in range(password_length))
                entry_template_password_login.insert(0, password)
                
                
            def handle_set_password():
                function_name = sys._getframe().f_code.co_name
                LogHandler.info_log(self, function_name, '', '')
                
                gen_password = entry_template_password_login.get()
                generated_password.set(gen_password)
                generate_password_window.destroy()
                
                

            #Generate Password Window Buttons
            set_password_button = tk.Button( generate_password_window, image = self.save_logo, borderwidth=0, bg='red', command=handle_set_password)
            set_password_button_canvas = generate_password_canvas.create_window( 60, 250, anchor = "nw",window = set_password_button)
            generate_new_password_button = tk.Button( generate_password_window, image = self.generate_password_logo, borderwidth=0, bg='red', command = generate_new_password )
            generate_password_button_canvas = generate_password_canvas.create_window( 200, 250, anchor = "nw",window = generate_new_password_button)
        
        #Add Record Window Buttons 
        create_record_button = tk.Button( self, image= self.save_logo, borderwidth=0, bg='red', command= handle_create_record)
        add_record_button_canvas = self.canvas.create_window( 60, 250, anchor = "nw",window = create_record_button)
        generate_password_button = tk.Button( self, image= self.generate_password_logo, borderwidth=0, bg='red', command= handle_generate_password)
        generate_password_button_canvas = self.canvas.create_window( 200, 250, anchor = "nw",window = generate_password_button)