from classes.utilities.static_variables import StaticVariables
from classes.handlers.log_handler import LogHandler
from configuration import Configuration

import sys
import smtplib, ssl

class EmailHandler():
    
    
    
    def send_email(self, email, msg):
        function_name = sys._getframe().f_code.co_name
        LogHandler.debug_log(self, function_name, '', '')
        
        context = ssl.create_default_context()
        with smtplib.SMTP(Configuration.EMAIL_SMTP_SERVER, Configuration.EMAIL_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(Configuration.COBRA_EMAIL, Configuration.EMAIL_PASSWORD)
            server.sendmail(Configuration.COBRA_EMAIL, email, msg)
            LogHandler.debug_log(self, function_name, 'Email Sent', msg)