from classes.handlers.encryption_handler import  EncryptionHandler
from classes.handlers.log_handler import LogHandler
from classes.utilities.static_variables import StaticVariables
from classes.handlers.database_handler import DatabaseHandler

import sys
import psycopg2


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
        query = ("SELECT * FROM record WHERE account_id = %s AND id = %s")
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