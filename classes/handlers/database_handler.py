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
    
    
    def connect_enc_database(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        enc_conn =  psycopg2.connect(
                    host = Configuration.DATABASE_HOST_NAME,
                    dbname = Configuration.COBRA_DATABASE_NAME,
                    user = Configuration.DATABASE_USERNAME,
                    password = Configuration.DATABASE_PASSWORD,
                    port = Configuration.DATABASE_PORT_ID
                    )
        enc_cur = enc_conn.cursor()
        connection_dict = {'connection' : enc_conn, 'cursor' : enc_cur}

        LogHandler.debug_log(self, function_name, 'connection_dict: ', connection_dict)

        return connection_dict


    def create_table(self, conn, create_command, table_name):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        main_cur = conn.cursor()
        main_cur.execute(create_command)
        LogHandler.debug_log(self, function_name, StaticVariables.TABLE_CREATED, table_name)

    
    def drop_table(self, conn, drop_command, table_name):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        main_cur = conn.cursor()
        main_cur.execute(drop_command)

        LogHandler.debug_log(self, function_name, StaticVariables.TABLE_DELETED, table_name)


    def insert(self, connection, script, value):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        conn = connection
        cur = conn.cursor()
        cur.execute(script, value)

        LogHandler.info_log(self, function_name, 'Value Inserted in database: ', value)

    
    def update(self, connection, script, value):

        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        conn = connection
        cur = conn.cursor()
        cur.execute(script, value)

        LogHandler.info_log(self, function_name, 'Database Table Updated: ', '')
    

    def delete(self, connection, script, param):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        
        conn = connection
        cur = conn.cursor()
        cur.execute(script, param)
        
        LogHandler.info_log(self, function_name, 'Value Deleted from database: ', param)


    def query_database_with_params(self, connection, query, args):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        main_query = query
        main_args = args
        conn = connection
        cursor = conn.cursor()
        cursor.execute(main_query, main_args)
        rows = cursor.fetchall()

        LogHandler.info_log(self, function_name, 'rows: ', rows)

        return rows


    def query_database_without_params(self, connection, query):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        main_query = query
        conn = connection
        cursor = conn.cursor()
        cursor.execute(main_query)
        rows = cursor.fetchall()

        LogHandler.info_log(self, function_name, 'rows: ', rows)

        return rows