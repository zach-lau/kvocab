"""
Includes handlers to register files with the database
"""

import psycopg2
from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    """Parse a config file and return a dictionary of credentiali values"""
    parser = ConfigParser()
    parser.read(filename)
    res = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            key, value = param
            res[key] = value
    else:
        raise Exception(f'Section {section} not found in fie {filename}')
    return res

class dbConnection:
    def __init__(self, inifile):
        creds = config(inifile)
        self.conn = psycopg2.connect(**creds)
    def execute(self, statement):
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(statement)
                return curs.fetchall()
    def execute_list(self, statements):
        with self.conn:
            res = []
            with self.conn.cursor() as curs:
                for s in statements:
                    curs.execute(s)
                    res.extend(curs.fetchall())
        return res
    def close(self):
        self.conn.close()

if __name__ == '__main__':
    try:
        db = dbConnection('database.ini')
        # res = db.execute('SELECT * FROM WORDS;')
        res = db.execute_list([
            """SELECT * FROM WORDS WHERE word = '학생';""",
            """SELECT * FROM WORDS WHERE word = '엄마';"""
        ])
        print(res)
    finally:
        db.close()
    