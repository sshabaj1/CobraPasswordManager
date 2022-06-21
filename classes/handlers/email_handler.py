from classes.utilities.static_variables import StaticVariables
from classes.handlers.log_handler import LogHandler
from configuration import Configuration

import sys
import smtplib, ssl

class EmailHandler():
    
    
    
    def send_email(self, email, msg):
        function_name = sys._getframe().f_code.co_name
        LogHandler.debug_log(self, function_name, '', '')
        port = 587
        smtp_server = Configuration.EMAIL_SMTP_SERVER
        sender_email = Configuration.COBRA_EMAIL
        receiver_email = email
        password = Configuration.EMAIL_PASSWORD
        message = msg
        
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        LogHandler.debug_log(self, function_name, 'Email Sent', '')