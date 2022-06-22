from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables

import tkinter as tk
import sys
from typing import TYPE_CHECKING




class LandingPage(tk.Frame): # Sub-lcassing tk.Frame
    
    if TYPE_CHECKING:
        from main import SampleApp
        app = SampleApp()
    
    def __init__(self, master, *args, **kwargs):

        # self is now an istance of tk.Frame
        tk.Frame.__init__(self,master, *args, **kwargs)
        # make a new Canvas whose parent is self.
        self.canvas = tk.Canvas(self, bg = 'red' ,width = 345,height = 518)
        self.canvas.pack(fill = "both", expand = True)
        master.title(StaticVariables.COBRA_PASSW_MANAGER)

        acc_id = master.set_account_id()

        
        self.logout_logo = tk.PhotoImage(file =StaticVariables.LOGOUT_LOGO_PATH )
        self.list_logo = tk.PhotoImage(file =StaticVariables.LIST_LOGO_PATH)
        self.account_logo = tk.PhotoImage(file =StaticVariables.ACCOUNT_LOGO_PATH )
        self.small_cobra_logo = tk.PhotoImage(file =StaticVariables.SMALL_COBRA_LOGO_PATH)
        small_logo_image = self.canvas.create_image(130, 400, image = self.small_cobra_logo, anchor=NW)
        
        account_button = tk.Button( self, image = self.account_logo, borderwidth=0, bg='red', command=lambda: master.switch_Canvas(StaticVariables.ACCOUNT_PAGE))
        account_button_canvas = self.canvas.create_window( 200, 255, anchor = "nw",window = account_button)
        record_list_button = tk.Button( self, image = self.list_logo, borderwidth=0, bg='red', command=lambda: master.switch_Canvas(StaticVariables.RECORD_LIST_PAGE))
        record_list_button_canvas = self.canvas.create_window( 110, 250, anchor = "nw",window = record_list_button)
        logout_button = tk.Button( self, image = self.logout_logo, borderwidth=0, bg='red', command=lambda: master.switch_Canvas(StaticVariables.LOGIN_PAGE))
        logout_button_canvas = self.canvas.create_window( 10, 10, anchor = "nw",window = logout_button)