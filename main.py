from cgitb import text
from decimal import Clamped
from email.mime import image
import imp
import tkinter as tk
from tkinter import ttk
import re
import secrets
import string
import sys
import psycopg2
import smtplib, ssl
from classes.pages.loginPage import LoginPage
from classes.pages.landingPage import LandingPage
from classes.pages.accountPage import AccountPage
from classes.pages.recordListPage import RecordListPage
from classes.pages.recordTilePage import RecordTilePage
from classes.pages.registerPage import RegisterPage
from classes.pages.verifyMailPage import VerifyMailPage
from classes.pages.accountVerifiedPage import AccountVerifiedPage
from classes.pages.changePasswordPage import ChangePasswordPage
from classes.pages.addRecordPage import AddRecordPage
from classes.pages.changeEmailPage import ChangeEmailPage
from classes.pages.editRecordPage import EditRecordPage
from classes.pages.recoverPasswordPage import RecoverPasswordPage
from classes.pages.setNewPasswordPage import SetNewPasswordPage
from classes.pages.passwordRecoveredPage import PasswordRecoveredPage



hostname = 'localhost'
database = 'CobraPasswordManager'
username = 'postgres'
pwd = 'Ab1234566'
port_id = 5432
conn = None
cur = None


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._Canvas= None
        self.switch_Canvas('LoginPage')

    
    def switch_Canvas(self, Canvas_class):
        print('main.py/switch_Canvas')
        template_canvas_class = getattr(sys.modules[__name__], Canvas_class)
        new_Canvas = template_canvas_class(self)
        if self._Canvas is not None:
            self._Canvas.destroy()
        self._Canvas = new_Canvas
        self._Canvas.pack()
    account_id = ''
    
    def query_account(self, qid):
        print('main.py/query_account')
        try:
            conn =  psycopg2.connect(
                    host = hostname,
                    dbname = database,
                    user = username,
                    password = pwd,
                    port = port_id
                    )

            cur = conn.cursor()
            q_id = qid
            cur.execute("SELECT * FROM account WHERE id = '%s'" %q_id)
            rows = cur.fetchall()
            idi = (rows[0])[0]
            usrn = (rows[0])[1]
            eml = (rows[0])[2]
            passwr = (rows[0])[3]

            print(f'queried--> id: {idi}, username: {usrn}, email: {eml}, password: {passwr}')
            credetials = [idi, usrn, eml, passwr]
            print('credentials main: ', credetials)
            
            
            
            conn.commit()
            cur.close()
            conn.close()
            return credetials
        except Exception as error:
            print('db error:', error)



        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
                
                
    def create_otp_recover_password(self):
        print('main.py/create_otp_recover_password')
        alphabet = string.ascii_letters + string.digits
        otp = ''.join(secrets.choice(alphabet) for i in range(8))
        print('otp is: ', otp)
        q_otp = self.get_otp(otp)
        return otp            
    
                
    def send_otp_recover_password(self, email):
        print('main.py/send_otp_recover_password')
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "cobra.manager2022@gmail.com"
        receiver_email = email
        password = 'Ab1234566'
        change_password_code = self.create_otp_recover_password()
        print('main.py/send_otp_recover_password/otp: ', change_password_code)
        message = f"""\
        Subject: Change Password

        This is the One time code to recover your password
        
        code: {change_password_code}
        
        """

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    
    
                
    def query_account_by_username(self, user):
        print('main.py/query_account')
        try:
            conn =  psycopg2.connect(
                    host = hostname,
                    dbname = database,
                    user = username,
                    password = pwd,
                    port = port_id
                    )

            cur = conn.cursor()
            q_usr = user
            cur.execute("SELECT * FROM account WHERE username = '%s'" %q_usr)
            rows = cur.fetchall()
            idi = (rows[0])[0]
            usrn = (rows[0])[1]
            eml = (rows[0])[2]
            passw = (rows[0])[3]


            print(f'queried--> id: {idi}, username: {usrn}, email: {eml}, password: {passw}')
            credetials = [idi, usrn, eml, passw]
            print('credentials main: ', credetials)
            
            
            
            conn.commit()
            cur.close()
            conn.close()
            return credetials
        except Exception as error:
            print('db error:', error)



        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
    
    
    def get_account_username(self, username):
        print('main.py/get_account_username')
        self.username = username
        
    def set_account_username(self):
        print('main.py/set_account_username')
        return self.username
    
    
    def get_otp(self, otp):
        print('main.py/get_otp')
        self.otp = otp
        
    def set_otp(self):
        print('main.py/set_otp')
        return self.otp
    
    
    def get_account_id(self, id):
        print('main.py/get_account_id')
        self.account_id = id
        
    def set_account_id(self):
        print('main.py/set_account_id')
        return self.account_id
    
    def get_record_id(self,id):
        print('main.py/get_record_id')
        self.record_id = id
        
    def set_record_id(self):
        print('main.py/set_record_id')
        return self.record_id
    
    


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()