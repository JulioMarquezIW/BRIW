

import pymysql

from briw.database.config import Config


class Database:
    """Database connection class."""

    def __init__(self, config):
        self.host = config.db_host
        self.username = config.db_user
        self.password = config.db_password
        self.port = config.db_port
        self.dbname = config.db_name
        self.conn = None

    def open_connection(self):
        try:
            if self.conn is None:
                self.conn = pymysql.connect(self.host,
                                            user=self.username,
                                            passwd=self.password,
                                            db=self.dbname,
                                            connect_timeout=5)
        except pymysql.MySQLError as e:
            print(e)

    def run_query(self, query):
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                records = []
                print("QUERY => " + query)
                cur.execute(query)
                splited_query = query.split(' ')
                if splited_query[0].upper() == 'SELECT':
                    result = cur.fetchall()
                    for row in result:
                        records.append(row)
                elif splited_query[0].upper() == 'INSERT':
                    records = cur.lastrowid
                cur.close()
                return records
        except pymysql.MySQLError as e:
            print("Error connecting to database: " + str(e))
        finally:
            if self.conn:
                self.conn.commit()
                self.conn.close()
                self.conn = None
