from classes.handlers.email_handler import EmailHandler
from classes.handlers.encryption_handler import  EncryptionHandler
from classes.handlers.log_handler import LogHandler
from classes.utilities.static_variables import StaticVariables
from classes.handlers.database_handler import DatabaseHandler
from classes.handlers.record_handler import  RecordHandler
from classes.handlers.otp_handler import OtpHandler

import sys
import psycopg2
from cryptography.fernet import Fernet


class AccountHandler():

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


    def create_account(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        usrname = self.username
        eml = self.email
        key = EncryptionHandler.generate_encryption_key()
        raw_password = self.password
        byte_password = EncryptionHandler.encrypt(raw_password, key)
        passw = byte_password.decode('utf-8')
        dublicate_query = 'SELECT * FROM account WHERE usermane = %s'
        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        try:
            rows =  DatabaseHandler.query_database_with_params(self, conn, cur, dublicate_query, usrname)
            if len(rows) > 0:
                account_created = {"status" : False}
                return account_created
            else:
                acc_id = AccountHandler.create_account_id()
                insert_script = 'INSERT INTO account (id, username, email, password) VALUES ( %s, %s, %s, %s)'
                insert_values = (acc_id, usrname, eml, passw)
                DatabaseHandler.insert(self, conn, cur, insert_script, insert_values)
                conn.commit()
                cur.close()
                conn.close()
                account_created = {"status" : True, 'acc_id': acc_id}
                return account_created
        
        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def create_account_id(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        query = "SELECT id FROM account ORDER BY id desc LIMIT 1"
        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        try:
            rows =  DatabaseHandler.query_database_with_params(self, conn, cur, query)
            cur.close()
            conn.close()
            if len(rows) > 0:
                query_id = str((rows[0])[0])
                acc_id = 1 + int(query_id)
                return acc_id
            else:
                acc_id
                return acc_id
        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()
     
     
                
    def get_record_by_ids(self, rec_id, acc_id):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        q_record_id = rec_id
        q_account_id = acc_id
        query = "SELECT * FROM record WHERE account_id = %s AND id = %s"
        args = (q_account_id, q_record_id)
        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        
        try:
            rows =  DatabaseHandler.query_database_with_params(self, conn, cur, query, args)
            
            LogHandler.info_log(self, function_name, 'rows: ', rows)

            q_web = (rows[0])[2]
            q_usern = (rows[0])[3]
            q_mail = (rows[0])[4]
            q_passw = (rows[0])[5]
            
            record = [q_web, q_usern, q_mail, q_passw]

            LogHandler.info_log(self, function_name, 'Record Returned Query:  ', record)
            
            cur.close()
            conn.close()
            
            return record
        
        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
            
        finally:
            if conn is not None:
                cur.close()
                conn.close()


        
    def get_record(self, id, web, usern, eml):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        acc_id = int(id)
        website = web
        user = usern
        email = eml

        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        query = "SELECT * FROM record WHERE account_id = %s AND website = %s AND username = %s AND email = %s"
        args = (acc_id, website, user, email)

        
        try:
            
            
            rows =  DatabaseHandler.query_database_with_params(self, conn, cur, query, args)

            q_id = (rows[0])[0]
            q_ac_id = (rows[0])[1]
            q_web = (rows[0])[2]
            q_usern = (rows[0])[3]
            q_mail = (rows[0])[4]
            q_passw = (rows[0])[5]
            
            record_returned = [q_id, q_ac_id, q_web, q_usern, q_mail, q_passw]
            LogHandler.info_log(self, function_name, 'record_returned: ', record_returned)
            
                    
            cur.close()
            conn.close()
            return record_returned

        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
            
        finally:
            if conn is not None:
                cur.close()
                conn.close()


    
    def query_records_by_account_id(self, id):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        acc_id = id
        query = ("SELECT * FROM record WHERE account_id = %s")
        args = acc_id
        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        records = []

        try:
            
            
            
            rows =  DatabaseHandler.query_database_with_params(self, conn, cur, query, args)

            LogHandler.debug_log(self, function_name, 'rows lenght', len(rows))

            if len(rows) > 1:
                for i in range(len(rows)):

                    LogHandler.debug_log(self, function_name, 'Enterd in loop: ', i)

                    idi = (rows[i])[0]
                    ac_id = (rows[i])[1]
                    web = (rows[i])[2]
                    user = (rows[i])[3]
                    mail = (rows[i])[4]
                    passw = (rows[i])[5]
                    record = RecordHandler(ac_id,web, user, mail, passw)
                    dict_object = record.__dict__
                    values_object = dict_object.values()
                    list_obj = list(values_object)
                    list_obj.pop(0)
                    records.append(list_obj)
            else:
                if len(rows) == 0:
                    LogHandler.debug_log(self, function_name, 'There are no records on rows:  ', '')

                    records = 'NO'
                else:
                    idi = (rows[0])[0]
                    ac_id = (rows[0])[1]
                    web = (rows[0])[2]
                    user = (rows[0])[3]
                    mail = (rows[0])[4]
                    passw = (rows[0])[5]
                    record = RecordHandler(ac_id, web, user, mail, passw)
                    dict_object = record.__dict__
                    values_object = dict_object.values()
                    list_obj = list(values_object)
                    LogHandler.debug_log(self, function_name, 'List of objects:   ', list_obj)

                    records.append(list_obj)

            
    
    
            cur.close()
            conn.close()

            return records

        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
            
        finally:
            if conn is not None:
                cur.close()
                conn.close()


    
    def check_verify_email(self, new_eml, verify_eml):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        new_email = new_eml
        verify_email = verify_eml
        if new_email == verify_email:

            return True


    
    def check_verify_password(self, new_passw, verify_passw):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        new_pass = new_passw
        verify_pass = verify_passw
        if new_pass == verify_pass:

            return True


    
    def check_old_email(self, email):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        acc_email = self.email
        old_email = email
        if acc_email == old_email:

            return True



    def check_old_password(self, passw):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        q_key = self.query_encryption_key(self.id)
        key = q_key[2]
        acc_password = EncryptionHandler.decrypt(key, self.password)
        old_password = passw
        if acc_password == old_password:

            return True


    def check_account_status(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        status = ''
        query = "select * from account where username = %s"
        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        
        
        try:
            
            rows =  DatabaseHandler.query_database_with_params(self, conn, cur, query, self.username)
            status = (rows[5])

            cur.close()
            conn.close()

            return status
        
        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
            
        finally:
            if conn is not None:
                cur.close()
                conn.close()


    def confirm_account(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        query = "Update account set status = %s where username = %s"
        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']

        try:
            DatabaseHandler.update(self, conn, cur, query, ('Verified', self.username))

            cur.commit()
            cur.close()
            conn.close()

        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
            
        finally:
            if conn is not None:
                cur.close()
                conn.close()


    
    
    def query_encryption_key(self, acc_id):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        connection_dict = DatabaseHandler.connect_enc_database(self)
        query = "SELECT * FROM keyHolder WHERE account_id = '%s'"
        conn = connection_dict['connection']
        cur = connection_dict['cursor']

        try:
            
            rows =  DatabaseHandler.query_database_with_params(self, conn, cur, query, acc_id)
            q_id = (rows[0])[0]
            q_ac_id = (rows[0])[1]
            q_key = (rows[0])[2]
            
            record = [q_id, q_ac_id, q_key]
            
            LogHandler.debug_log(self, function_name, 'record: ', record)
            
                    
            cur.close()
            conn.close()
            
            return record
        
        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                
                
                
    def create_encrypt_key_id(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        connection_dict = DatabaseHandler.connect_enc_database(self)
        query = "SELECT * FROM keyHolder ORDER BY id DESC LIMIT 1"
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        
        try:
            rows =  DatabaseHandler.query_database_without_params(self, conn, cur, query)

            if len(rows) > 0:
                q_id = (rows[0])[0]
                record_id = 1 + q_id
            else:
                record_id = 1
            
            LogHandler.info_log(self, function_name, 'Record id: ', record_id)
                    
            cur.close()
            conn.close()
            
            return record_id
        
        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                
                
    
    def insert_encrypted_key(self, enc_key, acc_id):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        account_id = acc_id
        key = enc_key.decode("utf-8") 
        id = self.create_encrypt_key_id()
        
        query = 'INSERT INTO keyHolder (id, account_id, key) VALUES (%s,%s, %s)'
        args = (id, account_id, key)
        connection_dict = DatabaseHandler.connect_enc_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        
        try:
            
            DatabaseHandler.insert(self, conn, cur, query, args)
            
            conn.commit()   
            cur.close()
            conn.close()

        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                
                
    
    def get_otp(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        query = "SELECT otp FROM account WHERE username = '%s'"
        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        
        try:
            rows =  DatabaseHandler.query_database_with_params(self, conn, cur, query, self.username)
            otp = str((rows[0])[0])

            
            cur.close()
            conn.close()
            
            return otp

        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                
                
    
    def verify_otp(self, n_otp):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        new_otp = n_otp
        otp = self.get_otp()
        if new_otp == otp:
            return True
        
        
        
    def set_otp(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        q_otp = OtpHandler.create_otp()
        query = "Update account set otp = %s where username = %s"
        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']

        try:
            
            DatabaseHandler.update(self, conn, cur, query, (q_otp, self.username))
            
            conn.commit()
            cur.close()
            conn.close()

        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                
                
                
    def send_otp_change_email(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.debug_log(self, function_name, '', '')
        
        message = f"""\
        Subject: Change Email
        This is the One time code to change your email
        
        code: {self.get_otp()}
        
        """
        EmailHandler.send_email(self, self.email, message)
        
        
    
    
    def send_otp_change_pass(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.debug_log(self, function_name, '', '')

        message = f"""\
        Subject: Change Password
        This is the One time code to change your password
        
        code: {self.get_otp()}
        
        """
        
        EmailHandler.send_email(self, self.email, message)
        
        
    
    def send_otp_verify_acc(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.debug_log(self, function_name, '', '')

        message = f"""\
        Subject: Verify Email
        Wellcome to Cobra Password Manager.
        One last step to registration process.
        Here is the code to finish the registration
        
        code: {self.get_otp()}
        
        """
        
        EmailHandler.send_email(self, self.email, message)
        
        
    
    def query_login_credentials(self,qusername):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        
        query = "SELECT * FROM account WHERE username = '%s'"
        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        
        try:
            
            rows =  DatabaseHandler.query_database_with_params(self, conn, cur, query, str(qusername))
            query_id = str((rows[0])[0])
            query_username = str((rows[0])[1])
            query_email = str((rows[0])[2])
            q_password = str((rows[0])[3])
            query_password = bytes(q_password, 'utf-8')
            q_key = self.query_encryption_key(query_id)
            key = q_key[2]
            raw_password = EncryptionHandler.decrypt(key, query_password)
            credentials = {'id' : query_id,
                           'username' : query_username,
                           'email' : query_email,
                           'password' : raw_password
                           }
            
            LogHandler.debug_log(self, function_name, 'credentials: ', credentials)

            cur.close()
            conn.close()
            
            return credentials

        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                
                
    def insert_new_email(self, usern, new_eml):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        username_query = "SELECT * FROM account WHERE username = '%s'"
        email_query = "Update account set email = %s where id = %s"
        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        
        try:
            rows =  DatabaseHandler.query_database_with_params(self, conn, cur, username_query, str(usern))
            q_rec_id = rows[0]
            DatabaseHandler.update(self, conn, cur, email_query, (new_eml, q_rec_id))

            conn.commit()
            cur.close()
            conn.close()
            
        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                
                
    
    def insert_new_password(self, usern, new_passw):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        username_query = "SELECT * FROM account WHERE username = '%s'"
        password_query = "Update account set password = %s where id = %s"
        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        
        try:
            rows =  DatabaseHandler.query_database_with_params(self, conn, cur, username_query, str(usern))
            q_rec_id = rows[0]
            DatabaseHandler.update(self, conn, cur, password_query, (new_passw, q_rec_id))

            conn.commit()
            cur.close()
            conn.close()
            
        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                
                
    
    def change_email(self, old_eml, new_eml, verify_eml, ver_otp):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        is_old_email = self.check_old_email(old_eml)
        is_email_verified = self.check_verify_email(new_eml, verify_eml)
        is_otp_verified = self.verify_otp(ver_otp)
        status = ''
        
        if is_old_email == True:
            if is_email_verified == True:
                if is_otp_verified == True:
                    self.insert_new_email(self.username, new_eml)
                    status = 'Email Changed'
                    return status
                else:
                    status = 'OTP is incorrect'
                    return status
            else:
                status = "Emails don't match"
                return status
        else:
            status = 'Old email is incorrect'
            return status
        
        
        
    
    def change_password(self, acc_id, old_passw, new_passw, verify_passw, ver_otp):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        key_raw = self.query_encryption_key(acc_id)
        key = key_raw[2]
        byte_password = EncryptionHandler.encrypt(self, new_passw, key)
        q_password = byte_password.decode("utf-8") 
        is_old_password = self.check_old_password(old_passw)
        is_password_verified = self.check_verify_password(new_passw, verify_passw)
        is_otp_verified = self.verify_otp(ver_otp)
        status = ''
        
        if is_old_password == True:
            if is_password_verified == True:
                if is_otp_verified == True:
                    self.insert_new_password(self.username, q_password)
                    status = 'Password Changed'
                    return status
                else:
                    status = 'OTP is incorrect'
                    return status
            else:
                status = "Passwords don't match"
                return status
        else:
            status = 'Old password is incorrect'
            return status



    def set_new_password(self, acc_id, passw):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        

        str_key = self.query_encryption_key(acc_id)
        key = bytes(str_key[2], 'utf-8')
        byte_password = EncryptionHandler.encrypt(self, passw, key)
        q_password = byte_password.decode("utf-8") 
        
        query = "Update account set password = %s where id = %s"
        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        
        try:
            
            DatabaseHandler.update(self, conn, cur, query, (q_password, acc_id))

            conn.commit()
            cur.close()
            conn.close()
            
        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()
        


        