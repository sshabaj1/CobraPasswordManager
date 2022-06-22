from classes.handlers.account_handler import AccountHandler
from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables


import tkinter as tk
from tkinter import E, StringVar, ttk
import sys
from typing import TYPE_CHECKING

record_list = []

class RecordListPage(tk.Frame): # Sub-lcassing tk.Frame
    
    if TYPE_CHECKING:
        from main import SampleApp
        app = SampleApp()
    
    def __init__(self, master, *args, **kwargs):

        tk.Frame.__init__(self,master, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg = 'red' ,width = 668,height = 550, relief="sunken")
        self.canvas.pack(fill = "both", expand = True)
        master.title(StaticVariables.RECORD_LIST)

        acc_id = master.set_account_id()

        
        acc_data = master.query_account(acc_id)
        ac_usr = acc_data[1]
        ac_mail = acc_data[2]
        ac_passw = acc_data[3]
        acc = AccountHandler(ac_usr, ac_mail, ac_passw)
        records = acc.query_records(acc_id)
        if records != StaticVariables.STRING_NO:

            function_name = sys._getframe().f_code.co_name
            LogHandler.debug_log(self, function_name, 'records: ', records)

            records[0].pop(0)
        else:
            records = []
        generated_password = StringVar()
        
        
        self.back_logo = tk.PhotoImage(file = StaticVariables.BACK_LOGO_PATH)
        self.add_record_logo = tk.PhotoImage(file =StaticVariables.ADD_RECORD_LOGO_PATH )
        
        
        back_button = tk.Button( self, image = self.back_logo, borderwidth=0, bg='red', command=lambda: master.switch_Canvas(StaticVariables.LANDING_PAGE))
        back_button_canvas = self.canvas.create_window( 10, 500, anchor = "nw",window = back_button)
        style = ttk.Style()
        style.configure(StaticVariables.TREEVIEW,
                        background = 'white',
                        foreground = 'black',
                        rowheight =25,
                        fieldbackground = 'white'
                        )
        style.map(StaticVariables.TREEVIEW,
                  background=[('selected','red')])
        # Create and show the Frame
        search_frame = tk.LabelFrame(self.canvas, text=StaticVariables.SEARCH_DATA)
        search_frame.place(height=470, width=670)
        
        
        # Create Treeview widget
        tv1 = ttk.Treeview(search_frame, columns=(1,2,3), show='headings', height='5')
        tv1.place(relheight=1, relwidth=1)
        tv1.heading(1, text=StaticVariables.WEBSITE_STRING)
        tv1.heading(2, text=StaticVariables.USERNAME_STRING)
        tv1.heading(3, text=StaticVariables.EMAIL_STRING)


        # print('matched objects --------------', matched_objects)
        def refresh_recors():
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')

            if records is not None:
                for record in records:
                    tv1.insert('', 'end', values=record)
                tv1.bind("<Double-1>", OnDoubleClick)
        

        def OnDoubleClick(event):
            function_name = sys._getframe().f_code.co_name
            LogHandler.info_log(self, function_name, '', '')

            item = tv1.identify('item',event.x,event.y)

            LogHandler.debug_log(self, function_name, 'you clicked on: ', tv1.item(item,"text"))
            LogHandler.debug_log(self, function_name, 'item: ', item)

            item_nr = int(item[1:])
            item_nr -= 1
            clicked_record = records[item_nr]
            record = records[item_nr]
            q_website = record[0]
            q_username = record[1]
            q_email = record[2]
            record_id = acc.get_record(acc_id, q_website, q_username, q_email)
            master.get_record_id(record_id[0])
            master.get_account_id(record_id[1])
            master.switch_Canvas(StaticVariables.RECORD_TILE_PAGE)
        
            
        refresh_recors()
        #Create and show the scrollbar
        scroll_bar_y = tk.Scrollbar(search_frame, orient='vertical', command=tv1.yview)
        scroll_bar_x = tk.Scrollbar(search_frame, orient='horizontal', command=tv1.xview)
        tv1.configure(xscrollcommand=scroll_bar_x.set, yscrollcommand=scroll_bar_y.set)
        scroll_bar_x.pack(side='bottom', fill='x')
        scroll_bar_y.pack(side='right', fill='y')
        
            
        #Record List Window Buttons    
        add_record_button = tk.Button( self, image = self.add_record_logo, borderwidth=0, bg='red', command=lambda: master.switch_Canvas(StaticVariables.ADD_RECORD_PAGE))
        add_record_button_canvas = self.canvas.create_window( 50, 500, anchor = "nw",window = add_record_button)