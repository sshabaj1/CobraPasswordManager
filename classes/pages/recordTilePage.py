from classes.handlers.account_handler import AccountHandler
from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables


import tkinter as tk
import os
import sys



from typing import TYPE_CHECKING


class RecordTilePage(tk.Frame): # Sub-lcassing tk.Frame
    
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
        self.copy_logo = tk.PhotoImage(file =StaticVariables.COPY_LOGO_PATH)
        self.edit_logo = tk.PhotoImage(file =StaticVariables.EDIT_LOGO_PATH)
        self.back_logo = tk.PhotoImage(file=StaticVariables.BACK_LOGO_PATH)

 
        
        
        back_button = tk.Button( self, image = self.back_logo, borderwidth=0, bg='red', command=lambda: master.switch_Canvas(StaticVariables.RECORD_LIST_PAGE))
        back_button_canvas = self.canvas.create_window( 10, 10, anchor = "nw",window = back_button)
        edit_button = tk.Button( self, image = self.edit_logo, borderwidth=0, bg='red', command=lambda: master.switch_Canvas(StaticVariables.EDIT_RECORD_PAGE))
        edit_button_canvas = self.canvas.create_window( 150, 240, anchor = "nw",window = edit_button)

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


        global status
        status = ''
        
        def copy_to_clipboard(button):
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')
            
            if button == StaticVariables.L_WEBSITE_STRING :
                text = str(q_website)
                label_username_copied.config(text='')
                label_email_copied.config(text='')
                label_password_copied.config(text='')
                label_website_copied.config(text=StaticVariables.COPIED)
            elif button == StaticVariables.L_USERNAME_STRING:
                text = str(q_username)
                label_website_copied.config(text='')
                label_email_copied.config(text='')
                label_password_copied.config(text='')
                label_username_copied.config(text=StaticVariables.COPIED)
            elif button == StaticVariables.L_EMAIL_STRING:
                text = str(q_email)
                label_website_copied.config(text='')
                label_username_copied.config(text='')
                label_password_copied.config(text='')
                label_email_copied.config(text=StaticVariables.COPIED)
            else:
                text = str(q_password)
                label_website_copied.config(text='')
                label_username_copied.config(text='')
                label_email_copied.config(text='')
                label_password_copied.config(text=StaticVariables.COPIED)
            
            
            command = 'echo ' + text.strip() + '| clip'
            os.system(command)
            


        
        # website
        label_website = tk.Label(self, bg='red',foreground='white', image= self.website_logo)
        label_website_canvas = self.canvas.create_window( 2, 50, anchor = "nw",window = label_website)
        
        label_website_query = tk.Label(self, bg='red',foreground='white', text=q_website)
        label_website_query_canvas = self.canvas.create_window( 60, 50, anchor = "nw",window = label_website_query)
        
        copy_website_button = tk.Button( self, image= self.copy_logo, borderwidth=0, bg='red', command=lambda: copy_to_clipboard(StaticVariables.L_WEBSITE_STRING))
        copy_website_button_canvas = self.canvas.create_window( 190, 50, anchor = "nw",window = copy_website_button)
        
        label_website_copied = tk.Label(self, bg='red',foreground='white', text='')
        label_website_copied_canvas = self.canvas.create_window( 250, 50, anchor = "nw",window = label_website_copied)
        
        
        # username
        label_username = tk.Label(self, bg='red',foreground='white', image= self.username_logo)
        label_username_canvas = self.canvas.create_window( 2, 80, anchor = "nw",window = label_username)
        
        label_username_query = tk.Label(self, bg='red',foreground='white', text=q_username)
        label_username_query_canvas = self.canvas.create_window( 60, 80, anchor = "nw",window = label_username_query)
        
        copy_username_button = tk.Button( self, image= self.copy_logo, borderwidth=0, bg='red', command=lambda: copy_to_clipboard(StaticVariables.L_USERNAME_STRING))
        copy_username_button_canvas = self.canvas.create_window( 190, 80, anchor = "nw",window = copy_username_button)
        
        label_username_copied = tk.Label(self, bg='red',foreground='white', text='')
        label_username_copied_canvas = self.canvas.create_window( 250, 80, anchor = "nw",window = label_username_copied)
        
        
        
        # email
        label_email = tk.Label(self, bg='red',foreground='white', image= self.email_logo)
        label_email_canvas = self.canvas.create_window( 2, 110, anchor = "nw",window = label_email)
        
        label_email_query = tk.Label(self, bg='red',foreground='white', text=q_email)
        label_email_query_canvas = self.canvas.create_window( 60, 110, anchor = "nw",window = label_email_query)
        
        copy_email_button = tk.Button( self, image= self.copy_logo, borderwidth=0, bg='red', command=lambda: copy_to_clipboard(StaticVariables.L_EMAIL_STRING))
        copy_email_button_canvas = self.canvas.create_window( 190, 110, anchor = "nw",window = copy_email_button)
        
        label_email_copied = tk.Label(self, bg='red',foreground='white', text='')
        label_email_copied_canvas = self.canvas.create_window( 250, 110, anchor = "nw",window = label_email_copied)
        
        
        
        # password
        label_password = tk.Label(self, bg='red',foreground='white', image= self.password_logo)
        label_password_canvas = self.canvas.create_window( 2, 140, anchor = "nw",window = label_password)
        
        label_password_query = tk.Label(self, bg='red',foreground='white', text=q_password)
        label_password_query_canvas = self.canvas.create_window( 60, 140, anchor = "nw",window = label_password_query)
        
        copy_password_button = tk.Button( self, image= self.copy_logo, borderwidth=0, bg='red', command=lambda: copy_to_clipboard(StaticVariables.L_PASSW_STRING))
        copy_password_button_canvas = self.canvas.create_window( 190, 140, anchor = "nw",window = copy_password_button)
        
        label_password_copied = tk.Label(self, bg='red',foreground='white', text='')
        label_password_copied_canvas = self.canvas.create_window( 250, 140, anchor = "nw",window = label_password_copied)