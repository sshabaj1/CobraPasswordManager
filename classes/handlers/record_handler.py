from classes.handlers.database_handler import DatabaseHandler
from classes.handlers.log_handler import LogHandler

import psycopg2
import sys



class RecordHandler():
    def __init__(self,account_id, website, username, email, password):
        self.account_id = account_id
        self.website = website
        self.username = username
        self.email = email
        self.password = password
        
        
        

    def insert_record(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        q_account_id = self.account_id
        q_website = self.website
        q_username = self.username
        email = self.email
        password = self.password
        query = "SELECT id FROM record ORDER BY id desc LIMIT 1"
        connection_dict = DatabaseHandler.connect_enc_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']

        try:
            
            rows =  DatabaseHandler.query_database_without_params(self, conn, cur, query)
            
            if len(rows) > 0:
                
                LogHandler.debug_log(self, function_name, 'rows: ', rows)

                query_id = str((rows[0])[0])

                LogHandler.debug_log(self, function_name, 'query id: ', query_id)

                reco_id = 1 + int(query_id)

                LogHandler.debug_log(self, function_name, 'new record id:', reco_id)

            else:
                reco_id = 1

                LogHandler.debug_log(self, function_name, 'First Record', '')
            
            insert_script = 'INSERT INTO record (id, account_id, website, username, email, password) VALUES (%s,%s, %s, %s, %s, %s)'
            insert_values = (reco_id, q_account_id, q_website, q_username, email, password)
            DatabaseHandler.insert(self, conn, cur, insert_script, insert_values)

            
            conn.commit()
            cur.close()
            conn.close()

        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                
                
    def update_record(self, acc_id, rec_id,web, user, eml, passw):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        account_id = acc_id
        record_id = rec_id
        q_web = web
        q_user = user
        q_eml = eml
        q_passw = passw

        connection_dict = DatabaseHandler.connect_main_database(self)
        conn = connection_dict['connection']
        cur = connection_dict['cursor']
        
        try:
            

            # Update single record now
            sql_update_website = """Update record set website = %s WHERE id = %s AND account_id = %s"""
            DatabaseHandler.update(self, conn, cur, sql_update_website,  (q_web, record_id, account_id))

            sql_update_username = """Update record set username = %s WHERE id = %s AND account_id = %s"""
            DatabaseHandler.update(self, conn, cur, sql_update_username,  (q_user, record_id, account_id))

            sql_update_email = """Update record set email = %s WHERE id = %s AND account_id = %s"""
            DatabaseHandler.update(self, conn, cur, sql_update_email,  (q_eml, record_id, account_id))

            sql_update_password = """Update record set password = %s WHERE id = %s AND account_id = %s"""
            DatabaseHandler.update(self, conn, cur, sql_update_password,  (q_passw, record_id, account_id))
            
            conn.commit()
            cur.close()
            conn.close()

        except (Exception, psycopg2.DatabaseError) as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:
            if conn is not None:
                cur.close()
                conn.close()