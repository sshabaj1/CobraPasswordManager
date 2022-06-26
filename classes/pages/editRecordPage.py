from classes.handlers.account_handler import AccountHandler
from classes.handlers.record_handler import RecordHandler
from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables

import tkinter as tk
from tkinter import StringVar
import sys






from typing import TYPE_CHECKING


class EditRecordPage(tk.Frame):
    
    if TYPE_CHECKING:
        from main import SampleApp
        app = SampleApp()
    
    def __init__(self, master, *args, **kwargs):

        tk.Frame.__init__(self,master, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg = 'red' ,width = 345,height = 518)
        self.canvas.pack(fill = "both", expand = True)
        master.title(StaticVariables.RECORD_TILE)
        
        self.username_logo = tk.PhotoImage(file=StaticVariables.USERNAME_LOGO_PATH)
        self.email_logo = tk.PhotoImage(file=StaticVariables.EMAIL_LOGO_PATH)
        self.password_logo = tk.PhotoImage(file=StaticVariables.PASSWORD_LOGO_PATH)
        self.website_logo = tk.PhotoImage(file =StaticVariables.WEBSITE_LOGO_PATH)
        self.back_logo = tk.PhotoImage(file=StaticVariables.BACK_LOGO_PATH)
        self.save_logo = tk.PhotoImage(file =StaticVariables.SAVE_LOGO_PATH)
        
        
        
        back_button = tk.Button( self, image = self.back_logo, borderwidth=0, bg='red', command=lambda: master.switch_Canvas(StaticVariables.RECORD_TILE_PAGE))
        back_button_canvas = self.canvas.create_window( 10, 10, anchor = "nw",window = back_button)

        acc_id = master.set_account_id()
        record_id = master.set_record_id()

        acc_data = master.query_account(acc_id)
        ac_usr = acc_data[1]
        ac_mail = acc_data[2]
        ac_passw = acc_data[3]
        acc = AccountHandler(ac_usr, ac_mail, ac_passw)
        record = acc.get_record_by_ids(record_id, acc_id)
        q_website = record[0]
        q_username = record[1]
        q_email = record[2]
        q_password = record[3]

        
        q_web = StringVar(self.canvas, value=q_website)
        q_user = StringVar(self.canvas, value=q_username)
        q_eml = StringVar(self.canvas, value=q_email)
        q_pass = StringVar(self.canvas, value=q_password)

        
        # Labels
        label_website = tk.Label(self, bg='red',foreground='white', image = self.website_logo)
        label_website_canvas = self.canvas.create_window( 2, 50, anchor = "nw",window = label_website)
        label_username = tk.Label(self, bg='red',foreground='white', image = self.username_logo)
        label_username_canvas = self.canvas.create_window( 2, 80, anchor = "nw",window = label_username)
        label_email = tk.Label(self, bg='red',foreground='white', image = self.email_logo)
        label_email_canvas = self.canvas.create_window( 2, 110, anchor = "nw",window = label_email)
        label_password = tk.Label(self, bg='red',foreground='white', image = self.password_logo)
        label_password_canvas = self.canvas.create_window( 2, 140, anchor = "nw",window = label_password)
        
        # Entry Boxes
        global entry_website
        global entry_username
        global entry_emai
        global entry_password
        entry_website = tk.Entry(self.canvas, textvariable=q_web) 
        entry_username = tk.Entry (self.canvas, textvariable=q_user)
        entry_emai = tk.Entry(self.canvas, textvariable=q_eml) 
        entry_password = tk.Entry (self.canvas, textvariable=q_pass)


        self.canvas.create_window(200, 60, window=entry_website)
        self.canvas.create_window(200, 90, window=entry_username)
        self.canvas.create_window(200, 120, window=entry_emai)
        self.canvas.create_window(200, 150, window=entry_password)
        
        
        def handle_save_button():
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')
            
            web = entry_website.get()
            user = entry_username.get()
            eml = entry_emai.get()
            passw = entry_password.get()
            record = RecordHandler(acc_id, web, user, eml, passw)
            record.update_record(acc_id, record_id, web, user, eml, passw)
            master.switch_Canvas(StaticVariables.RECORD_TILE_PAGE)
        
        
        
        
        save_button = tk.Button( self, image = self.save_logo, borderwidth=0, bg='red', command= handle_save_button)
        savebutton_canvas = self.canvas.create_window( 150, 240, anchor = "nw",window = save_button)