
from classes.handlers.account_handler import AccountHandler
from classes.handlers.log_handler import LogHandler

from classes.utilities.static_variables import StaticVariables

import tkinter as tk
import sys

from typing import TYPE_CHECKING




class AccountVerifiedPage(tk.Canvas):

    if TYPE_CHECKING:
        from main import SampleApp
        app = SampleApp()

    def __init__(self, app, *args, **kwargs):

        tk.Frame.__init__(self,app, *args, **kwargs)
        self.canvas = tk.Canvas(self , bg = 'red', width = 345,height = 518)
        self.canvas.pack(fill = "both", expand = True)
        app.title(StaticVariables.ACCOUNT_VERIFIED)
        app.iconbitmap(StaticVariables.COBRA_ICON_PATH)
        self.login_logo = tk.PhotoImage(file = StaticVariables.LOGIN_LOGO_PATH)
        
        
        website_label = tk.Label(self, bg='red', text=StaticVariables.ACC_VERIFIED, foreground='white')
        website_canvas = self.canvas.create_window( 80, 150, anchor = "nw",window = website_label)
        
        
        self.small_cobra_logo = tk.PhotoImage(file = StaticVariables.SMALL_COBRA_LOGO_PATH)
        small_logo_image = self.canvas.create_image(130, 450, image = self.small_cobra_logo, anchor=tk.NW)
        
        
        go_to_login_button = tk.Button( self, image = self.login_logo, borderwidth=0,  bg='red', command=lambda: app.switch_Canvas(StaticVariables.LANDING_PAGE))
        go_to_login_button_canvas = self.canvas.create_window( 160, 300, anchor = "nw",window = go_to_login_button)