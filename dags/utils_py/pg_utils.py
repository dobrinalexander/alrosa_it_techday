import psycopg2
import pandas as pd

from loguru import logger
from psycopg2.extras import execute_values

class PostgresConnector:
    def __init__(self, dbname: str, user: str, host: str, password: str):
        self.dbname = dbname
        self.user = user
        self.host = host
        self.password = password

        #create connection to DB
        try:
            creds = f"""dbname='{self.dbname}' user='{self.user}' host='{self.host}' password='{self.password}'"""
            logger.debug(f"creds pg: {creds}")
            self.conn = psycopg2.connect(creds)
            self.cursor = self.conn.cursor()
        except:
            logger.error("I am unable to connect to the PG database")
            raise ConnectionAbortedError("I am unable to connect to the PG database")
    
    def init_database(self, path_init_sql: str, init_flag: bool) -> None:
        """
        Function init DB and create schema raw_data
        """
        logger.debug("INIT DB")
        if init_flag == True:
            with open(path_init_sql, 'r') as f:
                sql = f.read()
            logger.debug("SQL INIT QUERY:")
            logger.debug(sql)
            self.cursor.execute(sql)
            self.conn.commit()
        else:
            logger.debug("Skip init db")

    def insert_data(self, data: dict, table_name: str, schema_name: str, ) -> None:
        """
        Function insert data to DB
        """
        col_list = data['columns_insert']
        columns = ', '.join(col_list)

        values = data['values_insert']

        query = f'INSERT INTO {schema_name}.{table_name} ({columns}) VALUES %s ON CONFLICT DO NOTHING;'
        logger.debug(query)

        execute_values(self.cursor, query, values, template=None, page_size=100)

        check_table = pd.read_sql_query(f"""SELECT COUNT(*) AS cnt_row FROM {schema_name}.{table_name};""", self.conn)
        logger.debug(check_table.head().T)
        self.conn.commit()


