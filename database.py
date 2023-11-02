"""
Includes handlers to register files with the database
"""

import psycopg2
from configparser import ConfigParser
import csv

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
    """
    Usage specific db connection
    """
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
                res.append(curs.fetchall())
        return res
    def get_unique_words(self):
        return [x[0] for x in self.execute("""SELECT DISTINCT WORD FROM WORDS;""")]
    def check_exists(self, word):
        """ Check if a word exists in the db"""
        res = self.execute(f"""SELECT 1 FROM WORDS WHERE word = '{word}';""")
        return len(res) > 0
    def update_word(self, word, count):
        """Update the count of a single word in the db. Add it if it doesn't yet exist"""
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(f"""SELECT WORD, NUM FROM WORDS WHERE word = '{word}';""")
                res = curs.fetchall()
                if len(res) > 0:
                    _, old_count = res[0]
                    new_count = old_count + count
                    curs.execute(f"""UPDATE WORDS SET num = {new_count} WHERE word = '{word}' RETURNING *;""")
                else: # In this case we need a insert
                    curs.execute(f"""INSERT INTO WORDS (word, num) values ('{word}', {count}) RETURNING *;""")
                res = curs.fetchall()
        return res
    def update_many(self, word_list):
        with self.conn:
            with self.conn.cursor() as curs:
                # Prep work to get all the words
                curs.execute(f"""SELECT WORD, NUM FROM WORDS;""")
                res = curs.fetchall()
                word_dict = {}
                for row in res:
                    word, num = row
                    word_dict[word] = num
                update_list = []
                insert_list = []
                for elem in word_list:
                    word, num = elem
                    if word in word_dict.keys():
                        new_num = word_dict[word] + num
                        update_list.append((new_num, word)) # Backwards order
                    else: # New word
                        insert_list.append((word, num))
                print(update_list)
                print(insert_list)
                update_sql = f"""UPDATE WORDS SET num = %s WHERE word = %s;"""
                insert_sql = f"""INSERT INTO WORDS (WORD, NUM) VALUES (%s, %s);"""
                curs.executemany(update_sql, update_list)
                curs.executemany(insert_sql, insert_list)
        
    def import_file(filename):
        with open(filename, 'r') as f:
            r = csv.reader(f)
            for row in r:
                pass
    def close(self):
        self.conn.close()

if __name__ == '__main__':
    try:
        db = dbConnection('database.ini')
        # res = db.execute('SELECT * FROM WORDS;')
        # res = db.execute_list([
        #     """SELECT * FROM WORDS WHERE word = '학생';""",
        #     """SELECT * FROM WORDS WHERE word = '엄마';"""
        # ])
        # res = db.check_exists('개새끼')A
        # res = db.update_word('졍국 사랑해', 100)
        db.update_many([('정국', 1), ('지민', 10)])
        # print(res)
    finally:
        db.close()
    