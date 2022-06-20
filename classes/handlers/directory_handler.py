import os
from datetime import date

class DirectoryHandler():
    
    
    def mkdir_today(self,path):
        today = date.today()
        dir_name = today.strftime("%d-%m-%Y")
        if_exitsts = os.path.exists(f'{path}/{dir_name}')
        
        if not if_exitsts:
            os.mkdir(f'{path}/{dir_name}')
        