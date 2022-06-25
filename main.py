from classes.handlers.log_handler import LogHandler
from classes.handlers.database_handler import DatabaseHandler
from classes.handlers.email_handler import EmailHandler

from classes.pages.accountPage import AccountPage
from classes.pages.accountVerifiedPage import AccountVerifiedPage
from classes.pages.addRecordPage import AddRecordPage
from classes.pages.changeEmailPage import ChangeEmailPage
from classes.pages.changePasswordPage import ChangePasswordPage
from classes.pages.editRecordPage import EditRecordPage
from classes.pages.landingPage import LandingPage
from classes.pages.passwordRecoveredPage import PasswordRecoveredPage
from classes.pages.recordListPage import RecordListPage
from classes.pages.recordTilePage import RecordTilePage
from classes.pages.recoverPasswordPage import RecoverPasswordPage
from classes.pages.registerPage import RegisterPage
from classes.pages.setNewPasswordPage import SetNewPasswordPage
from classes.pages.verifyMailPage import VerifyMailPage
from classes.pages.loginPage import LoginPage
from classes.pages.accountVerifiedPage import AccountVerifiedPage

from classes.utilities.static_variables import StaticVariables

import tkinter as tk
import secrets
import string
import sys
import psycopg2





class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._Canvas= None
        self.switch_Canvas(StaticVariables.LOGIN_PAGE)

    
    def switch_Canvas(self, Canvas_class):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
            
        template_canvas_class = getattr(sys.modules[__name__], Canvas_class)
        new_Canvas = template_canvas_class(self)
        if self._Canvas is not None:
            self._Canvas.destroy()
        self._Canvas = new_Canvas
        self._Canvas.pack()

    
    def query_account(self, qid):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        query = "SELECT * FROM account WHERE id = %s"

        
        try:
            rows =  DatabaseHandler.query_database_with_params(self, 'Main', query, qid)
            idi = (rows[0])[0]
            usrn = (rows[0])[1]
            eml = (rows[0])[2]
            passwr = (rows[0])[3]

            credetials = [idi, usrn, eml, passwr]
            
            LogHandler.info_log(self, function_name, 'credetials: ', credetials)

            return credetials
        
        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        

                
                
    def create_otp_recover_password(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        alphabet = string.ascii_letters + string.digits
        otp = ''.join(secrets.choice(alphabet) for i in range(8))
        print('otp is: ', otp)
        q_otp = self.get_otp(otp)
        return q_otp            
    
                
    def send_otp_recover_password(self, email):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        message = f"""\
        Subject: Change Password

        This is the One time code to recover your password
        
        code: {self.create_otp_recover_password()}
        
        """

        EmailHandler.send_email(self, email, message)
    
    
                
    def query_account_by_username(self, user):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        query = "SELECT * FROM account WHERE username = %s"

        
        try:
            rows =  DatabaseHandler.query_database_with_params(self, 'Main', query, user)
            idi = (rows[0])[0]
            usrn = (rows[0])[1]
            eml = (rows[0])[2]
            passw = (rows[0])[3]

            credetials = [idi, usrn, eml, passw]
            
            LogHandler.info_log(self, function_name, 'credentials', credetials)
            
            return credetials
        
        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
    
    
    def get_account_username(self, username):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        self.username = username
        
    def set_account_username(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        return self.username
    
    
    def get_otp(self, otp):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        self.otp = otp
        
    def set_otp(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        return self.otp
    
    
    def get_account_id(self, id):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        self.account_id = id
        
    def set_account_id(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        return self.account_id
    
    def get_record_id(self,id):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        self.record_id = id
        
    def set_record_id(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        return self.record_id
    
    


if __name__ == "__main__":
    app = SampleApp()
    DatabaseHandler.create_account_table(app)
    DatabaseHandler.create_record_table(app)
    DatabaseHandler.create_keyHolder_table(app)
    LogHandler.create_log_file(app)
    app.mainloop()