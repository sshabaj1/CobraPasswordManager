from classes.handlers.directory_handler import DirectoryHandler
from inspect import currentframe, getframeinfo
import logging
from datetime import datetime
from datetime import datetime
import os
from datetime import date, datetime


time = datetime.now()
class LogHandler():
    

    def create_log_file(self):
        today = date.today()
        log_dir = today.strftime("%d-%m-%Y")
        DirectoryHandler.mkdir_today(self, 'logs')
        num_of_frames = (len(os.listdir(f'logs/{log_dir}')) + 1)
        log_path = f'logs/{log_dir}//LOG{num_of_frames}.log'
        logging.basicConfig(filename=log_path, filemode='w',format= '%(asctime)s - %(levelname)s - %(message)s')


    def debug_log(self, function_name, context_name,context):
        print('enterd at debug log') 
        logger=logging.getLogger()
        logger.setLevel(logging.DEBUG)
        frameinfo = getframeinfo(currentframe())
        class_name = self.__class__.__name__
        var_name = context_name
        con_name = context
        LOG_DETAILS = str(f'Line: {frameinfo.lineno}| {class_name}.{function_name}()| {var_name}: {con_name}')
        logger.debug(f'{LOG_DETAILS}')
        
        
    def info_log(self, function_name, context_name,context):
        logger=logging.getLogger()
        logger.setLevel(logging.INFO)
        frameinfo = getframeinfo(currentframe())
        class_name = self.__class__.__name__
        var_name = context_name
        con_name = context
        LOG_DETAILS = str(f'Line: {frameinfo.lineno}| {class_name}.{function_name}()| {var_name} {con_name}')
        logger.info(f'{LOG_DETAILS}')
    
    def critical_log(self, function_name, context_name, context):
        logger=logging.getLogger()
        logger.setLevel(logging.CRITICAL)
        frameinfo = getframeinfo(currentframe())
        class_name = self.__class__.__name__
        var_name = context_name
        con_name = context
        LOG_DETAILS = str(f'Line: {frameinfo.lineno}| {class_name}.{function_name}()| {var_name} {con_name}')
        logger.critical(f'{LOG_DETAILS}')