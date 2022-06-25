from classes.handlers.log_handler import LogHandler
from classes.utilities.static_variables import StaticVariables
from configuration import Configuration


import psycopg2
import sys


class DatabaseHandler():



    def connect_main_database(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        main_conn =  psycopg2.connect(
                    host = Configuration.DATABASE_HOST_NAME,
                    dbname = Configuration.COBRA_DATABASE_NAME,
                    user = Configuration.DATABASE_USERNAME,
                    password = Configuration.DATABASE_PASSWORD,
                    port = Configuration.DATABASE_PORT_ID
                    )
        main_cur = main_conn.cursor()
        connection_dict = {'connection' : main_conn, 'cursor' : main_cur}

        LogHandler.debug_log(self, function_name, 'connection_dict: ', connection_dict)

        return connection_dict
    
    
    
    def create_account_table(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        

        connection_data = DatabaseHandler.connect_main_database(self)
        conn = connection_data['connection']
        cur = conn.cursor()
        create_acount_table = ''' Create TABLE IF NOT EXISTS account(
                            id                  int PRIMARY KEY,
                            username            varchar(40) NOT NULL,
                            email               varchar(40) NOT NULL,
                            password            varchar(225) NOT NULL,
                            otp                 varchar(40),
                            status              varchar(40))'''
        try:
            cur.execute(create_acount_table)
            
            conn.commit()
            cur.close()
            conn.close()
            
        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:   
             
            if conn is not None:
                cur.close()
                conn.close()
        
        
        
    
    def create_record_table(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        connection_data = DatabaseHandler.connect_main_database(self)
        conn = connection_data['connection']
        cur = conn.cursor()
        create_record_table = ''' Create TABLE IF NOT EXISTS record(
                            id                 int PRIMARY KEY,
                            account_id         int REFERENCES account(id),
                            website            varchar(40) NOT NULL,
                            username           varchar(40) NOT NULL,
                            email              varchar(40) NOT NULL,
                            password           varchar(40))'''
        try:
            
            cur.execute(create_record_table)
            
            conn.commit()
            cur.close()
            conn.close()
            
        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:   
             
            if conn is not None:
                cur.close()
                conn.close()
        
        
    def create_keyHolder_table(self):
        print('create key holder---------------------------------------------')
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        connection_data = DatabaseHandler.connect_enc_database(self)
        conn = connection_data['connection']
        cur = conn.cursor()
        create_keyHolder_table = ''' Create TABLE IF NOT EXISTS keyHolder(
                                id                  int PRIMARY KEY,
                                account_id            varchar(40) NOT NULL,
                                key               varchar(255) NOT NULL)'''

        try:
            
            cur.execute(create_keyHolder_table)
            
            conn.commit()
            print('created -----------------------------------------------')
            cur.close()
            conn.close()
            
        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:   
             
            if conn is not None:
                cur.close()
                conn.close()
    
    
    def connect_enc_database(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        enc_conn =  psycopg2.connect(
                    host = Configuration.DATABASE_HOST_NAME,
                    dbname = Configuration.ENC_DATABASE_NAME,
                    user = Configuration.DATABASE_USERNAME,
                    password = Configuration.DATABASE_PASSWORD,
                    port = Configuration.DATABASE_PORT_ID
                    )
        enc_cur = enc_conn.cursor()
        connection_dict = {'connection' : enc_conn, 'cursor' : enc_cur}

        LogHandler.debug_log(self, function_name, 'connection_dict: ', connection_dict)

        return connection_dict



    def insert(self, database, script, value):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        LogHandler.debug_log(self, function_name, 'data to insert: ', value)
        
        connection_data = DatabaseHandler.check_database_selected(self, database)
        if connection_data != 'Error':
            conn = connection_data['connection']
            cur = conn.cursor()
        
        try:
            cur.execute(script, value)

            LogHandler.info_log(self, function_name, 'Value Inserted in database: ', value)
            
            conn.commit()
            cur.close()
            conn.close()
            
        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:   
             
            if conn is not None:
                cur.close()
                conn.close()

    
    def update(self, database, script, value):

        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        connection_data = DatabaseHandler.check_database_selected(self, database)
        if connection_data != 'Error':
            conn = connection_data['connection']
            cur = conn.cursor()
            
        try:
        
            cur.execute(script, value)

            LogHandler.info_log(self, function_name, 'Database Table Updated: ', '')
            
            conn.commit()
            cur.close()
            conn.close()
            
        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:   
             
            if conn is not None:
                cur.close()
                conn.close()
    

    def delete(self, database, script, param):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        connection_data = DatabaseHandler.check_database_selected(self, database)
        if connection_data != 'Error':
            conn = connection_data['connection']
            cur = conn.cursor()
            
        try:
            
            cur.execute(script, (param,))
            
            LogHandler.info_log(self, function_name, 'Value Deleted from database: ', param)
            
            conn.commit()
            cur.close()
            conn.close()
            
        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:   
             
            if conn is not None:
                cur.close()
                conn.close()


    def query_database_with_params(self, database, query, args):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        connection_data = DatabaseHandler.check_database_selected(self, database)
        if connection_data != 'Error':
            conn = connection_data['connection']
            cur = conn.cursor()
        
        main_query = query
        main_args = args
        
        LogHandler.info_log(self, function_name, 'args: ', (main_args,))
        
        conn = connection_data['connection']
        cur = conn.cursor()
        
        try:
            
            cur.execute(main_query, (main_args,))
            rows = cur.fetchall()

            LogHandler.info_log(self, function_name, 'rows: ', rows)

            cur.close()
            conn.close()
            return rows
        
        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:   
             
            if conn is not None:
                cur.close()
                conn.close()


    def query_database_without_params(self, database, query):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        connection_data = DatabaseHandler.check_database_selected(self, database)
        if connection_data != 'Error':
            conn = connection_data['connection']
            cur = conn.cursor()

        main_query = query
        
        try:
            cur.execute((main_query))
            rows = cur.fetchall()

            LogHandler.info_log(self, function_name, 'rows: ', rows)

            cur.close()
            conn.close()
            
            return rows
            
        
        except Exception as db_error:
            LogHandler.critical_log(self, function_name, 'Database Error: ', db_error)
        
        finally:   
             
            if conn is not None:
                cur.close()
                conn.close()
    
    
    
    def check_database_selected(self, database):
        
        if database == 'Main':
           connection_data = DatabaseHandler.connect_main_database(self)
           
        elif database == 'Enc':
            connection_data = DatabaseHandler.connect_enc_database(self)
        else:
            connection_data = 'Error'
            
        return connection_data