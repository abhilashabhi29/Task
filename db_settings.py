import sqlite3
from sqlite3 import Error

class Settings():
    def create_connection(self,db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return None


    def create_table(self,conn):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return: Boolean to confirm Table created
        """
        sql_create_table = """CREATE TABLE IF NOT EXISTS USERs (
                                    SYMBOL varchar(32),
                                    SERIES varchar(32),
                                    OPEN int,HIGH int,
                                    LOW int,CLOSE int,
                                    LAST int,
                                    PREVCLOSE int,
                                    TOTTRDQTY int,
                                    TIMESTAMP date);"""


        try:
            c = conn.cursor()
            c.execute(sql_create_table)
            return True
        except Error as e:
            print(e)
            return False
